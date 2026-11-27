"""Tests for the decision logic in tools/agents.py.  Run: python -m unittest tools/test_agents.py"""
import datetime as dt
import json
import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agents  # noqa: E402

NOW = dt.datetime(2026, 11, 25, 14, 0)   # a Wednesday


class ParseNext(unittest.TestCase):
    def test_last_line_wins(self):
        self.assertEqual(agents.parse_next("did work\nNEXT: 30"), 30)
        self.assertEqual(agents.parse_next("NEXT: 5 ... later NEXT: 60"), 60)

    def test_missing(self):
        self.assertIsNone(agents.parse_next("no schedule here"))
        self.assertIsNone(agents.parse_next(""))


class ParseLimit(unittest.TestCase):
    def test_not_a_limit(self):
        self.assertIsNone(agents.parse_limit_reset("reviewed PR #9", NOW))

    def test_session_limit_later_today(self):
        r = agents.parse_limit_reset("You've hit your session limit · resets 3:45pm", NOW)
        self.assertEqual(r, dt.datetime(2026, 11, 25, 15, 47))

    def test_time_already_passed_means_tomorrow(self):
        r = agents.parse_limit_reset("You've hit your session limit · resets 9am", NOW)
        self.assertEqual(r, dt.datetime(2026, 11, 26, 9, 2))

    def test_weekly_limit_with_weekday(self):
        r = agents.parse_limit_reset("You've hit your weekly limit · resets Mon 12:00am", NOW)
        self.assertEqual(r, dt.datetime(2026, 11, 30, 0, 2))

    def test_five_hour_limit_with_timezone(self):
        # The exact text seen at 17:50 on 2026-11-25, which the old pattern missed.
        r = agents.parse_limit_reset("You've hit your 5-hour limit · resets 6:30pm (America/Vancouver)", NOW)
        self.assertEqual(r, dt.datetime(2026, 11, 25, 18, 32))

    def test_ordinary_text_mentioning_limits_is_not_a_limit(self):
        self.assertIsNone(agents.parse_limit_reset("the daily budget limit is $40; reviewed PR #9", NOW))

    def test_limit_without_time_falls_back(self):
        r = agents.parse_limit_reset("You've hit your usage limit", NOW)
        self.assertEqual(r, NOW + dt.timedelta(minutes=30))


class Settings(unittest.TestCase):
    def test_keeps_allow_and_deny_and_never_prompts(self):
        main = json.dumps({"permissions": {"allow": ["Bash(git status*)"],
                                            "deny": ["Bash(gh pr merge*)", "Bash(gh issue edit *approved*)"],
                                            "defaultMode": "bypassPermissions"}})
        s = agents.agent_settings(main)["permissions"]
        self.assertEqual(s["allow"], ["Bash(git status*)"])
        self.assertIn("Bash(gh issue edit *approved*)", s["deny"])
        self.assertTrue(s["denyInsteadOfPrompting"])
        self.assertNotIn("defaultMode", s)   # nothing else is carried over


class ChildEnv(unittest.TestCase):
    def test_strips_parent_markers(self):
        env = agents.child_env({"PATH": "x", "CLAUDE_CODE_CHILD_SESSION": "1", "CLAUDECODE": "1"})
        self.assertNotIn("CLAUDE_CODE_CHILD_SESSION", env)
        self.assertNotIn("CLAUDECODE", env)
        self.assertEqual(env["PATH"], "x")
        self.assertEqual(env["CLAUDE_CODE_FORCE_SESSION_PERSISTENCE"], "1")


class Orphans(unittest.TestCase):
    def test_matches_only_supervisor_passes_of_that_role(self):
        line = 'claude.exe -p "/reviewer-loop [supervisor] Started by tools/agents.py" --model x'
        self.assertTrue(agents.is_orphan_pass(line, "reviewer"))
        self.assertFalse(agents.is_orphan_pass(line, "author"))
        self.assertFalse(agents.is_orphan_pass('claude.exe --name reviewer "/loop /reviewer-loop"', "reviewer"))
        self.assertFalse(agents.is_orphan_pass("", "reviewer"))


class Budgets(unittest.TestCase):
    RECS = [
        {"role": "explorer", "started": "2026-11-25T09:00:00", "minutes": 120, "cost_usd": 18.5,
         "model_usage": {"claude-fable-5-2": {"inputTokens": 1000, "outputTokens": 500,
                                              "cacheReadInputTokens": 9000, "costUSD": 18.0},
                         "claude-haiku-5-5": {"inputTokens": 10, "outputTokens": 5}}},
        {"role": "explorer", "started": "2026-11-24T23:00:00", "minutes": 60, "cost_usd": 9.0},
        {"role": "author", "started": "2026-11-25T10:00:00", "minutes": 20, "cost_usd": 1.5},
    ]

    def test_spent_counts_only_that_role_since_the_time(self):
        midnight = dt.datetime(2026, 11, 25)
        self.assertAlmostEqual(agents.spent(self.RECS, "explorer", midnight), 18.5)
        self.assertAlmostEqual(agents.spent(self.RECS, "author", midnight), 1.5)
        self.assertAlmostEqual(agents.spent(self.RECS, "reviewer", midnight), 0)

    def test_summarize_sums_tokens_per_model_not_cost_fields(self):
        s = agents.summarize(self.RECS, dt.datetime(2026, 11, 25))["explorer"]
        self.assertEqual(s["passes"], 1)
        self.assertEqual(s["tokens"]["claude-fable-5-2"], 10500)   # costUSD excluded
        self.assertEqual(s["tokens"]["claude-haiku-5-5"], 15)

    def test_parse_budgets(self):
        b = agents.parse_budgets("explorer=25, author=10", agents.DAILY_BUDGET_USD)
        self.assertEqual(b["explorer"], 25.0)
        self.assertEqual(b["reviewer"], agents.DAILY_BUDGET_USD["reviewer"])
        with self.assertRaises(ValueError):
            agents.parse_budgets("bogus=5", agents.DAILY_BUDGET_USD)


class ParseResult(unittest.TestCase):
    def test_single_object(self):
        self.assertEqual(agents.parse_result('{"subtype": "success", "result": "hi"}')["result"], "hi")

    def test_list_of_messages_takes_last_result(self):
        out = json.dumps([{"type": "system"}, {"type": "result", "result": "a"},
                          {"type": "assistant"}, {"type": "result", "result": "b"}])
        self.assertEqual(agents.parse_result(out)["result"], "b")

    def test_garbage_never_raises(self):
        for bad in ("", "not json", "[1, 2]", "42", None):
            self.assertEqual(agents.parse_result(bad), {})


class Roles(unittest.TestCase):
    def test_every_role_has_schedule_and_timeout(self):
        for r in agents.ROLES:
            self.assertIn(r, agents.DEFAULT_NEXT)
            self.assertIn(r, agents.PASS_TIMEOUT)

    def test_explorer_gets_its_own_model(self):
        self.assertEqual(agents.ROLE_MODEL["explorer"], "claude-fable-5-2")
        self.assertGreater(agents.PASS_TIMEOUT["explorer"], agents.PASS_TIMEOUT["author"])

    def test_reviewer_is_woken_by_pr_changing_roles_only(self):
        self.assertIn("author", agents.CHANGES_PRS)
        self.assertIn("explorer", agents.CHANGES_PRS)
        self.assertNotIn("reviewer", agents.CHANGES_PRS)


class WaitUntil(unittest.TestCase):
    def fake(self):
        import threading, types
        return types.SimpleNamespace(stop=threading.Event(), wake={"author": threading.Event()})

    def test_returns_at_once_for_a_past_time(self):
        f = self.fake()
        agents.Supervisor.wait_until(f, "author", dt.datetime.now() - dt.timedelta(hours=3))

    def test_a_wake_ends_the_wait_and_is_cleared(self):
        f = self.fake()
        f.wake["author"].set()
        agents.Supervisor.wait_until(f, "author", dt.datetime.now() + dt.timedelta(hours=3))
        self.assertFalse(f.wake["author"].is_set())

    def test_steps_are_short_so_sleep_cannot_delay_a_pass_for_long(self):
        self.assertLessEqual(agents.WAIT_STEP, 120)


class Slug(unittest.TestCase):
    def test_https_and_ssh_with_and_without_git_suffix(self):
        for url in ("https://github.com/o/r.git", "https://github.com/o/r", "https://github.com/o/r/\n",
                    "git@github.com:o/r.git", "git@github.com:o/r", "ssh://git@github.com/o/r.git",
                    "https://user@github.com/o/r.git"):
            self.assertEqual(agents.parse_slug(url), "o/r", url)

    def test_dots_and_dashes_in_names(self):
        self.assertEqual(agents.parse_slug("git@github.com:my-org/proofs.v2.git"), "my-org/proofs.v2")

    def test_garbage_is_none(self):
        for bad in ("", None, "not a url", "https://gitlab.com/o/r.git", "https://github.com/o",
                    "error: No such remote 'origin'"):
            self.assertIsNone(agents.parse_slug(bad), bad)

    def test_no_hardcoded_repo_in_supervisor(self):
        src = (Path(__file__).resolve().parent / "agents.py").read_text(encoding="utf-8")
        self.assertNotIn("ndesmo", src)
        self.assertNotIn("leaning", src)


class Doctor(unittest.TestCase):
    ALL = {"git", "gh", "lake", "pwsh"}

    def run_checks(self, present=ALL, push="true", auth=0, claude="/bin/claude", slug="o/r"):
        def runner(cmd):
            if cmd[:3] == ["gh", "auth", "status"]:
                return types.SimpleNamespace(returncode=auth, stdout="")
            return types.SimpleNamespace(returncode=0, stdout=push + "\n")
        which = lambda name: f"/bin/{name}" if name in present else None
        return {name: level for level, name, _ in
                agents.doctor_checks(which, runner, py=(3, 11), claude=claude, slug=slug)}

    def test_all_present(self):
        c = self.run_checks()
        self.assertTrue(all(v == "OK" for v in c.values()), c)
        self.assertIn("push access", c)

    def test_missing_gh_is_hard(self):
        c = self.run_checks(present=self.ALL - {"gh"})
        self.assertEqual(c["gh"], "MISSING")
        self.assertNotIn("push access", c)   # cannot be checked without gh

    def test_missing_pwsh_is_only_a_warning(self):
        c = self.run_checks(present=self.ALL - {"pwsh"})
        self.assertEqual(c["pwsh"], "WARN")
        self.assertNotIn("MISSING", c.values())

    def test_no_push_access_warns(self):
        self.assertEqual(self.run_checks(push="false")["push access"], "WARN")

    def test_hard_failures(self):
        self.assertEqual(self.run_checks(auth=1)["gh auth"], "MISSING")
        self.assertEqual(self.run_checks(claude=None)["claude"], "MISSING")
        self.assertEqual(self.run_checks(slug=None)["origin"], "MISSING")
        self.assertEqual(self.run_checks(present=self.ALL - {"lake"})["lean"], "MISSING")
        which = lambda n: f"/bin/{n}"
        r = lambda cmd: types.SimpleNamespace(returncode=0, stdout="true")
        old = dict((n, l) for l, n, _ in agents.doctor_checks(which, r, py=(3, 8), claude="c", slug="o/r"))
        self.assertEqual(old["python"], "MISSING")


class Teardown(unittest.TestCase):
    def test_dirty_tree_is_refused(self):
        self.assertIn("uncommitted", agents.teardown_refusal(" M foo.lean\n", "", ""))

    def test_unpushed_commits_are_refused(self):
        why = agents.teardown_refusal("", "agent/x\n", "abc123 wip\n")
        self.assertIn("agent/x", why)
        self.assertIn("abc123 wip", why)

    def test_commits_on_a_detached_head_are_refused(self):
        why = agents.teardown_refusal("", "", "def456 local fix\n")
        self.assertIn("detached HEAD", why)

    def test_clean_is_allowed(self):
        self.assertIsNone(agents.teardown_refusal("", "", ""))           # detached at origin/main
        self.assertIsNone(agents.teardown_refusal("", "agent/x", ""))    # branch fully pushed


class Board(unittest.TestCase):
    def test_status_mapping(self):
        self.assertEqual(agents.board_status("pr", "MERGED"), "Done")
        self.assertEqual(agents.board_status("pr", "CLOSED"), "Done")
        self.assertEqual(agents.board_status("pr", "OPEN"), "In Review")
        self.assertEqual(agents.board_status("issue", "CLOSED", ["in-progress"], ["a"]), "Done")
        self.assertEqual(agents.board_status("issue", "OPEN", ["in-progress"], []), "In Progress")
        self.assertEqual(agents.board_status("issue", "OPEN", [], ["someone"]), "In Progress")
        self.assertEqual(agents.board_status("issue", "OPEN", ["moonshot"], []), "Todo")

    def test_find_project(self):
        ps = [{"number": 3, "title": "Old proofs", "closed": True},
              {"number": 4, "title": "Groceries"},
              {"number": 1, "title": "Proofs by Claude"}]
        self.assertEqual(agents.find_project(ps, "myrepo")["number"], 1)
        self.assertEqual(agents.find_project([{"number": 2, "title": "MyRepo board"}], "myrepo")["number"], 2)
        self.assertIsNone(agents.find_project(ps[1:2], "myrepo"))


if __name__ == "__main__":
    unittest.main()

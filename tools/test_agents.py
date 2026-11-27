"""Tests for the decision logic in tools/agents.py.  Run: python -m unittest tools/test_agents.py"""
import datetime as dt
import json
import sys
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


if __name__ == "__main__":
    unittest.main()

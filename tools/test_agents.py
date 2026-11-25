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


if __name__ == "__main__":
    unittest.main()

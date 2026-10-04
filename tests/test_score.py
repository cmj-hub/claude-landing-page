#!/usr/bin/env python3
"""score.py prints one URL, one offer, and one action, or refuses a sitemap."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = "incomplete-json-probe"
GOOD = {
    "url": "https://example.com/desk",
    "offer": "A one-page desk that names the week's leak.",
    "action": "Read the page and reply with the one number you want next.",
}


def run(args, stdin=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "score.py"), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


def score(draft):
    result = run(["--stdin", "--json"], stdin=json.dumps(draft))
    return result.returncode, json.loads(result.stdout)


class ScorePage(unittest.TestCase):
    def test_good_draft_prints_three(self):
        result = run(["--file", str(ROOT / "examples" / "page-good.json")])
        self.assertEqual(result.returncode, 0)
        self.assertIn("url: https://example.com/desk", result.stdout)
        self.assertIn("offer: A one-page desk that names the week's leak.", result.stdout)
        self.assertIn("action: Read the page and reply with the one number you want next.", result.stdout)
        self.assertNotIn("a sitemap", result.stdout)

    def test_sitemap_exits_1(self):
        result = run(["--file", str(ROOT / "examples" / "page-sitemap.json")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("a sitemap", result.stdout)
        self.assertNotIn("url:", result.stdout)

    def test_two_offers_example_fails(self):
        result = run(["--file", str(ROOT / "examples" / "page-two-offers.json")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("- offer is more than one sentence", result.stdout)

    def test_sitemap_shapes(self):
        for draft in (
            {**GOOD, "kind": "Sitemap"},
            {**GOOD, "pages": ["https://example.com/a"]},
            {**GOOD, "url": ["https://example.com/a", "https://example.com/b"]},
            {**GOOD, "url": "https://example.com/sitemap"},
            {**GOOD, "url": "https://example.com/pages.xml"},
        ):
            code, out = score(draft)
            self.assertEqual(code, 1, draft)
            self.assertTrue(out["sitemap"], draft)

    def test_url_problems(self):
        cases = {
            "http://example.com/desk": "url is not https",
            "example.com/desk": "url is not https",
            "https://example.com/a https://example.com/b": "url holds more than one address",
            "https:///desk": "url has no host",
            "": "url is missing",
        }
        for url, problem in cases.items():
            code, out = score({**GOOD, "url": url})
            self.assertEqual(code, 1, url)
            self.assertEqual(out["problems"], [problem], url)

    def test_second_offer_or_action_fails(self):
        for draft, problem in (
            ({**GOOD, "offer": ["one", "two"]}, "more than one offer"),
            ({**GOOD, "offers": ["two"]}, "more than one offer"),
            ({**GOOD, "action": ["Book", "Read"]}, "more than one action"),
            ({**GOOD, "ctas": ["Book a call"]}, "more than one action"),
            ({**GOOD, "action": "Book a call. Or download the guide."}, "action is more than one sentence"),
        ):
            code, out = score(draft)
            self.assertEqual(code, 1, draft)
            self.assertIn(problem, out["problems"], draft)

    def test_reports_every_problem(self):
        code, out = score({"url": "http://example.com"})
        self.assertEqual(code, 1)
        self.assertEqual(
            out["problems"], ["url is not https", "offer is missing", "action is missing"]
        )

    def test_long_offer_fails(self):
        code, out = score({**GOOD, "offer": "A desk " + "x" * 300})
        self.assertEqual(code, 1)
        self.assertIn("offer is longer than 200 characters", out["problems"])

    def test_abbreviation_is_one_sentence(self):
        code, out = score({**GOOD, "offer": "A desk for B2B teams, e.g. ops leads, at $4.50 a week."})
        self.assertEqual(code, 0, out)

    def test_json_output_on_pass(self):
        code, out = score(GOOD)
        self.assertEqual(code, 0)
        self.assertEqual(out, {"pass": True, "sitemap": False, "problems": [], **GOOD})

    def test_bad_json_hides_input(self):
        bad = run(["--stdin"], stdin='{"url": "' + CELL)
        self.assertEqual(bad.returncode, 2)
        self.assertNotIn(CELL, bad.stdout + bad.stderr)
        self.assertIn("invalid JSON", bad.stderr)
        array = run(["--stdin"], stdin='["' + CELL + '"]')
        self.assertEqual(array.returncode, 2)
        self.assertNotIn(CELL, array.stdout + array.stderr)
        self.assertIn("JSON must be an object", array.stderr)

    def test_missing_file_exits_2(self):
        result = run(["--file", str(ROOT / "examples" / "nope.json")])
        self.assertEqual(result.returncode, 2)
        self.assertIn("file not found", result.stderr)


if __name__ == "__main__":
    unittest.main()

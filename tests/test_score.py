#!/usr/bin/env python3
"""score.py prints one URL, one offer, and one action, or refuses a sitemap."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = "incomplete-json-probe"


def run(args, stdin=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "score.py"), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


class ScorePage(unittest.TestCase):
    def test_good_draft_prints_three(self):
        result = run(["--file", str(ROOT / "examples" / "page-good.json")])
        self.assertEqual(result.returncode, 0)
        self.assertIn("url: https://example.com/desk", result.stdout)
        self.assertIn("offer: A one-page desk that names the week's leak.", result.stdout)
        self.assertIn("action: Read the page and reply with the one number you want next.", result.stdout)
        self.assertIn("headline: A one-page desk that names the week's leak.", result.stdout)
        self.assertIn("section order: headline, proof, offer, action", result.stdout)
        self.assertIn("proof: Example, replace this: the page shows 1 leak", result.stdout)
        self.assertNotIn("a sitemap", result.stdout)

    def test_sitemap_exits_1(self):
        result = run(["--file", str(ROOT / "examples" / "page-sitemap.json")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("a sitemap", result.stdout)
        self.assertNotIn("url:", result.stdout)

    def test_bad_json_hides_input(self):
        bad = run(["--stdin"], stdin='{"url": "' + CELL)
        self.assertNotEqual(bad.returncode, 0)
        self.assertNotIn(CELL, bad.stdout + bad.stderr)
        self.assertIn("invalid JSON", bad.stderr)
        array = run(["--stdin"], stdin='["' + CELL + '"]')
        self.assertNotEqual(array.returncode, 0)
        self.assertNotIn(CELL, array.stdout + array.stderr)
        self.assertIn("JSON must be an object", array.stderr)

    def test_substance_order_proof_and_second_offer(self):
        import json
        good = {
            "url": "https://example.com/desk",
            "headline": "A one-page desk that names the week's leak.",
            "section_order": "offer, headline, proof, action",
            "proof": "Example, replace this: the page shows 1 leak before it asks for anything.",
            "offer": "A one-page desk that names the week's leak.",
            "action": "Read the page and reply with the one number you want next.",
        }
        wrong = run(["--stdin"], stdin=json.dumps(good))
        self.assertEqual(wrong.returncode, 1)
        self.assertEqual(wrong.stdout.strip(), "section order is wrong")
        good["section_order"] = "headline, proof, offer, action"
        good["proof"] = "The page shows 9 leaks."
        unlabeled = run(["--stdin"], stdin=json.dumps(good))
        self.assertEqual(unlabeled.returncode, 1)
        self.assertEqual(unlabeled.stdout.strip(), "proof number is not labeled example")
        good["proof"] = "Example, replace this: the page shows 1 leak before it asks for anything."
        good["headline"] = "Every address on the site, listed."
        missed = run(["--stdin"], stdin=json.dumps(good))
        self.assertEqual(missed.returncode, 1)
        self.assertEqual(missed.stdout.strip(), "headline does not name the offer")
        good["headline"] = "A one-page desk that names the week's leak."
        good["offer"] = "A desk that names the leak. A second workshop ships later."
        second = run(["--stdin"], stdin=json.dumps(good))
        self.assertEqual(second.returncode, 1)
        self.assertEqual(second.stdout.strip(), "a second offer")
        self.assertNotIn("url:", second.stdout)


if __name__ == "__main__":
    unittest.main()

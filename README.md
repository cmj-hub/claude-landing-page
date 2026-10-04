<p align="center">
  <img src="./assets/lockup.png" width="880" alt="Landing page skill for Claude Code. A landing page is one page, one offer, and one action.">
</p>

# Landing page skill for Claude Code

A landing page is one page, one offer, and one action.

The sample is a one-page desk that names the week's leak.

The good draft passes. A sitemap fails the score.

<p align="center">
  <img src="./assets/demo.gif" alt="Landing page skill — one page passes, a sitemap fails" width="100%">
</p>

The build guide teaches a human. The pack teaches an agent.

## Install

This pack is the files in this repository. Open the tree on the host you already run. There is no remote installer.

The scorer is Python in this repo. The skill calls it from its own folder, so it runs wherever the pack lands.

Run the tests:

```
python3 -m unittest discover -s tests
```

## What you walk out with in 15 minutes

Artifact: `examples/page-good.json`.

```
python3 scripts/score.py --file examples/page-good.json
python3 scripts/score.py --file examples/page-sitemap.json
```

```
python3 scripts/score.py --file examples/page-two-offers.json
```

The good draft exits 0 and prints the URL, the offer, and the action. The sitemap draft exits 1. The two-offer draft exits 1 and names the problem:

```
draft fails
- offer is more than one sentence
```

Then drop in yours. Every problem is listed at once, so one pass shows every fix. Add `--json` for machine-readable output.

## What the score checks

- `url` is one https address with a host. A list, two addresses, or a path that says sitemap fails.
- `offer` is one sentence, 200 characters or less. A list or an `offers` key fails.
- `action` is one sentence, 160 characters or less. A list, an `actions` key, or a `ctas` key fails.

Exit 0 passes. Exit 1 fails. Exit 2 means the input is unusable.

## What this pack will not do

It will not publish the page. It does not emit a sitemap. It will not list every URL on the site.

## What belongs on a landing page?

One page, one offer, and one action. A second offer, a second action, or a list of every URL on the site fails the score.

## Does this publish the page?

No. It scores the draft. You publish it.

## On the site

- [Landing page pack](https://jaymountconsulting.com/skills/claude-landing-page) — this pack's page
- [Skill packs catalog](https://jaymountconsulting.com/skills) — install paths + every pack

## Free, no signup

[All free tools](https://jaymountconsulting.com/prototypes)

## Free, by email

[**Growth Audit**](https://jaymountconsulting.com/growth-audit) — architecture gaps in the GTM you already run. Free written report.

[**Friday Signal**](https://jaymountconsulting.com/newsletter/signal) — one Friday GTM read. No pitch in it.

## Next

Previous: [Sales offer](https://github.com/cmj-hub/claude-sales-offer)

Next: [Generative engine optimization](https://github.com/cmj-hub/claude-geo)

## License

MIT. No paid APIs. Python 3 standard library only.

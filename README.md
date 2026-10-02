# Landing page skill for Claude Code

**A landing page is one page, one offer, and one action.**

You hold one URL, one offer, and one action. The scorer refuses a sitemap.

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![No paid APIs](https://img.shields.io/badge/paid%20APIs-none-success)

The build guide teaches a human. This pack teaches an agent.

## Install

```bash
npx skills add cmj-hub/claude-landing-page --all -g --full-depth
```

Installs into Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, and OpenCode. The scorer is Python in this repo. It does not call a paid API.

## What you walk out with in 15 minutes

Artifact: `examples/page-good.json`.

```bash
python3 scripts/score.py --file examples/page-good.json
python3 scripts/score.py --file examples/page-sitemap.json
```

The good draft exits 0 and prints the URL, the offer, and the action. The sitemap draft exits 1. Then drop in yours.

## What this pack will not do

It will not publish the page. It does not emit a sitemap. It will not list every URL on the site.

## What belongs on a landing page?

One page, one offer, and one action. A second offer, or a list of every URL on the site, fails the score.

## Does this publish the page?

No. It scores the draft. You publish it.

## Companion packs

- [claude-psp](https://github.com/cmj-hub/claude-psp) — Ideal customer profile
- [claude-evp](https://github.com/cmj-hub/claude-evp) — Value proposition
- [claude-cold-email](https://github.com/cmj-hub/claude-cold-email) — Cold email
- [claude-founder-brand](https://github.com/cmj-hub/claude-founder-brand) — LinkedIn posts
- [claude-pricing](https://github.com/cmj-hub/claude-pricing) — Pricing strategy
- [claude-geo](https://github.com/cmj-hub/claude-geo) — Generative engine optimization
- [claude-sales-offer](https://github.com/cmj-hub/claude-sales-offer) — Sales offer
- [claude-prospect-list](https://github.com/cmj-hub/claude-prospect-list) — Sales prospecting
- [claude-email-sequence](https://github.com/cmj-hub/claude-email-sequence) — Email sequence

## License

MIT. No paid APIs. Python 3 standard library only.

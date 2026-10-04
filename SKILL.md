---
name: page
description: "Draft one landing page as one https URL, one offer, and one action, then score it. Use when someone asks for a landing page, a single-offer page, or a page with one call to action. Refuses a sitemap or a list of pages."
when_to_use: "Trigger on: landing page, one-page offer, squeeze page, sign-up page, page with one CTA, score my landing page draft. Do not use for a site map, site navigation, a multi-page site, or publishing."
argument-hint: "[what the page offers]"
license: MIT
---

# The page

A page is one address. It states one offer. It asks for one action. A sitemap is a list of addresses. This pack refuses that list.

The build guide teaches a human. This pack teaches an agent.

## The three parts

1. URL. One https address for this page. Not a list of paths.
2. Offer. The thing the page puts in the reader's hands, in one sentence of 200 characters or less.
3. Action. The one thing the reader does on that page, in one sentence of 160 characters or less.

## How to write each part

- URL. Use the address the user gives. If they give none, ask for it. Do not invent a domain. `https://example.com/<slug>` is a placeholder only, and say so.
- Offer. Name the outcome the reader gets, not the company. One noun the reader holds, one result it gives them.
- Action. Start with a verb the reader does: book, reply, start, download, read. One verb phrase. "Book a call or download the guide" is two actions. Pick one.

If the user brings two offers, ask which one this page carries. The other one gets its own page.

## Checklist

Copy this list and tick it in order.

- [ ] 1. Name the one URL.
- [ ] 2. Write the draft to `draft.json`: `url`, `offer`, `action`.
- [ ] 3. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --file draft.json`.
- [ ] 4. Read each `- problem` line. Fix that field. Go back to step 3.

Stop when the script exits 0. Show the user the three printed lines.

## What the scorer refuses

| Output line | What it means | Fix |
| --- | --- | --- |
| `a sitemap` | `kind` is sitemap, a `urls` or `pages` list, a list in `url`, or a URL whose path says sitemap or ends in `.xml` | Keep one address. Drop the list. |
| `url is missing` / `url is not https` / `url has no host` | The address is absent or not a full https URL | Write `https://host/path`. |
| `url holds more than one address` | Two URLs in one field | Keep one. |
| `more than one offer` / `more than one action` | A list, or an `offers`, `actions`, or `ctas` key | Pick one. Move the other to its own page. |
| `offer is more than one sentence` / `action is more than one sentence` | A second sentence usually smuggles in a second offer or action | Cut to one sentence. |
| `... is longer than N characters` | The line does not fit in a headline or a button | Cut it. |

Exit 0 means the page passes. Exit 1 means it fails and each problem is listed. Exit 2 means the input is unusable: no file, not UTF-8, broken JSON, or not an object. A broken JSON does not echo the raw input.

## Run

```
python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --file ${CLAUDE_SKILL_DIR}/examples/page-good.json
python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --file ${CLAUDE_SKILL_DIR}/examples/page-sitemap.json
python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --file ${CLAUDE_SKILL_DIR}/examples/page-two-offers.json
```

Add `--json` to get one JSON object with `pass`, `sitemap`, `problems`, and the three fields.

Python 3 standard library only. No network. No publish.

## Example draft

```json
{
  "url": "https://example.com/desk",
  "offer": "A one-page desk that names the week's leak.",
  "action": "Read the page and reply with the one number you want next."
}
```

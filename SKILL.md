---
name: page
description: "Draft one page as one URL, one headline, one proof, one offer, and one action, in that order. Use when a landing page should hold a single address and a single next step, and when a sitemap or a second offer must be refused."
models: ""
---

# The page

A page is one address. It states one offer. It asks for one action. A sitemap is a list of addresses. This pack refuses that list.

No portal course owns this job. The skill still ships the page.

The build guide teaches a human. This pack teaches an agent.

You walk out with one page brief. The brief is the page, in order. The score file is that brief as JSON. A stranger can write it from this file alone.

This pack does not publish the page. It does not add a paid product. The public next steps already on the site are Friday Signal and the Growth Audit. They are not a second action on the page.

## Inputs

- The one https address for this page. Not a list of paths.
- The offer, in one sentence, in the reader's words. The thing the page puts in their hands.
- The one action. The one thing the reader does on that page.
- One proof the reader can check on that URL. If the proof uses a number, label it as an example and replace it. Do not invent a client result.

## Decision rules

The page has four sections, in this order, and no other order: headline, proof, offer, action. The URL is the address of the page. It is not a fifth section.

Headline. One sentence. It names the same offer as the offer line. It does not name a second offer. It does not contain a second address. It does not ask for the action. The action is the last section. If you use a number, the line must contain the word example.

Proof. One line the reader can check on that URL. A logo wall is not proof. A number is allowed only when the line contains the word example. Replace the number before you publish. The sample number is not a client result.

Offer. One sentence. One offer. A second sentence is a second offer, and it fails. Do not inventory the site.

Action. One sentence. One next step. "Read, then reply" is still one step when the reply is the point. A second ask fails the judgment. Do not add a paid product as the action.

URL. One address, `https://` or `http://`. A path that says sitemap is a sitemap. A `urls` list is a sitemap. A `kind` of sitemap is a sitemap.

Section order. The string is exactly `headline, proof, offer, action`.

## Procedure

1. Write the offer in one sentence.
2. Write the headline as one sentence that a reader could match to that offer. Do not put the action in the headline.
3. Write one proof line. If it needs a number, start from the sample shape: the word example, then the number, then replace the number.
4. Write the one action in one sentence.
5. Set `section_order` to `headline, proof, offer, action`.
6. Set `url` to the one address.
7. Save `draft.json`. From the repo root, run `python3 scripts/score.py --file draft.json`.

Exit 0 prints the six lines. Exit 1 prints one reason. Fix that line and run again.

## The brief

Write the brief in this shape, then score the JSON under it.

```
URL: one address
Headline: one sentence that names the offer
Proof: one line the reader can check
Offer: one sentence
Action: one sentence
Order: headline, proof, offer, action
```

## Score file

Six strings:

- `url`
- `headline`
- `section_order`
- `proof`
- `offer`
- `action`

## Filled example

Example only. Replace every line. `example.com` is not a client. The number in the proof is not a result. Replace it.

```json
{
  "url": "https://example.com/desk",
  "headline": "A one-page desk that names the week's leak.",
  "section_order": "headline, proof, offer, action",
  "proof": "Example, replace this: the page shows 1 leak before it asks for anything.",
  "offer": "A one-page desk that names the week's leak.",
  "action": "Read the page and reply with the one number you want next."
}
```

The page that object describes:

URL: `https://example.com/desk`

Headline: A one-page desk that names the week's leak.

Proof: Example, replace this: the page shows 1 leak before it asks for anything.

Offer: A one-page desk that names the week's leak.

Action: Read the page and reply with the one number you want next.

## What the scorer refuses

A sitemap. A sitemap is a `kind` of sitemap, a `urls` list, or a URL whose path says sitemap.

A second offer. A second offer is an `offers` list, or an offer line with more than one sentence.

These lines also fail a non-empty draft:

- `draft is incomplete` — a string is blank, or the URL is not an address.
- `section order is wrong` — the order is not headline, proof, offer, action.
- `headline is not one line` — the headline is not one sentence.
- `headline does not name the offer` — the headline and the offer do not share the offer's words.
- `proof number is not labeled example` — the proof has a digit and does not say example.
- `headline number is not labeled example` — the headline has a digit and does not say example.
- `action is not one line` — the action is not one sentence.

## Checklist

Copy this list and tick it in order.

- [ ] 1. Name the one URL.
- [ ] 2. Write the brief in order: headline, proof, offer, action. Copy that order into `section_order`.
- [ ] 3. From the repo root, run `python3 scripts/score.py --file draft.json`.

Check again until the script exits 0.

Go back to step 2 if step 3 fails.

## Run

```
python3 scripts/score.py --file examples/page-good.json
python3 scripts/score.py --file examples/page-sitemap.json
```

The good file exits 0 and prints the URL, the headline, the section order, the proof, the offer, and the action. The sitemap file exits 1.

A broken JSON exits non-zero and does not echo the raw input.

Python 3 standard library only. No network. No publish.

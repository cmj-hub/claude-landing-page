# Changelog

## 0.4.0

- Scorer checks what the docs promise: one https URL with a host, one
  offer, one action. A list, an `offers` / `actions` / `ctas` key, or a
  second sentence fails.
- Offer is capped at 200 characters and action at 160.
- A failing draft lists every problem, one per line, after `draft fails`.
- `--json` prints one result object.
- Sitemap detection also catches a `pages` list, a list in `url`, and
  `.xml` paths.
- Unusable input (missing file, broken JSON, not an object) exits 2.
- New example: `examples/page-two-offers.json`.
- `SKILL.md` calls the scorer through `${CLAUDE_SKILL_DIR}` so it runs
  from an installed plugin, adds trigger phrases and writing rules, and
  drops the invalid `models` field.
- `plugin.json` adds `repository` and `keywords`.
- Tests run in GitHub Actions.

## 0.3.0

- Plugin icon and manifest.

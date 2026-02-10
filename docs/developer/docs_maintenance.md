# Documentation Maintenance

This repository is intended as the single source of operational + analysis documentation.

## Update triggers

Update docs when any of the following changes:
- server IP/role changes
- worker populate calls change
- ingest GUI flow changes
- notebook catalog changes
- repo split conventions change
- backup script behavior changes

## Mandatory pages to update by change type

### Server / infra changes

Update:
- `infrastructure/architecture.md`
- `infrastructure/worker_population.md`
- `infrastructure/backups.md`
- `common/servers_access.md`

### Ingest workflow changes

Update:
- `ingest/overview.md`
- `ingest/gui_workflow.md`
- `ingest/modalities.md`
- `ingest/notebook_map.md`

### Analysis workflow changes

Update:
- `analysis/overview.md`
- `analysis/notebook_map.md`
- `analysis/query_patterns.md`

## Local docs build check

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-docs.txt
sphinx-build -b html docs docs/_build/html
```

Resolve warnings before merge when possible.

## Style guidance

- write for advanced beginners first
- keep command snippets copy-paste runnable
- separate policy vs implementation detail
- include operational caveats explicitly
- avoid hidden assumptions about setup names and paths

## Versioning note

Add date-stamped notes when documenting operational state snapshots.
Example:
- "Documented state as of 2026-02-10"

## Cross-repo sync practice

When split repo READMEs change materially, reflect key updates here.
Suggested cadence:
- review `adamacs_ingest/README.md` and `adamacs_analysis/README.md` at least monthly
- align notebook maps each release cycle

## Integrating informal ops notes safely

Informal sources (for example chat exports, Slack summaries, SOP scratch notes) are often operationally important.

When integrating them:
1. extract stable policy and workflow details
2. remove personal credentials, passwords, and private identifiers
3. avoid embedding screenshots with personal account names
4. cross-check against code/SOP scripts before publishing as canonical docs

If a source is not machine-readable in CI/headless tooling (for example JS-only share pages), keep a short note in commit/PR context and continue integrating all verifiable content from accessible sources.

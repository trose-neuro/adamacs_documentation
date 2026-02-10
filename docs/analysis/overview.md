# Analysis Overview

`adamacs_analysis` is the student-facing analysis workspace split from ingest operations.

## Analysis philosophy

- Keep ingest/pipeline mutation in `adamacs_ingest`.
- Keep analysis logic, figures, and project interpretation in `adamacs_analysis`.
- Fork `adamacs_analysis` for project-specific work and open PRs for reusable improvements.

## What lives in analysis repository

- starter notebooks for querying and plotting
- personal/project notebook workspaces
- analysis helper modules
- schema-class scaffold generator (`adamacs-analysis-generate`)

## Typical analysis flow

1. Start from proven keys (`subject`, `session_id`, `scan_id`).
2. Join incrementally across schema domains.
3. Validate counts and key uniqueness at each join.
4. Restrict by `paramset_idx` and `curation_id` explicitly.
5. Extract DataFrames/arrays only when key logic is correct.
6. Persist derived analysis artifacts with clear provenance.

## Recommended first notebook sequence

1. `01_querying_guide.ipynb`
2. `02_querying_template.ipynb`
3. modality-specific notebook (for example gaze or behavioral summary)

## Analysis and worker interaction

Analysis assumes ingest and worker-managed populations are complete.
If expected tables are empty, check worker status and upstream task completion before debugging analysis code.

## Reproducibility expectations

For every analysis figure/table, preserve:
- key restriction definitions
- table versions (`paramset_idx`, `curation_id`, model_name)
- commit hash of analysis code
- environment metadata (`pip freeze` or lockfile)

## Related pages

- `Analysis -> Database Structure`
- `Analysis -> Schema Chapters (User-Focused)`
- `Analysis -> Notebook Map`
- `Analysis -> Query Patterns`
- `Analysis -> Schema Scaffolding`
- `Infrastructure -> Worker-Owned Population`

# Repository Split Model

This page explains the ADAMACS split-repo architecture and the intended collaboration model.

## Goal of the split

- keep ingest operations stable and centrally managed
- make analysis work easy to fork and iterate
- reduce accidental operational breakage from analysis-side experimentation

## Repositories and responsibilities

## `adamacs_ingest`

Primary responsibilities:
- ingest GUI and ingest helper logic
- schema and pipeline activation
- task-table staging logic
- operational notebooks and batch ingest templates

Collaboration model:
- students should use upstream directly for routine ingest
- no default requirement to fork for day-to-day use
- propose operational improvements via focused PRs to main repository

## `adamacs_analysis`

Primary responsibilities:
- student/project analysis notebooks
- query helpers and plotting utilities
- analysis schema scaffolding and reusable analysis modules

Collaboration model:
- students can fork freely
- use feature branches for project-specific analyses
- upstream PRs for reusable patterns/helpers

## Legacy `adamacs` monorepo

Used as historical reference and compatibility source.
Most day-to-day new development should follow split repos.

## Data flow and ownership

```{mermaid}
flowchart LR
    ING[adamacs_ingest] --> DB[DataJoint and workers]
    DB --> ANA[adamacs_analysis]
    ANA --> PR[analysis PRs]
    ING --> OPR[operational PRs]
```

## What goes where

Put code in `adamacs_ingest` if it:
- changes ingest parsing
- changes table/task insertion behavior
- affects worker-run population logic

Put code in `adamacs_analysis` if it:
- computes derived metrics for studies
- adds exploratory visualizations
- adds reusable analysis-side helper APIs

## Decision rule

If a change can break ingest or worker operations, it belongs to ingest repo with stricter review.
If a change mainly supports analysis interpretation and can be sandboxed, it belongs to analysis repo.


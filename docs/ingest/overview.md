# Ingest Overview

`adamacs_ingest` is the central operational entrypoint for data onboarding into ADAMACS.

## Core principle

Students should ingest metadata and create tasks.
Workers should perform most heavy populations.

This prevents:
- duplicate compute
- filesystem permission collisions on blob-backed outputs
- inconsistent ownership of long-running jobs

## High-level ingest flow

```{mermaid}
flowchart LR
    A[Acquisition setup output] --> B[Consolidated session folder]
    B --> C[Upload to TATCHU share]
    C --> D[Ingest GUI or ingest notebook]
    D --> E[Session and scan metadata tables]
    D --> F[*Task tables]
    F --> G[Server workers populate]
    G --> H[Computed tables and file blobs]
    H --> I[Analysis notebooks]
```

## What lives in ingest repository

- DataJoint pipeline activation (`adamacs/pipeline.py`)
- schema declarations (`adamacs/schemas/*`)
- ingest logic (`adamacs/ingest/*`)
- ingest GUI (`adamacs.gui.select_sessions`)
- ingest and operator notebooks
- batch ingest templates

## Ingest source directory conventions

Configured via:
- `custom.imaging_root_data_dir`
- `custom.exp_root_data_dir`
- `custom.dlc_root_data_dir`

Typical lab path:
- `/datajoint-data/data/<username>`

## Rule of thumb for populations

- If a workflow has a `*Task` table, insert the task and let workers pick it up.
- Run manual populations primarily for lightweight ingest-side computed tables.

Detailed ownership table:
- `Infrastructure -> Worker-Owned Population`

## First practical steps

1. Confirm `dj_local_conf.json` paths and credentials.
2. Open ingest GUI workflow notebook.
3. Select sessions and verify parsed session/scan IDs.
4. Commit ingest metadata and tasks.
5. Monitor worker completion.
6. Hand off to analysis.

## Related pages

- `Ingest -> GUI Workflow`
- `Ingest -> Batch Ingest`
- `Ingest -> Modalities`
- `Infrastructure -> Permissions and Ownership`

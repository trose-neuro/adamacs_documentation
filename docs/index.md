# Welcome to ADAMACS documentation

This site is the operational and analysis manual for the ADAMACS ecosystem:
- `adamacs_ingest`: ingest + population workflows
- `adamacs_analysis`: analysis + notebook workflows
- lab infrastructure around DataJoint, worker processes, blob storage, and backups

The structure below follows a multi-section documentation pattern similar to mature pipeline docs (separate common, workflow, and developer tracks).

```{toctree}
:maxdepth: 2
:caption: Common

common/getting_started
common/database_philosophy
common/lab_operations_playbook
common/environment_setup
common/dj_local_conf
common/servers_access
common/troubleshooting
common/glossary
```

```{toctree}
:maxdepth: 2
:caption: Ingest

ingest/overview
ingest/gui_workflow
ingest/batch_ingest
ingest/modalities
ingest/notebook_map
```

```{toctree}
:maxdepth: 2
:caption: Analysis

analysis/overview
analysis/notebook_map
analysis/query_patterns
analysis/schema_scaffolding
analysis/gaze_pose_imaging
```

```{toctree}
:maxdepth: 2
:caption: Infrastructure

infrastructure/architecture
infrastructure/worker_population
infrastructure/backups
infrastructure/permissions
infrastructure/slack_post_template
```

```{toctree}
:maxdepth: 2
:caption: Developer Documentation

developer/repo_split
developer/deploy_private_repository
developer/contributing
developer/docs_maintenance
```

## Intended audiences

- Students: start with `Common -> Getting Started`, then `Ingest -> GUI workflow` and `Analysis -> overview`.
- Advanced analysts: start with `Analysis -> query patterns` and `Infrastructure -> worker population`.
- Operators/admins: start with `Infrastructure` and `Developer Documentation`.

## Current infra snapshot (as documented)

- `MAIN_SERVER`: `172.25.64.3` (main DB/blob/share/CPU workers)
- `GPU_SERVER`: `172.25.70.3` (GPU worker host, permanent IP)
- `BACKUP_SERVER`: `172.26.65.8` (backup host)

If this changes, update infrastructure pages first.

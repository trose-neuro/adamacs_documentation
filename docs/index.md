# Welcome to ADAMACS documentation

This site is the operational and analysis manual for ADAMACS.
Use the section hubs below for fast navigation.

```{toctree}
:maxdepth: 2
:caption: Common

common/overview
```

```{toctree}
:maxdepth: 2
:caption: Ingest

ingest/overview
```

```{toctree}
:maxdepth: 2
:caption: Analysis

analysis/overview
```

```{toctree}
:maxdepth: 2
:caption: Infrastructure

infrastructure/overview
```

```{toctree}
:maxdepth: 2
:caption: Developer Documentation

developer/overview
```

## Quick paths

- New users: `Common -> Getting Started`
- Ingest users: `Ingest -> GUI Workflow`
- Analysis users: `Analysis -> Overview`
- Operators/admins: `Infrastructure -> Overview`

## Current infra snapshot (as documented)

- `MAIN_SERVER`: `172.25.64.3` (main DB/blob/share/CPU workers)
- `GPU_SERVER`: `172.25.70.3` (GPU worker host, permanent IP)
- `BACKUP_SERVER`: `172.26.65.8` (backup host)

If this changes, update infrastructure pages first.

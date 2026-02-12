# Welcome to ADAMACS documentation

This site is the operational and analysis manual for ADAMACS.
Use the section hubs below for fast navigation.
ADAMACS is informed by the Moser pipeline lineage, but all pages here use ADAMACS-specific terminology and workflows.

<div class="landing-hero">
  <a class="troselab-link" href="https://www.troselab.de" target="_blank" rel="noopener noreferrer">
    visit Troselab: www.troselab.de
  </a>
  <div class="hero-carousel" aria-label="Decorative Troselab microscopy banner">
    <img class="hero-slide hero-slide-1" src="_static/branding/troselab-banner.jpg" alt="Troselab banner microscopy collage"/>
    <img class="hero-slide hero-slide-2" src="_static/branding/troselab-logo.jpg" alt="Troselab logo panel"/>
    <img class="hero-slide hero-slide-3" src="_static/branding/troselab-g2.jpg" alt="Troselab decorative microscopy panel"/>
  </div>
</div>

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
- External component docs: `Common -> External References`
- Ingest users: `Ingest -> GUI Workflow`
- Analysis users: `Analysis -> Overview`
- Operators/admins: `Infrastructure -> Overview`

## Current infra snapshot (as documented)

- `MAIN_SERVER`: `<MAIN_SERVER_IP>` (main DB/blob/share/CPU workers)
- `GPU_SERVER`: `<GPU_SERVER_IP>` (GPU worker host, permanent IP)
- `BACKUP_SERVER`: `<BACKUP_SERVER_IP>` (backup host)

Note:
- internal endpoint values are intentionally redacted in public documentation.

If this changes, update infrastructure pages first.

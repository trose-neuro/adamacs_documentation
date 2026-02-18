# Getting Started

This page is the shortest path from zero setup to first successful ingest + first analysis query.

## 1. Clone repositories side-by-side

ADAMACS is used as two repos:
- `adamacs_ingest` (ingest/task staging) - CLONE
- `adamacs_analysis` (querying/analysis notebooks) - FORK



```bash
cd /path/to/workspace
git clone https://github.com/SFB1089/adamacs_ingest.git
git clone https://github.com/YOUR-FORK/adamacs_analysis.git
```

or (likely) when using ssh access:

```bash
cd /path/to/workspace
git clone git@github.com:SFB1089/adamacs_ingest.git
git clone git@github.com:YOUR-FORK/adamacs_analysis.git
```

## 2. Install environment

Recommended:

```bash
cd /path/to/workspace/adamacs_analysis
./scripts/install_datajoint_analysis.sh
```

For detailed install options, use `Common -> Environment Setup`.

## 3. Create local DataJoint config

Create local config files:

```bash
cd /path/to/workspace/adamacs_ingest
cp Example_dj_local_conf.json dj_local_conf.json

cd /path/to/workspace/adamacs_analysis
cp Example_dj_local_conf.json dj_local_conf.json
```

Then set host/user/password/path values for your account.
Reference: `Common -> dj_local_conf`.

## 4. Verify DB connection

In your configured environment:

```python
import datajoint as dj
dj.conn()
print("Connected")
```

If this fails: `Common -> Troubleshooting`.

## 5. Do first ingest + first analysis check

First ingest:

```python
from adamacs.gui import select_sessions
select_sessions(["XX_ANM-0000_2026-01-01_sessXXXX_scanXXXX"])
```

Then open analysis notebook:
- `adamacs_analysis/notebooks/01_querying_guide.ipynb`

## Workflow rules

- Stage ingest/task rows from GUI.
- Let workers run heavy populations.
- Analyze in `adamacs_analysis`.

## What to read next

- `Ingest -> Overview`
- `Ingest -> GUI Workflow`
- `Analysis -> Overview`
- `Infrastructure -> Worker-Owned Population`

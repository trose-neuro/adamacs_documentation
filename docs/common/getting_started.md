# Getting Started

This page gives you the shortest reliable path from zero setup to productive ingest + analysis work.

## 1) Understand the repository split

ADAMACS is now best used as two working repositories:

- `adamacs_ingest`
  - ingest-first repository
  - pipeline definitions, ingest code, task insertion, GUI, batch ingest templates
- `adamacs_analysis`
  - analysis-first student repository
  - querying, plotting, exploratory notebooks, analysis helper code

Operationally:
- ingest and heavy population tasks are centered in `adamacs_ingest`
- project-specific analysis should mostly happen in `adamacs_analysis` (easy to fork)
- students should normally use `adamacs_ingest` directly (no mandatory fork) and contribute improvements via PRs to main

## 2) Clone repos side-by-side

```bash
cd /path/to/workspace
git clone https://github.com/your-org/adamacs_ingest.git
git clone https://github.com/your-org/adamacs_analysis.git
```

(If your organization host differs, replace remotes accordingly.)

## 3) Install the analysis environment (recommended first)

From `adamacs_analysis`:

```bash
./scripts/install_datajoint_analysis.sh
```

This installs a pinned DataJoint pre-2.0 stack and installs both repos in editable mode.

## 4) Configure local DataJoint credentials

Create local, untracked config files (details in `dj_local_conf` page):

```bash
cd /path/to/workspace/adamacs_ingest
cp Example_dj_local_conf.json dj_local_conf.json

cd /path/to/workspace/adamacs_analysis
cp Example_dj_local_conf.json dj_local_conf.json
```

Edit host/user/password/path fields for your account.

## 5) First connection test

In any Python shell (inside your configured environment):

```python
import datajoint as dj

dj.conn()
print("Connected")
```

If this fails, go directly to `Common -> Troubleshooting`.

## 6) First ingest run

Use the ingest GUI entrypoint:

```python
from adamacs.gui import select_sessions

select_sessions(["XX_ANM-0000_2026-01-01_sessXXXX_scanXXXX"])
```

You will normally:
- ingest metadata and insert task rows
- let workers pick up heavy jobs

## 7) First analysis run

From `adamacs_analysis`, open notebook:
- `notebooks/01_querying_guide.ipynb`

Then validate a simple query (for example by subject/session filter) before scaling up.

## Standard student workflow

1. Upload/consolidate data to server share.
2. Use ingest GUI to register sessions/scans and create task rows.
3. Wait for worker-managed heavy populations.
4. Analyze results in `adamacs_analysis` notebooks.
5. Commit analysis code in your branch/fork and open PR.

## What to read next

- `Common -> Environment Setup`
- `Ingest -> GUI Workflow`
- `Infrastructure -> Worker-Owned Population`
- `Analysis -> Overview`

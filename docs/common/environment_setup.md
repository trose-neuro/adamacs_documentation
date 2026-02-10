# Environment Setup

This page documents the practical, reproducible environment setup for ADAMACS ingest and analysis.

## Recommended strategy

Use the provided installer scripts from split repositories:
- `adamacs_ingest/scripts/install_datajoint_ingest.sh`
- `adamacs_analysis/scripts/install_datajoint_analysis.sh`

These scripts pin versions and run compatibility handling that is easy to miss in manual installs.

## Option A: Install `adamacs_analysis` stack (most students)

```bash
cd /path/to/workspace/adamacs_analysis
./scripts/install_datajoint_analysis.sh
```

Optional custom env + explicit ingest path:

```bash
./scripts/install_datajoint_analysis.sh my_analysis_env /absolute/path/to/adamacs_ingest
```

## Option B: Install ingest-only stack

```bash
cd /path/to/workspace/adamacs_ingest
./scripts/install_datajoint_ingest.sh
```

Optional env name:

```bash
./scripts/install_datajoint_ingest.sh my_ingest_env
```

## Manual baseline (if script not usable)

The current stack in split repos is Python 3.11 + pinned DataJoint pre-2.0 dependencies.

Example manual pattern:

```bash
conda create -n datajoint_analysis python=3.11 -y
conda install -n datajoint_analysis -y graphviz
conda run -n datajoint_analysis python -m pip install --upgrade pip wheel "setuptools<81"
conda run -n datajoint_analysis python -m pip install -r requirements_datajoint.txt
conda run -n datajoint_analysis python -m pip install -e ../adamacs_ingest
conda run -n datajoint_analysis python -m pip install -e ".[notebooks]"
```

## Optional compatibility packages

In some environments you may need:

```bash
python -m pip install --no-deps "pywavesurfer @ git+https://github.com/your-org/PyWaveSurfer.git"
python -m pip install scanimage-tiff-reader==1.4.1.4
```

If wheel build fails for `scanimage-tiff-reader`:

```bash
conda install -c conda-forge scanimage-tiff-reader
```

## Verify installation

```bash
python - <<'PY'
import datajoint as dj
print("DataJoint:", dj.__version__)
PY
```

Then test import paths:

```bash
python - <<'PY'
import adamacs
print("adamacs import ok")
PY
```

For analysis repo:

```bash
python - <<'PY'
import adamacs_analysis
print("adamacs_analysis import ok")
PY
```

## Local checks (recommended before PR)

```bash
python -m pip install pytest ruff
python -m ruff check --select E9,F63,F7,F82 adamacs tests
python -m pytest -q
```

(Use `adamacs_analysis` equivalents in that repo.)

## Common install pitfalls

- Mixed Python versions in env (must be what scripts expect).
- Missing Graphviz (`dj.Diagram` export breaks).
- Local config file missing or tracked accidentally.
- TLS handshake issue due to `database.use_tls` not set for non-TLS DB.

See `Common -> Troubleshooting`.

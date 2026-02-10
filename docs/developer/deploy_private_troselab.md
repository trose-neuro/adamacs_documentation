# Deploy To Private `troselab` Repository

This runbook publishes `adamacs_documentation` as a private repository and keeps it maintainable for lab operations.

## 1) Create private repository in GitHub org

1. In GitHub org `troselab`, create repository `adamacs_documentation`.
2. Set visibility to **Private**.
3. Do not initialize with default files if this local repo already exists.

## 2) Push local repository

From local repo root:

```bash
git remote add origin git@github.com:troselab/adamacs_documentation.git
git add .
git commit -m "Initial RTD documentation import"
git push -u origin main
```

If `origin` already exists, update it:

```bash
git remote set-url origin git@github.com:troselab/adamacs_documentation.git
```

## 3) Repository hardening

Recommended baseline:

1. Enable branch protection on `main`.
2. Require pull requests for direct changes.
3. Require status checks before merge.
4. Enable secret scanning and push protection.
5. Add CODEOWNERS for infra + ingest maintainers.

## 4) CI docs build (GitHub Actions)

Add a workflow to verify docs compile on every PR.

Suggested workflow name: `.github/workflows/docs-build.yml`

Key steps:
- setup Python
- install `requirements-docs.txt`
- run `sphinx-build -b html docs docs/_build/html`

Optional: upload `_build/html` as workflow artifact.

## 5) Private Read the Docs deployment

### Option A: Read the Docs with private project support

1. Connect GitHub account/org app in Read the Docs.
2. Import `troselab/adamacs_documentation`.
3. Confirm config file `.readthedocs.yaml` is detected.
4. Enable private documentation visibility.
5. Grant project access to lab members/groups.

### Option B: GitHub-only workflow

If private RTD is unavailable, keep docs in GitHub and use local builds or CI artifacts.

## 6) Required files already present

- `.readthedocs.yaml`
- `requirements-docs.txt`
- `docs/conf.py`

These should work for standard Sphinx + MyST + Mermaid builds.

## 7) Operational update cadence

When infra/process changes, update these pages together:
- `docs/infrastructure/architecture.md`
- `docs/infrastructure/worker_population.md`
- `docs/infrastructure/backups.md`
- `docs/common/servers_access.md`

## 8) Access model for lab users

Recommended role split:
- Students: read access + PR permissions via forks/branches.
- Operators/maintainers: write + merge rights.
- Infra maintainers: admin rights for secrets, CI, and release controls.

## 9) Publish URL in lab channels

After first successful deployment, share one canonical docs URL in lab channels and pin it.

Include link in:
- ingest onboarding message
- analysis onboarding message
- worker-policy announcement post

# Lab Operations Playbook

This page consolidates practical, day-to-day ADAMACS operating rules from internal lab notes and SOP scripts into one privacy-safe reference.

Scope:
- ingest and analysis operations
- worker ownership rules
- naming conventions and curation policy
- storage and access hygiene

Personal credentials, personal contact details, and private account specifics are intentionally omitted.

## Source basis

This playbook was cross-checked against:
- lab-provided workflow notes in this documentation project context
- repository code paths (`adamacs` ingest/helpers/schemas)
- `troselab/SOPs` server scripts and markdown references

Note:
- some external note-sharing links are JS-rendered and may not be machine-readable in headless fetch contexts; in that case, only verifiable content from accessible sources is promoted to canonical docs.

## 1) Core operating rule

Use `adamacs_ingest` as the central entry point.

- Students: ingest metadata, insert task rows, run lightweight populate where appropriate.
- Workers: execute heavy and blob-writing jobs.
- Analysis: primarily in `adamacs_analysis`.

Rule of thumb:
- If a `*Task` table exists, insert tasks and wait for workers.

## 2) Why permission errors happen

You can have valid SQL rights but still fail writes to blob storage on Linux filesystem paths.

Typical symptom:

```text
[Errno 13] Permission denied: /datajoint-db/blobs/.../*.saving
```

Interpretation:
- DB user rights are sufficient for table operations.
- OS user/group rights are insufficient for blob path writes.

Action:
- Do not force manual repopulation for worker-owned blob workflows.
- Verify whether worker queues already finished the key.

## 3) Student curation policy

Curation is mandatory for imaging outputs.

- First extraction is not final.
- Manual curation quality control is required before downstream analysis claims.
- Keep `curation_id` explicit in analysis filters and figures.

Versioning reminder:
- There can be multiple extraction/curation versions for the same session/scan.
- Always pin analysis to specific `curation_id` and parameter context.

## 4) DLC naming convention

Model naming in the database should use:

```text
SHORTHAND;PURPOSE;VIDEOKEY
```

Example:

```text
NK;TopTrackingNoScope;top_video*.mp4
```

This naming convention is important for reproducibility and unambiguous model selection.

## 5) CASCADE workflow policy

CASCADE inference is task-driven.

General flow:
1. Insert rows into `imaging.ActivityCascadeTask` with the desired curation/parameter pairing.
2. Worker listeners process queued tasks.
3. Results appear in imaging activity outputs (cascade inference path alongside standard deconvolution outputs, depending on active schema implementation).

Operationally, treat this as worker-owned compute unless explicitly instructed otherwise.

Environment synchronization note for CASCADE-enabled workflows:

```bash
pip uninstall element-calcium-imaging
pip install git+https://github.com/SFB1089/element-calcium-imaging.git@main
```

Also ensure local `adamacs` code is up to date before task insertion.

## 6) RSpace folder grammar (required for stable parsing)

Use a strict hierarchy for mouse-level experiment records:

```text
ROOT/
└── Experiments/
    ├── <INITIALS>_<MOUSEID>/
    │   ├── YYYY-MM-DD_<entry_type>
    │   ├── YYYY-MM-DD_<setup>_<session_token>
    │   └── ...
```

Examples:
- `TR_ROS-999/2022-12-12_craniotomy`
- `TR_ROS-999/2023-01-01_mini2p1_sessABC123`

Guideline:
- Date-bound entries should always use the date-prefixed format.
- Optional non-date summary documents can be included at mouse folder level when needed.

## 7) Storage and disk hygiene

- Store raw data under shared data roots, not in home directories.
- Keep environments lean (prefer Miniconda/minimal environments).
- Remove stale caches/environments regularly.
- Keep user home directories responsive and clean.

## 8) Access and security hygiene

- Prefer SSH keys over password-based workflows.
- Do not store plaintext passwords in notes or local text files.
- Keep API keys/tokens out of committed repository files.

## 9) Remote development practice

Remote coding can use:
- VS Code Remote SSH
- VS Code tunnel workflows (if configured by operators)

Typical tunnel CLI sequence on server:

```bash
curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz
tar -xf vscode_cli.tar.gz
./code tunnel
```

Reference:
- https://code.visualstudio.com/docs/remote/tunnels

## 10) Daily student checklist

1. Confirm local config and server reachability.
2. Upload/consolidate to shared ingest path.
3. Use ingest GUI or batch scripts to insert metadata + tasks.
4. Let workers process heavy queues.
5. Confirm completion for your keys.
6. Start analysis with explicit key restrictions (`session_id`, `scan_id`, `curation_id`, `paramset_idx`, `model_name`).

## Related pages

- `Infrastructure -> Worker-Owned Population`
- `Infrastructure -> Permissions and Ownership`
- `Infrastructure -> Architecture`
- `Ingest -> Overview`

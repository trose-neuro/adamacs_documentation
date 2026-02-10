# Batch Ingest

Batch ingest workflows are intended for repeated, multi-session onboarding without clicking each session manually.

## Where to find templates

In `adamacs_ingest`:
- `examples/batch_ingest/`
- ingest notebooks including camera/DLC/eye batch workflows

## Batch ingest design goals

- deterministic key parsing
- idempotent inserts (`skip_duplicates=True` patterns)
- clean separation between:
  - metadata insert
  - task insert
  - worker-managed populations

## Recommended pattern

1. Build a session manifest (CSV/DataFrame/list of folders).
2. Validate naming and path existence.
3. Insert/refresh metadata tables.
4. Insert relevant `*Task` rows only.
5. Let workers process heavy compute.
6. Export success/failure logs.

## Modalities to cover in batch routines

A complete ingest batch suite should include templates for:
- calcium imaging processing tasks
- DLC pose task insertion
- eye camera ingest + pupil tracking task preparation
- OptiTrack/mocap task insertion
- BPod + aux synchronization ingest
- denoising/cascade task insertion where applicable

## Example pseudocode skeleton

```python
for sess in session_manifest:
    ingest_session_metadata(sess)
    for scan in discover_scans(sess):
        ingest_scan_metadata(scan)
        insert_behavior_tasks(scan)
        insert_imaging_tasks(scan)
        insert_dlc_tasks(scan)
        insert_mocap_tasks(scan)
        insert_cascade_or_denoise_tasks(scan)
```

## Guardrails

- Use one modality batch script per concern when possible.
- Save structured logs (timestamp, key, action, status, traceback).
- Avoid calling heavy populate loops from student accounts in batch mode.

## Failure handling

For each failed key:
- keep batch moving (`suppress_errors=True` at orchestration layer)
- write traceback summary to log
- generate rerun list for failed keys only

## Batch ingest and worker interaction

Batch scripts should primarily stage tasks.
Dedicated workers on MAIN_SERVER/GPU_SERVER should execute compute.

## Related pages

- `Ingest -> Modalities`
- `Infrastructure -> Worker-Owned Population`
- `Common -> Troubleshooting`

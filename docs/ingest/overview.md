# Ingest Overview

`adamacs_ingest` is where you register new sessions and create processing tasks.

## Start here

Use `ingestgui_v2` first:
- notebook: `adamacs_ingest/notebooks/00_ingest_gui_workflow_adamacs_ingest_v2.ipynb`
- helper: `adamacs.helpers.adamacs_ingest_v2.select_sessions(...)`

## Golden rules

- Ingest metadata and insert tasks from the GUI.
- Keep `do_population=False` during normal user ingest.
- Let workers handle heavy compute tables.

## Typical flow

1. Confirm `dj_local_conf.json` paths and credentials.
2. Open `00_ingest_gui_workflow_adamacs_ingest_v2.ipynb`.
3. Select sessions in the GUI and check key fields.
4. Commit ingest metadata and tasks.
5. Verify task rows exist.
6. Continue in analysis notebooks.

## Path settings used by ingest

- `custom.exp_root_data_dir`
- `custom.imaging_root_data_dir`
- `custom.dlc_root_data_dir`

## Related pages

- `Ingest -> GUI Workflow`
- `Ingest -> Batch Ingest`
- `Infrastructure -> Worker-Owned Population`

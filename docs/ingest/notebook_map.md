# Ingest Notebook Map

Use this page to choose the right notebook quickly.

## Default choice

- `00_ingest_gui_workflow_adamacs_ingest_v2.ipynb`
  - default for almost all ingest runs
  - session discovery + GUI commit flow

## If you need more than the GUI

| Need | Notebook |
| --- | --- |
| Check pipeline/schema connectivity | `01_pipeline.ipynb` |
| Manual subject/session/scan insert | `02_manual_insert.ipynb`, `04_scan_insert.ipynb` |
| PyRAT import | `03_pyrat_insert.ipynb` |
| Imaging processing follow-up | `07_imaging_processing.ipynb` |
| Suite2p parameter work | `12_suite2p_parameters.ipynb` |
| DLC troubleshooting | `13_DLClive_ingest.ipynb`, `23_batch_dlc_eye_ingestion.ipynb` |
| Behavior/sync troubleshooting | `06_behavior_insert.ipynb`, `09_insert_bpod_harp.ipynb` |
| Server-side diagnostics | `99 ServerIngestDebug.ipynb` |

## Recommended order for new users

1. `00_ingest_gui_workflow_adamacs_ingest_v2.ipynb`
2. `01_pipeline.ipynb`
3. Only open modality-specific notebooks if the GUI run needs follow-up.

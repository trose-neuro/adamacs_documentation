# Ingest Notebook Map

This map is based on current notebook inventory in the ingest-oriented codebase and legacy monorepo references.

## Core onboarding notebooks

- `01_pipeline.ipynb`
  - pipeline initialization and schema visibility
- `02_manual_insert.ipynb`
  - manual subject/session/scan insertion primitives
- `03_pyrat_insert.ipynb`
  - PyRAT subject ingest
- `04_scan_insert.ipynb`
  - session and scan ingestion

## Imaging and processing notebooks

- `07_imaging_processing.ipynb`
  - suite2p processing task and computed table progression
- `12_suite2p_parameters.ipynb`
  - parameter set definitions and adjustment
- `15_imaging denoising pipeline.ipynb`
  - denoising workflow
- `16_imaging cascade pipeline.ipynb`
  - cascade inference workflow

## Behavior and synchronization notebooks

- `06_behavior_insert.ipynb`
  - behavior ingestion foundations
- `09_insert_bpod_harp.ipynb`
  - BPod + HARP synchronization paths
- `20_manual_step_by_step_ingest_bpod_trial.ipynb`
  - trial-level ingest checks/debugging
- `debug_bpod_timeout_ingestion.ipynb`
  - timeout-specific debugging

## DLC and camera ingest notebooks

- `05_DeepLabCut model insert.ipynb`
- `05_DeepLabCut.ipynb`
- `13_DLClive_ingest.ipynb`
- `21_batch_camera_ingest.ipynb`
- `23_batch_dlc_eye_ingestion.ipynb`

## Eye tracking and gaze notebooks

- `14_pupil_tracking_ingestion.ipynb`
- `19_eyecam_ingest.ipynb`
- `19_2_eyecam_ingest.ipynb`
- `22_blender_gaze_render.ipynb`
- `25_Optitrack_RigidMouse_and_Gaze_Repopulation.ipynb`
- `26_arena_slam_gaze_reconstruction_draft.ipynb`
- `27_slam_worldcam_minimal.ipynb`

## Mocap / OptiTrack notebooks

- `17_optitrack_insert.ipynb`
- `25_Optitrack_RigidMouse_and_Gaze_Repopulation.ipynb`

## Batch and server debug notebooks

- `10_troselab_workflow.ipynb`
  - integrated ingest workflow
- `99 ServerIngestDebug.ipynb`
  - server-side ingest diagnostics

## User/project notebooks (selected)

Examples: `66_*`, `67_*` notebooks are user/project-specific and can contain mixed ingest/analysis logic.
Treat them as references, not authoritative ingest SOP.

## Recommended starting sequence

1. `01_pipeline.ipynb`
2. `03_pyrat_insert.ipynb`
3. `04_scan_insert.ipynb`
4. `10_troselab_workflow.ipynb`
5. modality-specific notebook from sections above

## Curation note

Notebooks evolve quickly; maintain an internal short list of lab-approved canonical notebooks for each semester cohort.

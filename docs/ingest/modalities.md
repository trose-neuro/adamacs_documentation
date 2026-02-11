# Ingest Modalities

This page maps each major modality to its ingest path, staging tables, and downstream worker behavior.

## 1) Calcium imaging (ScanImage + suite2p)

### Inputs
- scan folders with TIFF files and ScanImage header metadata

### Typical ingest path
1. Insert/refresh session and scan metadata.
2. Populate `scan.ScanInfo`.
3. Insert `imaging.ProcessingTask` with `paramset_idx`.
4. Worker populates:
   - `imaging.Processing`
   - `imaging.MotionCorrection`
   - `imaging.Segmentation`
   - `imaging.MaskClassification`
   - `imaging.Fluorescence`
   - `imaging.Activity`

### Notes
- curation tasks can be generated post hoc from processing outputs.
- `curation_id` and `paramset_idx` must be tracked carefully in downstream analysis.

## 2) DLC pose tracking (video)

### Inputs
- camera videos in session/scan folders
- model names in `SHORTHAND;PURPOSE;VIDEOKEY` format

### Typical ingest path
1. Insert `model.VideoRecordingNew` and file rows.
2. Insert `model.PoseEstimationTaskNew` entries.
3. GPU worker populates:
   - `model.RecordingInfoNew`
   - `model.PoseEstimationNew`

### Notes
- keep model naming strict; this is key for reproducibility.
- recommended naming grammar:

```text
SHORTHAND;PURPOSE;VIDEOKEY
```

Example:

```text
XX;TopTrackingNoScope;top_video*.mp4
```

- use dynamic cropping settings deliberately (project-dependent).

## 3) Eye tracking and gaze reconstruction

### Inputs
- eye camera recordings
- head/body orientation context (often from mocap/virtual markers)

### Typical ingest path
1. Ingest eye videos / timestamp events.
2. Insert relevant pose/pupil task rows.
3. Run pupil tracking and gaze reconstruction workflows.

### Common linked schemas
- `pupil_tracking`
- `virtual_markers_optitrack`
- `mocap`

## 4) OptiTrack / mocap

### Inputs
- Motive exports (for example `.tak`, `.csv` variants)

### Typical ingest path
1. Insert `mocap.MocapRecording` and file rows.
2. Populate `mocap.MocapRecordingInfo` (sometimes ingest-side).
3. Insert `mocap.MotionCaptureTask`.
4. Worker populates `mocap.MotionCapture`.

### Critical permission note
`mocap.MotionCapture` may write blob-backed outputs.
Manual user populations can fail with filesystem permission errors even when DB SQL privileges exist.

## 5) BPod synchronization and trial ingest

### Inputs
- BPod session files / state events
- optional aux channels for alignment

### Typical ingest path
- ingest BPod raw events/states
- ingest trial times and event alignment
- populate behavior-side derived tables where enabled

### Common behavior-side computed calls
- `behavior.TreadmillRecording.populate(...)`
- `behavior.HarpRecording.populate(...)`
- `behavior.CamSyncRecording.populate(...)`

## Event/trial ontology (ADAMACS-specific)

Use the dedicated page:
- `Infrastructure -> Event/Trial Ontology`

It contains:
- ADAMACS table mapping for `event.*` and `trial.*`
- ASCII timeline
- graph visualization
- quick validation queries

## 6) Aux data ingest (HARP, treadmill, camera sync)

### Inputs
- aux files by setup type
- digital channel conventions by setup (`bench2p`, `openfield`, `behavior_box`, etc.)

### Typical ingest path
1. Determine setup from `scan.ScanInfo.userfunction_info`.
2. Call setup-specific ingest parser.
3. Populate derived behavior recordings.

### Notes
- setup type normalization is essential for parser routing.
- many failures are setup-string mismatch or channel-index mismatch.

## 7) Denoising and CASCADE tasks

### Denoising
- insert denoising tasks (as configured)
- worker populates `denoising.Denoising`

### CASCADE
- insert `imaging.ActivityCascadeTask`
- worker activity population writes cascade inference into activity traces
- this is generally worker-owned (task-driven), not manual heavy-populate territory for student sessions

## Setup-type mapping overview

Common normalized setup values used by ingest logic include:
- `mini2p1_openfield`
- `mini2p2_openfield`
- `mini2p2_headfixed`
- `bench2p`
- `bench2p_lineartrack`
- `bench2p_oddball`
- `bench2p_Oddball_V2`
- `behavior_box`

## Recommended modality onboarding for new students

1. Start with one calcium imaging session.
2. Add behavior sync ingest.
3. Add one DLC model path.
4. Add mocap session.
5. Add eye/gaze path.
6. Move to batch ingest templates.

## External docs by modality

- Calcium imaging:
  <https://docs.datajoint.com/elements/element-calcium-imaging/latest/>,
  <https://suite2p.readthedocs.io/en/latest/parameters/>,
  <https://suite2p.readthedocs.io/en/latest/outputs/>
- DLC pose tracking:
  <https://docs.datajoint.com/elements/element-deeplabcut/latest/>,
  <https://deeplabcut.github.io/DeepLabCut/>
- Event/trial synchronization:
  <https://docs.datajoint.com/elements/element-event/0.2/concepts/>,
  <https://docs.datajoint.com/core/datajoint-python/latest/query/operators/>
- DISK imputation:
  <https://github.com/bozeklab/DISK>
- CASCADE inference:
  <https://github.com/HelmchenLabSoftware/Cascade>
- Full index:
  `Common -> External References`

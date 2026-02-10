# Worker-Owned Population

This page defines which `populate()` calls are worker-managed versus user-run.

State snapshot:
- documented operational state as of `2026-02-10`

## Policy summary

- Students should generally stage `*Task` rows and avoid manually running heavy/blob-writing populations.
- Dedicated workers run with correct OS permissions and `reserve_jobs=True` patterns.

## Why this matters

Manual users can have valid DB SQL permissions but still fail at filesystem writes for blob-backed outputs.

Example error:

```text
[Errno 13] Permission denied: /datajoint-db/blobs/.../*.saving
```

## Current worker-managed populations

### MAIN_SERVER CPU worker loop

- `imaging.Processing.populate(...)`
- `imaging.Curation().create1_from_processing_task(...)` (curation task creation)
- `imaging.MotionCorrection.populate(...)`
- `imaging.Segmentation.populate(...)`
- `imaging.MaskClassification.populate(...)`
- `imaging.Fluorescence.populate(...)`
- `imaging.Activity.populate(...)`
- `mocap.MocapRecordingInfo.populate(...)`
- `mocap.MotionCapture.populate(...)`

### GPU_SERVER worker loops

- `model.RecordingInfoNew.populate(...)`
- `model.PoseEstimationNew.populate(...)`
- `denoising.Denoising.populate(...)`
- dedicated cascade/activity listener deployments can run `imaging.Activity.populate(...)` for queued cascade tasks

### BACKUP_SERVER

- no active autopopulate loops documented
- backup-only role

## Populate calls users can run (technically available)

These are callable from user sessions in code/notebooks, but policy should still decide what users actually run manually.

- `scan.ScanInfo.populate(...)`
- `behavior.TreadmillRecording.populate(...)`
- `behavior.HarpRecording.populate(...)`
- `behavior.CamSyncRecording.populate(...)`
- `mocap.MocapRecordingInfo.populate(...)`
- `mocap.MotionCapture.populate(...)`
- `imaging.Processing.populate(...)`
- `imaging.MotionCorrection.populate(...)`
- `imaging.Segmentation.populate(...)`
- `imaging.MaskClassification.populate(...)`
- `imaging.Fluorescence.populate(...)`
- `imaging.Activity.populate(...)`
- `model.RecordingInfoNew.populate(...)`
- `model.PoseEstimationNew.populate(...)`
- `denoising.Denoising.populate(...)`

## Recommended student-run subset

Usually safe to run manually (lightweight/non-protected):
- `scan.ScanInfo.populate(...)`
- `behavior.TreadmillRecording.populate(...)`
- `behavior.HarpRecording.populate(...)`
- `behavior.CamSyncRecording.populate(...)`

Usually worker-owned and not student-manual by default:
- imaging heavy chain
- mocap motion capture
- new DLC model chain
- denoising chain

## Rule of thumb

If a pipeline stage has a `*Task` table:
1. insert task rows
2. let workers pick up jobs
3. verify completion before analysis

## Operational verification snippets

```python
from adamacs.pipeline import imaging, model
from adamacs.schemas import mocap

print("pending processing:", len(imaging.ProcessingTask - imaging.Processing))
print("pending pose:", len(model.PoseEstimationTaskNew - model.PoseEstimationNew))
print("pending mocap:", len(mocap.MotionCaptureTask - mocap.MotionCapture))
```

For one scan:

```python
scan_id = "scanXXXX"
print("mocap done:", bool(mocap.MotionCapture & f'scan_id = "{scan_id}"'))
print("activity done:", bool(imaging.Activity & f'scan_id = "{scan_id}"'))
```

# Slack Post Template: Server Roles and Population Policy

Use this template when announcing worker behavior, permission policy, or onboarding updates.

## Copy-ready Slack post

```text
ADAMACS INFRA UPDATE (Ingest + Worker Policy)

Docs: <https://REPLACE_WITH_DOCS_URL>

Summary
- Main ingest entry point is adamacs_ingest (GUI + task insertion).
- If a *Task table exists, workers pick up these jobs automatically.
- Students can run many lightweight populations manually, but heavy/blob-writing jobs are worker-owned.

Current server roles
- MAIN_SERVER (172.25.64.3): DataJoint DB host, blob host, ingest share host, CPU worker host
- GPU_SERVER (172.25.70.3): GPU workers + model training/evaluation host
- BACKUP_SERVER (172.26.65.8): backup host (rsync pull + borg compression)

ASCII overview
[SETUPS + ACQUISITION PCs]
        |
        v
[Consolidated session folders]
        |
        v
[MAIN_SERVER share /datajoint-data/data/<user>]
        |
        v
[adamacs_ingest GUI + batch scripts]
        |
        +--> [DataJoint DB]
        |          |
        |          +--> [MAIN_SERVER CPU workers] --> [/datajoint-db/blobs/...]
        |          |
        |          +--> [GPU_SERVER GPU workers] --> [/datajoint-db/blobs/...]
        |
        +--> [Task tables]

[Data + blobs + DB dumps] --> [BACKUP_SERVER backup pulls] --> [borg zstd,22 archives]

Closed-loop
GPU_SERVER model training/evaluation can feed stimulation candidates back to bench2p1 (MEI restimulation), and those new recordings re-enter ingest.

Worker-managed populate calls
MAIN_SERVER CPU worker:
- imaging.Processing.populate(...)
- imaging.Curation().create1_from_processing_task(...)
- imaging.MotionCorrection.populate(...)
- imaging.Segmentation.populate(...)
- imaging.MaskClassification.populate(...)
- imaging.Fluorescence.populate(...)
- imaging.Activity.populate(...)
- mocap.MocapRecordingInfo.populate(...)
- mocap.MotionCapture.populate(...)

GPU_SERVER GPU workers:
- model.RecordingInfoNew.populate(...)
- model.PoseEstimationNew.populate(...)
- denoising.Denoising.populate(...)
- activity/cascade listener deployments can run imaging.Activity.populate(...) for cascade-task queues

Typical user-run populate calls (lightweight/common)
- scan.ScanInfo.populate(...)
- behavior.TreadmillRecording.populate(...)
- behavior.HarpRecording.populate(...)
- behavior.CamSyncRecording.populate(...)

Permission note
If you see:
[Errno 13] Permission denied: /datajoint-db/blobs/.../*.saving
this usually means SQL rights are fine but Linux blob-path write rights are not.
For worker-owned paths, stage task rows and let workers finish.

Quick check example
scan_id = "<your_scan_id>"
bool(mocap.MotionCapture & f'scan_id = "{scan_id}"')

For <user> specifically: please check if mocap.MotionCapture for your scan is already populated now.
```

## Tips

- Replace the docs URL before posting.
- Keep the worker list synchronized with `Infrastructure -> Worker-Owned Population`.
- Keep server/IP entries synchronized with `Infrastructure -> Architecture`.

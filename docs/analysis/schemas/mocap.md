# Mocap Schema

Schema: `mocap`

This schema ingests OptiTrack/Motive outputs and provides marker and rigid-body trajectories.
It is the raw kinematic layer for head/body reconstruction.

## What this schema answers

- Which motion-capture recording belongs to a scan?
- Which markers/rigid bodies were tracked and with what timestamps?
- Which mocap import task produced the current structured output?

## Core ADAMACS tables

- `mocap.MocapRecording`, `mocap.MocapRecording.File`, `mocap.MocapRecordingInfo`
- `mocap.TrackingId`
- `mocap.Mocap`, `mocap.Mocap.TrackingId`
- `mocap.MotionCaptureTask`
- `mocap.MotionCapture`
- `mocap.MotionCapture.TrackingPosition`
- `mocap.MotionCapture.RigidBodyPosition`

## Query anchors

- `scan_id`
- `mocap_name`
- `tracking_id`

```python
scan_key = {'session_id': 'sessXXXXXXXX', 'scan_id': 'scanXXXXXXXX'}
(mocap.MotionCapture & scan_key)
(mocap.MotionCapture.TrackingPosition & scan_key)
```

## Diagram

![Mocap schema](../../assets/db_diagrams/mocap.svg)

## Notes for users

- Check tracking IDs before assuming a marker is missing.
- Keep coordinate-frame assumptions explicit in downstream transforms.
- Use `MotionCaptureTask` as the execution boundary for reproducibility.

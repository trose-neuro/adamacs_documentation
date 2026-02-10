# Virtual Markers OptiTrack Schema

Schema: `virtual_markers_optitrack`

This schema converts raw mocap markers into rigid-body aligned virtual landmarks.
It is the bridge from raw marker coordinates to head-centered pose interpretation.

## What this schema answers

- How are eye/nose/world-camera landmarks defined in local head coordinates?
- What is the reconstructed global head pose per frame?
- Which quaternion/Euler streams should downstream gaze reconstruction use?

## Core ADAMACS tables

- `virtual_markers_optitrack.EyeNoseCamPosCalib`
- `virtual_markers_optitrack.RigidMouseTracking`

## Query anchors

- `scan_id`
- `subject`
- `mocap_name`

```python
scan_key = {'session_id': 'sessXXXXXXXX', 'scan_id': 'scanXXXXXXXX'}
(virtual_markers_optitrack.RigidMouseTracking & scan_key)
```

## Diagram

![Virtual markers schema](../../assets/db_diagrams/virtual_markers_optitrack.svg)

## Notes for users

- Validate calibration landmarks before trusting downstream gaze vectors.
- Keep axis-transform assumptions documented in notebook code.
- Use quaternion outputs as the canonical head-orientation signal for world transforms.

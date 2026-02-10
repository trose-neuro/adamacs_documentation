# Behavior Schema

Schema: `behavior`

This schema stores continuous behavioral streams derived from auxiliary recordings.
It complements event/trial tables by keeping channel-wise waveform and timestamp arrays.

## What this schema answers

- Which IMU/treadmill/camsync streams were ingested?
- Which channels and time vectors are available?
- Are behavioral channels aligned well enough for downstream fusion?

## Core ADAMACS tables

- `behavior.HarpDevice`, `behavior.HarpRecording`, `behavior.HarpRecording.Channel`
- `behavior.TreadmillDevice`, `behavior.TreadmillRecording`, `behavior.TreadmillRecording.Channel`
- `behavior.CamSyncDevice`, `behavior.CamSyncRecording`, `behavior.CamSyncRecording.Channel`

## Query anchors

- `session_id`
- `scan_id`
- `channel_name`

```python
scan_key = {'session_id': 'sessXXXXXXXX', 'scan_id': 'scanXXXXXXXX'}
(behavior.HarpRecording.Channel & scan_key)
(behavior.CamSyncRecording.Channel & scan_key)
```

## Diagram

![Behavior schema](../../assets/db_diagrams/behavior.svg)

## Notes for users

- Validate channel availability before running movement-state analysis.
- Keep resampling/downsampling steps documented in analysis code.
- Use behavior channels together with event/timestamps for robust synchronization checks.

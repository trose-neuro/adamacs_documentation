# DISK Schema

Schema: `disk`

This schema integrates DISK-based imputation for pose and mocap streams.
It is an optional enhancement layer used when missing-value reconstruction is needed.

## What this schema answers

- Which DISK model was used for an imputation run?
- Which imputation task was staged and executed?
- How many frames/values were imputed and with what uncertainty?

## Core ADAMACS tables

- `disk.DISKModel`
- `disk.DLCImputationTask`, `disk.DLCImputation`, `disk.DLCImputation.BodyPartPositionDISK`
- `disk.MocapImputationTask`, `disk.MocapImputation`
- `disk.MocapImputation.TrackingPositionDISK`
- `disk.MocapImputation.RigidBodyPositionDISK`

## Query anchors

- `disk_model_name`
- `task_mode`
- `session_id`
- `scan_id`

```python
scan_key = {'session_id': 'sessXXXXXXXX', 'scan_id': 'scanXXXXXXXX'}
(disk.DLCImputationTask & scan_key)
(disk.MocapImputationTask & scan_key)
```

## Diagram

![DISK schema](../../assets/db_diagrams/disk.svg)

## Notes for users

- Treat imputed outputs as a distinct data product, not a silent replacement of raw values.
- Preserve uncertainty and mask fields in downstream analyses.
- Report model/version metadata whenever imputed values are used.

## External references

- DISK source and README:
  <https://github.com/bozeklab/DISK>
- DeepLabCut docs (for upstream pose streams):
  <https://deeplabcut.github.io/DeepLabCut/>
- Element DeepLabCut integration:
  <https://docs.datajoint.com/elements/element-deeplabcut/latest/>
- DataJoint query operators:
  <https://docs.datajoint.com/core/datajoint-python/latest/query/operators/>

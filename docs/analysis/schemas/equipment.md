# Equipment Schema

Schema: `equipment`

This schema is the hardware vocabulary layer.
It normalizes scanner/camera/restraint labels used by ingest and model tables.

## What this schema answers

- Which scanner or camera produced this data?
- Which setup/constraint context was used at acquisition time?
- Which hardware-specific processing branch should be selected?

## Core ADAMACS tables

- `equipment.Equipment`: scanner definitions.
- `equipment.Device`: camera/device definitions.
- `equipment.SetupRestraint`: setup condition labels.

## Query anchors

- `scanner`
- `camera`
- `setup_restraint`

```python
(scan.Scan * equipment.Equipment)
(model.VideoRecording * equipment.Device)
```

## Diagram

![Equipment schema](../../assets/db_diagrams/equipment.svg)

## Notes for users

- Restrict hardware early if your analysis depends on specific optics/cameras.
- Keep hardware labels controlled; avoid introducing ad-hoc names.

# Imaging Schema

Schema: `imaging`

This schema is the calcium-processing backbone.
It stages processing tasks, tracks curation state, and stores segmentation/trace/activity outputs.

## What this schema answers

- Which processing configuration was run for a scan?
- Which curation/version should be analyzed?
- Where are masks, fluorescence traces, and activity readouts?

## Core tables used most often

- `imaging.ProcessingTask`, `imaging.Processing`
- `imaging.ProcessingParamSet`
- `imaging.Curation`
- `imaging.MotionCorrection`
- `imaging.Segmentation`, `imaging.Segmentation.Mask`
- `imaging.Fluorescence`, `imaging.Fluorescence.Trace`
- `imaging.Activity`, `imaging.Activity.Trace`

## Query anchors

- `scan_id`
- `paramset_idx`
- `curation_id`

```python
proc_key = {'session_id': 'sessXXXXXXXX', 'scan_id': 'scanXXXXXXXX', 'paramset_idx': 66}
(imaging.ProcessingTask & proc_key)
(imaging.Curation & proc_key)
```

## Diagram

![Imaging schema](../../assets/db_diagrams/imaging.svg)

## Notes for users

- Always carry `paramset_idx` and `curation_id` when reporting results.
- Do not mix curated and uncurated outputs in one analysis block.
- Check task status before assuming a missing table indicates data absence.

## Element lineage

ADAMACS imaging follows Element Calcium Imaging processing conventions.
Reference: <https://docs.datajoint.com/elements/element-calcium-imaging/latest/>

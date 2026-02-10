# Model Schema

Schema: `model`

This schema manages video recordings, model definitions, and pose-estimation outputs.
It is the main route from camera streams to body-part trajectories.

## What this schema answers

- Which recording/model pair produced a pose estimate?
- Which task is staged (`load`/`trigger`) and where is output stored?
- Which body-part trajectories are available for alignment with events or neural data?

## Core tables used most often

- `model.VideoRecording`, `model.VideoRecording.File`
- `model.VideoRecordingNew`, `model.VideoRecordingNew.File`
- `model.Model`, `model.Model.BodyPart`
- `model.PoseEstimationTask`, `model.PoseEstimation`
- `model.PoseEstimationTaskNew`
- `model.RecordingInfo`, `model.RecordingInfoNew`

## Query anchors

- `recording_id`
- `model_name`
- `task_mode`

```python
(model.PoseEstimationTaskNew & {'scan_id': 'scanXXXXXXXX'})
(model.PoseEstimationNew & {'recording_id': 'LE_eye_left_tracking_YYYY-MM-DD'})
```

## Diagram

![Model schema](../../assets/db_diagrams/model.svg)

## Notes for users

- Keep `recording_id` and `model_name` explicit in all notebook outputs.
- Validate `task_mode` before interpreting empty computed tables.
- Use model body-part vocabularies as controlled contracts across analyses.

## Element lineage

ADAMACS model tables build on Element DeepLabCut patterns.
Reference: <https://docs.datajoint.com/elements/element-deeplabcut/latest/>

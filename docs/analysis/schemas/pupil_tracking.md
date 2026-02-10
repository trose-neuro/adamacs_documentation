# Pupil Tracking Schema

Schema: `pupil_tracking`

This schema turns eye-camera body-part tracks into pupil geometry, synchronized eye rotation, and 3D gaze vectors.
It is the main eye-to-world interpretation layer.

## What this schema answers

- Which ellipse-fitting parameters were used?
- How were eye-camera timestamps synchronized to optitrack frames?
- What are the gaze vectors in head and world coordinates?

## Core ADAMACS tables

- `pupil_tracking.PupilEllipseParameter`
- `pupil_tracking.PupilEllipseFitting`
- `pupil_tracking.PupilEllipseParametersFreeMoving`
- `pupil_tracking.EyeCamTimeSource`
- `pupil_tracking.PupilEllipseFittingFreeMoving`
- `pupil_tracking.PupilRotationOptiTrack`
- `pupil_tracking.TorsionCalibManual`
- `pupil_tracking.EyeModel`
- `pupil_tracking.GazeReconstruction3D`

## Query anchors

- `recording_id`
- `parameter_id`
- `eyecam_time_source`
- `eye_model_id`

```python
scan_key = {'session_id': 'sessXXXXXXXX', 'scan_id': 'scanXXXXXXXX'}
(pupil_tracking.PupilRotationOptiTrack & scan_key)
(pupil_tracking.GazeReconstruction3D & scan_key)
```

## Diagram

![Pupil tracking schema](../../assets/db_diagrams/pupil_tracking.svg)

## Notes for users

- Keep timestamp source (`ocr`, `lin`, `bonsaicsv`) explicit in analyses.
- Treat eye model and torsion parameters as versioned analysis assumptions.
- Validate frame-count alignment before interpreting gaze-neural coupling.

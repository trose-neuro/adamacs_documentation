# Ingest GUI Workflow

The ingest GUI is the primary student-facing ingest interface.

## Main entrypoint

```python
from adamacs.gui import select_sessions

select_sessions(["TR_ROS-0000_2026-01-01_sessXXXX_scanXXXX"])
```

In notebook form, use the center-stage workflow notebook in `adamacs_ingest`.

## What the GUI does

At a high level, the GUI workflow:
- discovers candidate session folders
- parses session and scan identifiers from folder names
- resolves user defaults (cameras, setup type, parameter defaults)
- ingests session + scan metadata
- inserts processing tasks (imaging, pose, mocap, cascade where configured)
- optionally performs lightweight populate steps

## Recommended operator sequence

1. Open GUI notebook and connect to DataJoint.
2. Confirm root data directory and visible session list.
3. Filter sessions by date/subject/user as needed.
4. Verify each selected session has correct:
   - subject ID
   - session date
   - scan IDs
   - setup type / camera defaults
   - processing parameter set index
5. Commit ingest.
6. Validate task rows were inserted.
7. Wait for worker completion on heavy pipelines.

## Safe defaults for students

- Keep heavy population toggles disabled unless explicitly required.
- Prefer task insertion over manual population for blob-heavy workflows.
- For troubleshooting, temporarily set strict error mode only on a single test key.

## Common GUI-side outputs

- `session` and `scan` metadata rows
- `scan.ScanInfo` updates
- `imaging.ProcessingTask`
- `model.PoseEstimationTaskNew`
- `mocap.MotionCaptureTask`
- `imaging.ActivityCascadeTask` (when model setup warrants)

## Post-commit checks

Use quick checks to confirm pipeline movement:

```python
from adamacs.pipeline import imaging, model
from adamacs.schemas import mocap

print("Processing tasks:", len(imaging.ProcessingTask))
print("Pose tasks:", len(model.PoseEstimationTaskNew))
print("Mocap tasks:", len(mocap.MotionCaptureTask))
```

Then restrict by session/scan key for targeted verification.

## Debugging strategy

If GUI commit fails:
- check directory naming tokens (`sess...`, `scan...`)
- verify scan files exist and are readable
- run on one session at a time
- inspect traceback with `suppress_errors=False` in controlled debugging context

## Related pages

- `Ingest -> Batch Ingest`
- `Common -> Troubleshooting`
- `Infrastructure -> Worker-Owned Population`

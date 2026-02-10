# Schema Chapters (User-Focused)

This section breaks the ADAMACS database into practical chapters, one per major schema.
Use it as a working map when you are deciding where to read from, where to stage tasks, and which keys to carry forward.

The content here is derived from:
- live ADAMACS schema modules (`adamacs_ingest/adamacs/schemas/*.py`)
- `dj.Diagram` exports from `adamacs_analysis/notebooks/21_schema_dependency_diagrams.ipynb`
- DataJoint Element documentation
- reference pipeline documentation on ReadTheDocs

No personal identifiers are required to use these chapters. Work with stable keys (`subject`, `session_id`, `scan_id`, `recording_id`) and controlled vocabularies.

## Read order

1. `subject` -> `session` -> `scan`
2. `event` + `trial` + `behavior`
3. `imaging` + `model`
4. `mocap` + `virtual_markers_optitrack` + `pupil_tracking`
5. `disk` for imputation workflows

```{toctree}
:maxdepth: 1

schemas/subject
schemas/surgery
schemas/equipment
schemas/session
schemas/scan
schemas/imaging
schemas/model
schemas/event
schemas/trial
schemas/behavior
schemas/mocap
schemas/virtual_markers_optitrack
schemas/pupil_tracking
schemas/disk
```

## External references used

- DataJoint Elements index: <https://docs.datajoint.com/elements/>
- DataJoint core docs: <https://docs.datajoint.com/core/datajoint-python/latest/>
- Element Session: <https://docs.datajoint.com/elements/element-session/latest/>
- Element Calcium Imaging: <https://docs.datajoint.com/elements/element-calcium-imaging/latest/>
- Element DeepLabCut: <https://docs.datajoint.com/elements/element-deeplabcut/latest/>
- Element Event concepts: <https://docs.datajoint.com/elements/element-event/0.2/concepts/>
- Suite2p docs: <https://suite2p.readthedocs.io/en/latest/>
- Suite2p parameters: <https://suite2p.readthedocs.io/en/latest/parameters/>
- DeepLabCut docs: <https://deeplabcut.github.io/DeepLabCut/>
- DISK source: <https://github.com/bozeklab/DISK>
- CASCADE source: <https://github.com/HelmchenLabSoftware/Cascade>
- Reference pipeline docs: <https://moser-pipelines.readthedocs.io/en/latest/>
- Reference pipeline components page: <https://moser-pipelines.readthedocs.io/en/latest/technical/contributing.html#components-of-the-pipeline>

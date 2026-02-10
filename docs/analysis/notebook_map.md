# Analysis Notebook Map

This map reflects the current notebook set in `adamacs_analysis`.

## Starter notebooks

- `01_querying_guide.ipynb`
  - best first notebook for new users
  - shows core restrictions and joins
- `02_querying_template.ipynb`
  - reusable template for new analyses
- `03_blender_gaze_render.ipynb`
  - gaze rendering workflow with parameterized execution

## Personal/project notebooks

Personal notebooks exist in numbered slots (for example `04_personal_*.ipynb` through `09_personal_*.ipynb`).

Treat these as examples only:
- they often contain project-specific assumptions
- they are not canonical onboarding notebooks

## Operations and diagnostics

- `20_routine_quick_job_cleanup_template.ipynb`
  - cleanup and job management template
- `21_schema_dependency_diagrams.ipynb`
  - exports dependency diagrams for schema domains

## Behavioral analysis series (`behavioral_series`)

- `01_trial_event_summary_refactored.ipynb`
- `02_group_behavioral_metrics_refactored.ipynb`
- `03_pupil_headcam_sync_qc_refactored.ipynb`

## Suggested progression for new students

1. Run `01_querying_guide.ipynb` end-to-end.
2. Copy `02_querying_template.ipynb` and rename for your project.
3. Add one modality branch (imaging, pose, gaze, or behavior).
4. Move reusable code from notebook to helper module when stable.

## Notebook hygiene

- keep one logical question per notebook
- avoid hidden state between cells
- pin all key restrictions in a top parameter cell
- save exported figures with descriptive filenames and date/version tags

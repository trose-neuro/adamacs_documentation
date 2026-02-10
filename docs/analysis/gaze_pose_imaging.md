# Gaze, Pose, and Imaging Integration

This page outlines a practical multimodal integration workflow for:
- calcium imaging traces
- DLC/pose trajectories
- mocap / head orientation
- pupil/gaze reconstruction

## Conceptual pipeline

```{mermaid}
flowchart LR
    I[Imaging traces and activity] --> J[Shared scan or session keys]
    P[DLC pose trajectories] --> J
    M[Mocap and virtual markers] --> J
    G[Pupil and gaze outputs] --> J
    J --> K[Aligned analysis dataframe or tensors]
    K --> L[Behavior-neural coupling metrics]
```

## Practical key strategy

1. Choose one anchor keyspace:
   - usually `scan_id` plus session restriction
2. Build restricted keyset.
3. Join each modality to that keyset.
4. Validate row completeness per modality.

## Timing and synchronization checks

Before deriving metrics:
- verify event timestamps and sampling assumptions
- check camera frame counts vs pose timestamps
- check mocap timebase and scan reference alignment

## Suggested metric families

- head direction vs neural activity
- pupil diameter vs fluorescence or inferred activity
- gaze-world intersection vs task events
- movement speed/turning vs neural state transitions

## Quality control checklist

- missing modality coverage reported explicitly
- outlier frames/sessions excluded by transparent rule
- model names and curation versions logged
- plots include trial/session context

## Reproducibility fields to attach to outputs

For each exported metric table or figure:
- `session_id`, `scan_id`
- `paramset_idx`, `curation_id`
- DLC `model_name`
- software commit hash
- processing date/time

## Typical failure modes

- mismatched key granularity (`recording_id` vs `scan_id`)
- implicit use of mixed curation versions
- silently missing worker-generated tables
- setup-specific timestamp conventions ignored


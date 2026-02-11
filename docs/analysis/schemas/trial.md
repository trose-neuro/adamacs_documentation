# Trial Schema

Schema: `trial`

This schema turns continuous recordings into trial-structured analysis units.
It is the main route for condition-locked aggregation and trial-level statistics.

## What this schema answers

- Which trial windows exist for a recording?
- Which trial types/blocks are defined?
- Which events belong to each trial?

## Core tables used most often

- `trial.TrialType`
- `trial.Trial`
- `trial.TrialEvent`
- `trial.Block`
- `trial.BlockTrial`

## Query anchors

- `session_id`
- `scan_id`
- `trial_id`
- `trial_type`

```python
scan_key = {'session_id': 'sessXXXXXXXX', 'scan_id': 'scanXXXXXXXX'}
(trial.Trial & scan_key)
(trial.TrialEvent & scan_key)
```

## Diagram

![Trial schema](../../assets/db_diagrams/trial.svg)

## Notes for users

- Keep trial definitions in-table; avoid per-notebook trialization variants.
- Validate `trial_start_time`/`trial_stop_time` against event timestamps.
- For condition comparisons, include explicit `trial_type` restrictions.

## Element lineage

ADAMACS trial logic follows Element Event trial tables.
Reference: <https://docs.datajoint.com/elements/element-event/0.2/concepts/>

## External references

- Element Event concepts (trial ontology):
  <https://docs.datajoint.com/elements/element-event/0.2/concepts/>
- DataJoint query operators:
  <https://docs.datajoint.com/core/datajoint-python/latest/query/operators/>
- ADAMACS ontology page:
  `Infrastructure -> Event/Trial Ontology`

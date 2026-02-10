# Subject Schema

Schema: `subject`

This schema is the identity and cohort backbone.
If identity metadata is inconsistent here, every downstream join becomes fragile.

## What this schema answers

- Which subject is this session/scan linked to?
- Which project/protocol/line context should this subject be grouped under?
- Is there genotype or life-cycle metadata that changes interpretation?

## Core ADAMACS tables

- `subject.Subject`: canonical subject identity row.
- `subject.User`: ownership/responsibility metadata used by session and ingest workflows.
- `subject.Project`: project-level grouping labels.
- `subject.Line`, `subject.Protocol`, `subject.Mutation`: biological and protocol context.
- `subject.SubjectGenotype`, `subject.SubjectDeath`, `subject.SubjectRspace`: optional extensions.

## Query anchors you will reuse

- `subject`
- `owner_id`
- `project`

```python
subject_key = {'subject': 'ROS-XXXX'}
(session.Session & subject_key)
(scan.Scan & subject_key)
```

## Diagram

![Subject schema](../../assets/db_diagrams/subject.svg)

## Notes for users

- Treat `subject` as a long-lived key; avoid notebook-local aliases.
- Keep project/protocol restrictions explicit in analysis notebooks.
- Resolve identity mismatch here before debugging downstream tables.

## Lineage

This is ADAMACS-specific, but conceptually aligns with Element-style identity layers used before session-level ingestion.
Reference: <https://docs.datajoint.com/elements/element-animal/latest/>

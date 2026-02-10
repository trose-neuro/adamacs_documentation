# Surgery Schema

Schema: `surgery`

This schema stores intervention context that changes how recordings should be interpreted.
Use it when grouping scans by implantation site, injection strategy, or preparation constraints.

## What this schema answers

- What intervention history applies to this subject?
- Which anatomical target and coordinates were used?
- Which substances/protocol elements are relevant for interpretation?

## Core ADAMACS tables

- `surgery.Surgery`, `surgery.SurgeryNote`
- `surgery.AnatomicalLocation`, `surgery.Coordinates`
- `surgery.Virus`, `surgery.ViralInjection`
- `surgery.Anesthesia`, `surgery.Analgesia`, `surgery.Antagonist`, `surgery.AnalgesiaSubject`
- `surgery.CranialWindow`

## Query anchors

- `subject`
- `date` (surgery date)
- `anatomical_location`

```python
subject_key = {'subject': 'ROS-XXXX'}
(surgery.Surgery & subject_key)
(surgery.CranialWindow & subject_key)
```

## Diagram

![Surgery schema](../../assets/db_diagrams/surgery.svg)

## Notes for users

- Prefer lookup-controlled labels over free-text notes where possible.
- Join surgery context before cross-subject comparisons.
- Keep coordinate use explicit when deriving anatomical groupings.

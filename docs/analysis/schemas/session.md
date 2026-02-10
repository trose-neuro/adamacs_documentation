# Session Schema

Schema: `session`

This schema binds subject identity to a concrete acquisition session.
Most analysis key sets should start here before descending into scan- or recording-level tables.

## What this schema answers

- Which sessions exist for a subject/project/date window?
- Where is the session directory and who is linked to it?
- Which session notes or same-site grouping tags apply?

## Core tables used most often

- `session.Session`
- `session.SessionDirectory`
- `session.SessionUser`
- `session.SessionNote`
- `session.SessionSite`, `session.SessionSameSite`
- `session.SessionRspace` (optional external linkage)

## Query anchors

- `session_id`
- `subject`
- `session_datetime`

```python
session_key = {'session_id': 'sessXXXXXXXX'}
(session.Session & session_key)
(scan.Scan & session_key)
```

## Diagram

![Session schema](../../assets/db_diagrams/session.svg)

## Notes for users

- Use session restrictions to narrow the search space before multimodal joins.
- Keep session-level notes as context, not as key logic.
- Carry `session_id` through all downstream tables for reproducibility.

## Element lineage

ADAMACS session design follows the Element Session model.
Reference: <https://docs.datajoint.com/elements/element-session/latest/>

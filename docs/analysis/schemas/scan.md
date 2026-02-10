# Scan Schema

Schema: `scan`

This is the multimodal acquisition anchor.
In ADAMACS, `scan_id` is usually the most practical restriction when validating ingest and linking modalities.

## What this schema answers

- What acquisition unit should downstream processing attach to?
- Which scan metadata (software/channels/fields/files) is available?
- Which scan should imaging, event, model, and mocap tables be restricted to?

## Core tables used most often

- `scan.Scan`
- `scan.ScanInfo`, `scan.ScanInfo.Field`, `scan.ScanInfo.ScanFile`
- `scan.Channel`
- `scan.AcquisitionSoftware`
- `scan.ScanPath`, `scan.ScanLocation`

## Query anchors

- `session_id`
- `scan_id`

```python
scan_key = {'session_id': 'sessXXXXXXXX', 'scan_id': 'scanXXXXXXXX'}
(scan.Scan & scan_key)
(event.BehaviorRecording & scan_key)
(imaging.ProcessingTask & scan_key)
```

## Diagram

![Scan schema](../../assets/db_diagrams/scan.svg)

## Notes for users

- Start multimodal debugging from `scan_key`.
- Validate scan metadata before debugging downstream computed tables.
- Keep scan-level filters explicit in notebooks to avoid accidental cross-scan joins.

## Element lineage

ADAMACS scan structure aligns with Element Calcium Imaging scan concepts.
Reference: <https://docs.datajoint.com/elements/element-calcium-imaging/latest/>

# Query Patterns

This page provides robust patterns for multimodal DataJoint queries in analysis workflows.

## 1) Start narrow, then expand

Bad pattern:
- large unrestricted joins followed by filtering in pandas

Good pattern:
- apply strict key restrictions first, then join

```python
base = scan.Scan & 'session_id = "sessXXXX"' & 'scan_id = "scanXXXX"'
```

## 2) Restrict curation and parameter sets explicitly

Always include these where relevant:
- `paramset_idx`
- `curation_id`

```python
q = imaging.Fluorescence & 'paramset_idx = 1' & 'curation_id = 1'
```

## 3) Build keysets for downstream joins

```python
keyset = (scan.Scan & 'session_id = "sessXXXX"').proj()
pose = model.PoseEstimationNew & keyset
moc = mocap.MotionCapture & keyset
```

## 4) Verify upstream completion before analysis

```python
pending_pose = model.PoseEstimationTaskNew - model.PoseEstimationNew
print("pending pose tasks:", len(pending_pose))
```

If pending is high, analysis gaps may be operational, not code-related.

## 5) Key-integrity checks

Before fetch/plot:
- check tuple count
- inspect one sample row
- verify key uniqueness assumptions

```python
print(len(q))
print((q).fetch('KEY', limit=3))
```

## 6) Event alignment pattern

When joining event and continuous streams:
- confirm event type labels are exact
- verify timestamp units and sampling rate assumptions
- test alignment on one scan before cohort aggregation

## 7) Cohort-level aggregation pattern

1. Define cohort keyset (`subject`, date range, project).
2. Materialize per-scan metrics.
3. Concatenate into analysis table.
4. Store provenance metadata columns.

## 8) Common anti-patterns

- mixing different curation IDs implicitly
- using wildcard restrictions that include wrong setups
- joining across scan/session without explicit key projection
- interpreting missing rows as biological null instead of pipeline incomplete

## 9) Suggested reusable helper design

When a query stabilizes across notebooks:
- move it into `adamacs_analysis` helper module
- write a small test around expected key behavior
- call helper from notebooks


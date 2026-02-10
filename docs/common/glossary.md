# Glossary

## ADAMACS
Architectures for Data Management and Computational Support, the DataJoint-centered pipeline ecosystem used in the lab.

## DataJoint schema
Logical table namespace (for example `subject`, `imaging`, `model`, `mocap`).

## Session
A recording unit identified by a unique `session_id`.

## Scan
A recording sub-unit linked to a session, identified by `scan_id`.

## `*Task` table
Manual/staging table indicating that downstream computed processing should be run.

## Worker
Background process that continuously calls `populate(..., reserve_jobs=True)` on selected tables.

## Reserve jobs
DataJoint mechanism to avoid duplicate compute across concurrent workers.

## Blob store
Filesystem-backed large-object storage used for large payloads instead of direct DB inline storage.

## Curation
Manual/algorithmic quality-control state for extracted imaging components.

## `paramset_idx`
Processing parameter set identifier used in imaging processing workflows.

## `curation_id`
Version key identifying curation iteration.

## PyRAT
Animal metadata source system queried for subject/genotype metadata staging.

## RSpace
Electronic lab notebook service used optionally for ingest-linked document creation.

## CASCADE
Ground-truth-calibrated spike inference integration path in imaging activity workflows.

## DLC
DeepLabCut model workflows for video-based pose tracking.

## Worker-owned population
Population step that should usually be run by dedicated server worker accounts rather than personal user accounts.

## Legacy monorepo
Original `adamacs` repository before ingest/analysis split.

## Split repos
Current recommended working repos:
- `adamacs_ingest`
- `adamacs_analysis`

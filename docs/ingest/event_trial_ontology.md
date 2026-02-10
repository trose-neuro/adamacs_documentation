# Event/Trial Ontology (ADAMACS)

This page adapts the DataJoint Element Event ontology to ADAMACS usage.

Reference: [Element Event concepts](https://docs.datajoint.com/elements/element-event/0.2/concepts/).

## Ontology-first mindset for ADAMACS

The core idea is simple: define time ontology first, then run analysis.

In practice:
- first agree on what counts as a session, scan, block, trial, and event
- encode those concepts in tables and keys
- only then compute features, train models, and compare conditions

This is why ADAMACS treats event/trial structure as core infrastructure, not as notebook-side convenience.

## Why this matters

Most ingest/debug issues in behavior synchronization come from unclear timing ontology.
Use this page when validating `event.Event` and `trial.Trial` population.

## ADAMACS ontology map

| Concept | Element Event table | ADAMACS usage |
| --- | --- | --- |
| Session | `session.Session` | One experiment session (`session_id`) |
| Recording | `event.BehaviorRecording` + `.File` | Behavior/AUX recording linked to the session/scan ingest context |
| Event vocabulary | `event.EventType` | Names such as `aux_cam`, `optitrack_frames`, `raw_bpod_*` |
| Event instances | `event.Event` | Timestamped entries (`event_start_time`, optional `event_end_time`) |
| Trial vocabulary | `trial.TrialType` | Trial category labels |
| Trial instances | `trial.Trial` | Trial windows (`trial_start_time`, `trial_stop_time`) |
| Event-trial link | `trial.TrialEvent` | Event membership per trial |
| Optional blocking | `trial.Block`, `trial.BlockTrial` | Block-level grouping (optional) |
| Analysis window spec | `event.AlignmentEvent` | Event-locked windows for downstream analysis |

## Expanded labeled timeline (adapted)

This extends the Element Event conceptual timeline with ADAMACS labels used in practice.

```text
|------------------------ behavior.Procedure 1 (session-bound) ------------------------|_____|------- behavior.Procedure 2 (cross-session labels) -------|
|-------------------------------------------- Session 1 --------------------------------------------|______________________________|------------- Session 2 -------------|
|---------------------------- Scan 1 ----------------------------|__|--------- Scan 2 ---------|_______________________________________|--------- Scan 1 ---------|__|---- Scan 2 ----|
|----- Block 1 -----|______|----- Block 2 -----|______|----- Block 3 -----|
| Trial 1 || Trial 2 |____| Trial 3 || Trial 4 |____| Trial 5 |____| Trial 6 |
|_|e1|_|e2||e3|_|e4|__|e5|__|e6||e7||e8||e9||e10||e11|____|e12||e13|______|
```

Interpretation:
- Procedure labels are conceptual groupings:
  - session-bound variants usually map to session metadata + trial/event labels
  - cross-session variants are shared label vocabularies (for example `trial.TrialType`, `event.EventType`)
- `behavior.Procedure` in this timeline is a conceptual label, not a required core table in ADAMACS.
- Scans are ingest units in ADAMACS and are commonly used as restrictions (`scan_key`).
- Blocks and trials are intervals; events are points/spans on the same recording clock.
- `trial.TrialEvent` links event instances to trial windows.

## Procedure labels in ADAMACS

In ADAMACS, procedures are part of the experimental grammar, not free text.
ADAMACS mirrors this with two practical layers:

- session-bound procedure context:
  usually represented through session/recording metadata (`session.SessionNote`, `event.BehaviorRecording.recording_notes`) and scan-restricted event/trial rows
- cross-session procedure vocabulary:
  represented by stable label sets in `event.EventType` and `trial.TrialType`

If the lab decides to add a dedicated `behavior.Procedure` lookup later, this ontology still holds:
- the table should define shared vocabulary
- session/scan/trial tables should carry the instance-level links

## Label mapping in ADAMACS

| Timeline label | Where to store/restrict |
| --- | --- |
| Procedure (session-bound) | `session.Session*`, scan restrictions, `recording_notes`, session notes |
| Procedure (cross-session) | `trial.TrialType`, `event.EventType` |
| Session | `session_id` |
| Scan | `scan_id` (use `scan_key`) |
| Block | `trial.Block` (optional) |
| Trial | `trial.Trial` |
| Event (`e1`, `e2`, ...) | `event.Event` with `event_type` |

## Graph visualization

```{mermaid}
flowchart TD
    S["session.Session<br/>(session_id)"]
    SC["scan.Scan<br/>(session_id, scan_id)"]

    BR["event.BehaviorRecording<br/>(recording_start_time, recording_duration, recording_notes)"]
    BRF["event.BehaviorRecording.File<br/>(filepath)"]
    ET["event.EventType<br/>(event_type)"]
    EV["event.Event<br/>(event_start_time, event_end_time)"]
    AE["event.AlignmentEvent<br/>(alignment/start/end event types + shifts)"]

    TT["trial.TrialType"]
    TR["trial.Trial<br/>(trial_id, trial_start_time, trial_stop_time)"]
    TV["trial.TrialEvent"]
    BL["trial.Block"]
    BT["trial.BlockTrial"]

    S --> SC
    S --> BR
    BR --> BRF
    BR --> EV
    ET --> EV
    ET --> AE
    BR --> TR
    TT --> TR
    TR --> TV
    EV --> TV
    BR --> BL
    BL --> BT
    TR --> BT
```

## ER view (same ontology)

```{mermaid}
erDiagram
    SESSION ||--o{ BEHAVIOR_RECORDING : "contains"
    BEHAVIOR_RECORDING ||--o{ BEHAVIOR_RECORDING_FILE : "has files"
    EVENT_TYPE ||--o{ EVENT : "labels"
    BEHAVIOR_RECORDING ||--o{ EVENT : "contains"
    BEHAVIOR_RECORDING ||--o{ TRIAL : "contains"
    TRIAL_TYPE ||--o{ TRIAL : "labels"
    TRIAL ||--o{ TRIAL_EVENT : "has"
    EVENT ||--o{ TRIAL_EVENT : "linked by"
    BEHAVIOR_RECORDING ||--o{ BLOCK : "contains"
    BLOCK ||--o{ BLOCK_TRIAL : "groups"
    TRIAL ||--o{ BLOCK_TRIAL : "member of"
```

## Key field semantics

- `event.Event.event_start_time` and `event.Event.event_end_time` are in seconds relative to recording start.
- `trial.Trial.trial_start_time` and `trial.Trial.trial_stop_time` are also on the same recording-time axis.
- `trial.TrialEvent` is the bridge table used for event-in-trial analyses.
- Typical ADAMACS restrictions use `session_id` + `scan_id` (`scan_key`).

## Table-level reference (core)

| Table | Primary key shape | Key attributes used most often |
| --- | --- | --- |
| `event.EventType` | `event_type` | `event_type_description` |
| `event.BehaviorRecording` | `-> Session` | `recording_start_time`, `recording_duration`, `recording_notes` |
| `event.BehaviorRecording.File` | `-> BehaviorRecording`, `filepath` | relative file path for recording source |
| `event.Event` | `-> BehaviorRecording`, `-> EventType`, `event_start_time` | `event_end_time` |
| `event.AlignmentEvent` | `alignment_name` | alignment/start/end event types with time shifts |
| `trial.TrialType` | `trial_type` | `trial_type_description` |
| `trial.Trial` | `-> event.BehaviorRecording`, `trial_id` | nullable `trial_type`, `trial_start_time`, `trial_stop_time` |
| `trial.TrialEvent` | `-> trial.Trial`, `-> event.Event` | event membership of trials |
| `trial.Block` | `-> event.BehaviorRecording`, `block_id` | `block_start_time`, `block_stop_time` |
| `trial.BlockTrial` | `-> trial.Block`, `-> trial.Trial` | block membership of trials |

Note:
- In Element Event / Trial, many imported tables are populated via explicit inserts in ingest workflows (`allow_direct_insert=True` patterns are common).

## `dj.Diagram` views (from `adamacs_analysis`)

These are exported from `adamacs_analysis/notebooks/21_schema_dependency_diagrams.ipynb`.

### Event schema

![Event schema diagram](../assets/db_diagrams/event.svg)

### Trial schema

![Trial schema diagram](../assets/db_diagrams/trial.svg)

These diagrams are not decoration.
Use them as the dependency contract before writing downstream analysis joins.

## ADAMACS-specific conventions

- In ADAMACS workflows, event/trial checks are usually run with `scan_key` restrictions.
- Typical validation pattern:

```python
(event.Event() & scan_key)
(trial.Trial() & scan_key)
(trial.TrialEvent() & scan_key)
```

- Common sync sanity checks:

```python
(event.Event() & "event_type='aux_cam'" & 'event_start_time < "100"' & scan_key)
(event.Event() & "event_type='aux_cam'" & 'event_start_time > "1000"' & scan_key)
```

## Minimal debugging checklist

1. `event.EventType` contains required event names.
2. `event.Event` rows exist for the target `scan_key`.
3. `trial.Trial` rows exist and time windows are non-empty.
4. `trial.TrialEvent` rows exist for expected events.
5. Event times and trial windows use the same recording clock convention.

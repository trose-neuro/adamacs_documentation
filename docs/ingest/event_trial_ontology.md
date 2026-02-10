# Event/Trial Ontology (ADAMACS)

This page adapts the DataJoint Element Event ontology to ADAMACS usage.

Reference: [Element Event concepts](https://docs.datajoint.com/elements/element-event/0.2/concepts/).

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

## ASCII timeline

```text
|----------------------------------------------------------------------------------|
|------------------------------- Session (session_id) -----------------------------|
|---------------------- Recording (BehaviorRecording context) ---------------------|
|------ Block 1 ------|______________|------ Block 2 ------|______________________|
|-- Trial 1 --||-- Trial 2 --|______|-- Trial 3 --||-- Trial 4 --|_______________|
| e(aux_cam) | e(raw_bpod_trial_start) | e(optitrack_frames) | e(raw_bpod_reward) |
|----------------------------------------------------------------------------------|
```

Interpretation:
- Trials are intervals.
- Events are points or spans on the same recording clock.
- `TrialEvent` links events that fall inside each trial window.

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

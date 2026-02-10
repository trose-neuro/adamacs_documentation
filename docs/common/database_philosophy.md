# Database Philosophy

This page rewrites the database philosophy for ADAMACS using two sources of design logic:
- reference pipeline documentation (why labs use this style of database pipeline)
- DataJoint documentation and architecture principles

The goal is not generic "good database practice". The goal is to explain why this approach is necessary for **our specific experimental complexity**.

## Core thesis

ADAMACS is built as an executable relational workflow because modern systems neuroscience experiments are now too complex for ad-hoc files and scripts.

The operating conditions are:
- many modalities per experiment (imaging, behavior, pose, eye, mocap, events)
- many actors (students, analysts, operators, workers)
- long chains of dependent computation
- iterative reprocessing and curation
- closed-loop model-guided experiments

Without a strict dependency graph and machine-readable keys, this system becomes un-auditable and non-reproducible.

## Operational principles (adapted)

The philosophy used in ADAMACS can be summarized as:

1. Ontology before algorithms
   - Define experimental structure (`session`, `scan`, `trial`, `event`) before feature extraction.
2. Keys before convenience
   - Keep stable key grammar even when notebooks evolve.
3. Labels are contracts
   - Shared vocabularies (event/trial types) should be explicit and reusable across users and projects.
4. Provenance is part of the result
   - A value without lineage is not analysis-ready.
5. Diagrams are executable thinking tools
   - Use dependency diagrams to reason about joins and compute order, not just for documentation.

## Reference-Pipeline Reasons (rewritten for ADAMACS)

Reference pipeline docs emphasize that database pipelines are needed to manage large and complex table networks, support multiple user roles, and make it possible to extend workflows to new hardware/data types while preserving structure.

In ADAMACS terms, this means:

1. **Complexity is structural, not accidental**
   - We do not have one stream; we have coordinated streams and derived products.
   - Complexity must be encoded in schema dependencies, not hidden in notebook order.

2. **The pipeline is the collaboration contract**
   - Experimentalists, analysts, and workers need a shared, explicit data contract.
   - Table keys and task tables are that contract.

3. **Generalized schemas beat one-off scripts**
   - New setup variants and modalities appear regularly.
   - A relational dependency model absorbs change better than bespoke scripts.

4. **Discoverability matters**
   - People must be able to inspect dependencies (`dj.Diagram` style reasoning) and understand where values originate.

## DataJoint principles that ADAMACS relies on

ADAMACS depends on DataJoint not only as storage, but as a workflow engine.

1. **Dependencies are executable semantics**
   - Parent-child relations define computation order and provenance boundaries.

2. **Relational workflow model**
   - Data definition + computation linkage are co-located in schema/class design.

3. **Automated population with job reservation**
   - Worker loops can run safely in parallel (`reserve_jobs=True`) without duplicating heavy compute.

4. **Provenance-first design**
   - Derived values are tied to stable keys, parameter sets, and curation versions.

5. **Separation of manual staging and computed execution**
   - `*Task` tables let users stage intent while workers execute under operational permissions.

## Why this is necessary for hypercomplexity

"Hypercomplexity" in this context means the system has all of these simultaneously:
- multimodal recording and synchronization
- continuous model updates
- heterogeneous compute surfaces (CPU workers, GPU workers, human analysts)
- repeated re-ingest/recompute cycles
- closed-loop experiment control informed by previous model outputs

At this point, you need:
- **machine-readable naming conventions**
- **strict key grammar** (`session_id`, `scan_id`, `recording_id`, `paramset_idx`, `curation_id`)
- **task-mediated compute orchestration**
- **worker ownership boundaries**
- **reproducible dependency maps**

Otherwise closed-loop behavior becomes opaque and scientifically unsafe.

## Closed-loop and model training/evaluation rationale

ADAMACS now includes closed-loop paths where model outputs affect future acquisition.

Example loop:
1. ingest multimodal data
2. worker pipelines produce aligned features
3. `GPU_SERVER` runs model training and evaluation (including MEI candidate scoring)
4. evaluated candidates feed stimulation design for `bench2p1`
5. new recordings are produced
6. those recordings re-enter ingest and are versioned in the same dependency graph

This loop is only trustworthy if every transformation step is key-addressable and auditable.

## Philosophy translated to operational rules

1. **Task first, worker second**
   - Users stage; workers execute heavy pipelines.

2. **Never hide state in notebooks**
   - Notebooks are views and analysis surfaces, not implicit pipeline controllers.

3. **Every derived metric must declare lineage**
   - Keep key restrictions, model names, paramset, curation context attached.

4. **Use schema constraints to prevent drift**
   - Enforce conventions in tables and helpers, not only in lab memory.

5. **Optimize for future machine use**
   - Data should be immediately consumable by model training/evaluation pipelines.

## Practical consequence for students

Students should think of the database as:
- a reproducibility engine
- a collaboration engine
- a machine interface for future models

not just a place to "store data".

## References

- DataJoint docs and architecture:
  - https://docs.datajoint.com/core/datajoint-python/latest/design/tables/dependencies/
  - https://docs.datajoint.com/core/datajoint-python/latest/query/operators/
  - https://www.datajoint.com/docs/core/

# Infrastructure Architecture

This is the current documented ADAMACS lab architecture for ingest and analysis operations.

Public-doc note:
- internal endpoint values are intentionally redacted here; request live values from lab ops.

## Server roles and IPs

- `MAIN_SERVER` (`<MAIN_SERVER_IP>`)
  - main DataJoint DB host
  - blob storage host
  - shared data upload host
  - CPU-side worker host
- `GPU_SERVER` (`<GPU_SERVER_IP>`)
  - GPU worker host (DLC/model-heavy/denoising and related jobs)
  - model training and evaluation host (including MEI candidate generation/evaluation workflows)
- `BACKUP_SERVER` (`<BACKUP_SERVER_IP>`)
  - backup host (pull backups + borg compression)

Legacy note:
- some historical scripts/docs still mention `<LEGACY_MAIN_SERVER_IP>`.

## End-to-end dependency graph (PCs, servers, workers, and feedback loop)

```{mermaid}
flowchart TB
    subgraph PCs["Acquisition PCs and setup controllers"]
      PC_M1["PC mini2p1 controller"]
      PC_M2["PC mini2p2 controller"]
      PC_B1["PC bench2p1 controller"]
      PC_A1["PC aux1 controller"]
      PC_A2["PC aux2 controller"]
      PC_H1["PC behavior1 controller"]
      PC_H2["PC behavior2 controller"]
    end

    subgraph SETUPS["Acquisition setups"]
      S_M1["mini2p1"]
      S_M2["mini2p2"]
      S_B1["bench2p1"]
      S_A1["aux1"]
      S_A2["aux2"]
      S_H1["behavior1"]
      S_H2["behavior2"]
    end

    subgraph MAIN_SERVER["MAIN_SERVER MAIN_SERVER_IP"]
      SHARE["SMB/Linux share /datajoint-data/data/<user>"]
      CONS["Consolidation and naming"]
      ING["adamacs_ingest GUI and ingest notebooks"]
      TASK["Manual and *Task tables"]
      DB["DataJoint DB services"]
      CPUW["CPU worker loops (imaging+mocap)"]
      BLOB["External blob storage /datajoint-db/blobs/..."]
      DBDUMP["DB dump outputs"]
      ANA["adamacs_analysis users and notebooks"]
    end

    subgraph GPU["GPU_SERVER GPU_SERVER_IP"]
      GPUW["GPU worker loops (DLC/denoise/cascade)"]
      TRAIN["Model training pipelines"]
      EVAL["Model evaluation and MEI candidate scoring"]
    end

    subgraph BACKUP["BACKUP_SERVER BACKUP_SERVER_IP"]
      RSYNC["Pull jobs (rsync from MAIN_SERVER)"]
      BORG["Borg archives zstd,22"]
    end

    PYRAT["PyRAT API"]
    RSP["RSpace API optional"]

    PC_M1 --> S_M1
    PC_M2 --> S_M2
    PC_B1 --> S_B1
    PC_A1 --> S_A1
    PC_A2 --> S_A2
    PC_H1 --> S_H1
    PC_H2 --> S_H2

    S_M1 --> CONS
    S_M2 --> CONS
    S_B1 --> CONS
    S_A1 --> CONS
    S_A2 --> CONS
    S_H1 --> CONS
    S_H2 --> CONS

    CONS --> SHARE
    SHARE --> ING
    ING --> TASK
    ING --> DB
    TASK --> DB
    ANA --> DB
    DB --> ANA

    PYRAT --> DB
    ING --> RSP
    RSP --> DB

    DB --> CPUW
    DB --> GPUW
    GPUW --> DB
    CPUW --> BLOB
    GPUW --> BLOB

    DB --> TRAIN
    TRAIN --> EVAL
    EVAL --> S_B1
    S_B1 --> CONS

    SHARE --> RSYNC
    BLOB --> RSYNC
    DBDUMP --> RSYNC
    DB --> DBDUMP
    RSYNC --> BORG
```

### Closed-loop note

The `GPU_SERVER` model training/evaluation path feeds MEI candidate stimuli back to `bench2p1` for re-stimulation experiments, and those new recordings re-enter the same ingest pipeline.

## Directory structure and file naming convention visualization

```{mermaid}
flowchart TB
    ROOT["/datajoint-data/data/<username>"]
    SESS["<INITIALS>_<ANIMALID>_<YYYY-MM-DD>_sess<SESSIONID>"]
    SCAN["scan<SCANID>"]
    RAW["Raw files (.tif/.mp4/.tak/.csv/.json etc.)"]
    TOK1["Token: initials (for example XX, YY)"]
    TOK2["Token: animal ID (for example ANM-2172)"]
    TOK3["Token: date (ISO YYYY-MM-DD)"]
    TOK4["Token: session id (sess...)"]
    TOK5["Token: scan id (scan...)"]
    META["Parsed to session_id and scan_id keys"]
    TASK["Task insertion and worker pickup"]

    ROOT --> SESS
    SESS --> SCAN
    SCAN --> RAW
    SESS --> TOK1
    SESS --> TOK2
    SESS --> TOK3
    SESS --> TOK4
    SCAN --> TOK5
    SESS --> META
    SCAN --> META
    META --> TASK
```

### Directory structure (ASCII)

```text
/datajoint-data/data/<username>/
├── <INITIALS>_<ANIMALID>_<YYYY-MM-DD>_sess<SESSIONID>/
│   ├── scan<SCANID_A>/
│   │   ├── <files>.tif
│   │   ├── <files>.mp4
│   │   ├── <files>.tak / <files>.csv
│   │   └── <aux and metadata files>
│   ├── scan<SCANID_B>/
│   │   └── <same pattern as above>
│   └── <optional session-level notes/logs>
└── <more session folders...>

Session folder token convention:
  <INITIALS>_<ANIMALID>_<YYYY-MM-DD>_sess<SESSIONID>

Scan folder token convention:
  scan<SCANID>

Example:
  XX_ANM-2172_2026-02-10_sess9FY6AIRM/scan9FY6AIRM/
```

## ID token structure (`sessid`, `scanid`, `expid`)

This is the practical ID grammar used by ingest/path parsing.
These IDs are token strings carried through folder names and DataJoint keys.

Important:
- these are **not** cryptographic hashes
- do not rewrite existing IDs after data is ingested
- treat them as stable opaque identifiers

### Token prefixes and expected shapes

| Concept | Prefix in filenames | Parser expectation in current code | Typical payload |
| --- | --- | --- | --- |
| Session token | `sess...` | regex extraction of `sess` token from folder string | 8-character base36-like token |
| Scan token | `scan...` | scan token parsed from folder names; scan ingest expects an 8-character scan payload | 8-character base36-like token |
| Suite2p experiment token | `exp...` (inside `suite2p_exp...`) | Suite2p helper writes output folders as `suite2p_exp<token>` | usually matches scan token payload |

### Example mapping

```text
Folder: XX_ANM-2172_2026-02-10_scan9FY6AIRM_sess9FY6AIRM
  session_id = sess9FY6AIRM
  scan_id    = scan9FY6AIRM
  expid      = 9FY6AIRM   (in paths such as suite2p_exp9FY6AIRM)
```

### What the 8-character payload is

In current helper code, these payloads are handled as base36-like IDs and can be converted to timestamps in legacy utility code.
Operationally, this means:
- the token is time-derived in origin
- it is used as the stable key payload
- it should be treated as an ID, not as a value to recompute later

### Implementation pointers (for maintainers)

- Session token extraction: `adamacs/helpers/adamacs_ingest_v2.py` (`get_session_key_from_dir`)
- Scan token extraction: `adamacs/helpers/adamacs_ingest_v2.py` (`get_scan_key_from_dir`)
- Scan ingest expectation: `adamacs/ingest/session.py` (`scan_pattern = "scan.{8}"`)
- Suite2p `expid` folder naming: `adamacs/helpers/s2p_helpers.py` (`suite2p_exp...`)
- Legacy base36-to-datetime helper: `adamacs/helpers/stack_helpers.py` (`convert_id_to_datetime`)

## External references (pipeline components)

Use these when you need implementation details beyond ADAMACS-specific wrappers.

### DataJoint and Elements

- DataJoint core docs: <https://docs.datajoint.com/core/datajoint-python/latest/>
- DataJoint Elements index: <https://docs.datajoint.com/elements/>
- Element Calcium Imaging: <https://docs.datajoint.com/elements/element-calcium-imaging/latest/>
- Element DeepLabCut: <https://docs.datajoint.com/elements/element-deeplabcut/latest/>
- Element Event concepts: <https://docs.datajoint.com/elements/element-event/0.2/concepts/>

### Processing/model toolchains

- Suite2p docs: <https://suite2p.readthedocs.io/en/latest/>
- Suite2p parameters: <https://suite2p.readthedocs.io/en/latest/parameters/>
- Suite2p inputs/outputs: <https://suite2p.readthedocs.io/en/latest/inputs/>, <https://suite2p.readthedocs.io/en/latest/outputs/>
- Suite2p source: <https://github.com/MouseLand/suite2p>
- DISK source: <https://github.com/bozeklab/DISK>
- CASCADE source: <https://github.com/HelmchenLabSoftware/Cascade>
- DeepLabCut docs: <https://deeplabcut.github.io/DeepLabCut/>
- DeepLabCut source: <https://github.com/DeepLabCut/DeepLabCut>

## ASCII interaction sketch

```text
[SETUPS: mini2p1/mini2p2/bench2p1/aux1/aux2/behavior1/behavior2]
                |
                v
      [consolidated session folder]
                |
                v
   [MAIN_SERVER share /datajoint-data/data/<user>]
                |
                v
        [adamacs_ingest GUI/notebooks]
                |
     +----------+-------------+
     |                        |
     v                        v
[DataJoint DB on MAIN_SERVER]   [RSpace optional]
     |
     +--> [*Task tables]
     |
     +--> [MAIN_SERVER CPU workers] ----+
     |                              |
     +--> [GPU_SERVER GPU workers] -+--> [/datajoint-db/blobs/...]
     |
     +--> [DB dumps]

[/datajoint-data + blobs + DB dumps] --> [BACKUP_SERVER pull backups] --> [borg zstd,22]
```

## Operational boundaries

- Ingest users stage metadata/tasks.
- Workers execute heavy populations.
- Analysis users query resulting computed tables.
- Backup host is independent execution surface for resilience.

## Change-control guidance

Any server/IP/process change should be updated in:
- this page (`architecture`)
- `worker_population`
- `backups`
- onboarding pages under `Common`

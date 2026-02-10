# Infrastructure Architecture

This is the current documented ADAMACS lab architecture for ingest and analysis operations.

## Server roles and IPs

- `MAIN_SERVER` (`172.25.64.3`)
  - main DataJoint DB host
  - blob storage host
  - shared data upload host
  - CPU-side worker host
- `GPU_SERVER` (`172.25.70.3`)
  - GPU worker host (DLC/model-heavy/denoising and related jobs)
  - model training and evaluation host (including MEI candidate generation/evaluation workflows)
- `BACKUP_SERVER` (`172.26.65.8`)
  - backup host (pull backups + borg compression)

Legacy note:
- some historical scripts/docs still mention `172.26.128.53`.

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

    subgraph MAIN_SERVER["MAIN_SERVER 172.25.64.3"]
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

    subgraph GPU["GPU_SERVER 172.25.70.3"]
      GPUW["GPU worker loops (DLC/denoise/cascade)"]
      TRAIN["Model training pipelines"]
      EVAL["Model evaluation and MEI candidate scoring"]
    end

    subgraph BACKUP["BACKUP_SERVER 172.26.65.8"]
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

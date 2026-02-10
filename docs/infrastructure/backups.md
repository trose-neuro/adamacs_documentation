# Backups and Data Protection

This page documents the current backup model centered on LOKI.

## Backup host

- `LOKI` (`172.26.65.8`) is the backup server.

## What is backed up

From TATCHU, backup scripts pull:
- `/datajoint-data/` (uploaded and organized data)
- `/datajoint-db/blobs/` (external file blobs)
- DB dump directories (database backups)

## Pull strategy

Backup scripts use `rsync` pull jobs from LOKI to TATCHU endpoints.
Historical script variants reference legacy TATCHU IPs; maintainers should keep these scripts updated with current addresses.

Documented script set (SOP server scripts):
- `backup_tatchu_data.sh`
- `backup_tatchu_blobs.sh`
- `backup_tatchu_database.sh`
- `borg_backup_on_loki.sh`
- optional notification wrappers:
  - `backup_and_notify_on_loki.sh`
  - `backup_and_notify_on_tatchu.sh`

## Borg archival

After pull synchronization, LOKI runs borg archive creation with high compression settings.
Documented pattern includes:
- `borg create --compression zstd,22 ...`
- retention pruning (`daily/weekly/monthly` windows)

## Backup flow graph

```{mermaid}
flowchart LR
    TDATA[TATCHU /datajoint-data] --> RSYNC[LOKI rsync pull]
    TBLOB[TATCHU /datajoint-db/blobs] --> RSYNC
    TDB[TATCHU DB dumps] --> RSYNC
    RSYNC --> BORG[borg archive zstd,22]
    BORG --> RET[retention prune]
```

## Operational recommendations

- Monitor backup logs and failure notifications daily.
- Validate restore paths periodically (not only backup completion).
- Test random restore samples monthly.
- Keep backup scripts under version control and document host/IP assumptions.

## Restore readiness checklist

- verify latest successful pull timestamp
- verify borg repository health (`borg check`)
- verify enough free space for restore target
- verify permissions for restore destination
- verify DB dump compatibility with current DB engine version

## Incident response basics

If TATCHU-side data loss occurs:
1. stop worker writes to prevent further divergence
2. determine loss scope (raw data, blobs, DB, or combination)
3. restore in dependency order:
   - database dumps
   - blob storage
   - data directories
4. run post-restore consistency checks on key tables

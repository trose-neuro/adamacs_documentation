# Backups and Data Protection

This page documents the current backup model centered on BACKUP_SERVER.

## Backup host

- `BACKUP_SERVER` (`<BACKUP_SERVER_IP>`) is the backup server.

## What is backed up

From MAIN_SERVER, backup scripts pull:
- `/datajoint-data/` (uploaded and organized data)
- `/datajoint-db/blobs/` (external file blobs)
- DB dump directories (database backups)

## Pull strategy

Backup scripts use `rsync` pull jobs from BACKUP_SERVER to MAIN_SERVER endpoints.
Historical script variants reference legacy MAIN_SERVER IPs; maintainers should keep these scripts updated with current addresses.

Documented script set (SOP server scripts):
- `backup_main_server_data.sh`
- `backup_main_server_blobs.sh`
- `backup_main_server_database.sh`
- `borg_backup_on_backup_server.sh`
- optional notification wrappers:
  - `backup_and_notify_on_backup_server.sh`
  - `backup_and_notify_on_main_server.sh`

## Borg archival

After pull synchronization, BACKUP_SERVER runs borg archive creation with high compression settings.
Documented pattern includes:
- `borg create --compression zstd,22 ...`
- retention pruning (`daily/weekly/monthly` windows)

## Backup flow graph

```{mermaid}
flowchart LR
    TDATA[MAIN_SERVER /datajoint-data] --> RSYNC[BACKUP_SERVER rsync pull]
    TBLOB[MAIN_SERVER /datajoint-db/blobs] --> RSYNC
    TDB[MAIN_SERVER DB dumps] --> RSYNC
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

If MAIN_SERVER-side data loss occurs:
1. stop worker writes to prevent further divergence
2. determine loss scope (raw data, blobs, DB, or combination)
3. restore in dependency order:
   - database dumps
   - blob storage
   - data directories
4. run post-restore consistency checks on key tables

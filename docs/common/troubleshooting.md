# Troubleshooting

This page captures high-frequency issues seen during ADAMACS ingest and analysis.

## Connection issues

### `SSLV3_ALERT_HANDSHAKE_FAILURE`

Cause:
- DataJoint attempts TLS against a non-TLS DB endpoint.

Fix:
- Set `"database.use_tls": false` in `dj_local_conf.json`.

### Authentication failed

Check:
- username/password in `dj_local_conf.json`
- account exists on DB host
- no hidden spaces or stale copied credentials

## Import and dependency issues

### `ModuleNotFoundError: datajoint` (or similar)

Cause:
- wrong conda env active.

Fix:
- activate expected env
- reinstall dependencies via repo install script

### `scanimage-tiff-reader` install fails

Fallback:

```bash
conda install -c conda-forge scanimage-tiff-reader
```

## Ingest workflow issues

### Session not discovered in GUI

Check:
- naming convention contains expected `sess...` and `scan...` tokens
- folder exists under configured root dirs
- `imaging_root_data_dir` points to correct path

### `scan.ScanInfo.populate()` fails

Common causes:
- no `.tif` in scan folder
- incompatible TIFF header
- wrong scan path in `scan.ScanPath`

### Task inserted but no downstream result

Check:
- corresponding worker service is running
- task row exists in `*Task` table
- jobs are not stuck in reserved/error state

## Permission issues

### Blob write permission denied (`Errno 13` on `.saving` file)

Example symptom:
- permission denied under `/datajoint-db/blobs/.../*.saving`

Cause:
- SQL privilege is present, but filesystem write permission is not.

Fix:
- do not run manual populate for worker-owned blob-heavy tables from personal account.
- insert task rows and let worker account populate.

See `Infrastructure -> Worker-Owned Population`.

## Analysis issues

### Empty query results though ingest ran

Check:
- correct schema prefix in config
- correct key restriction (`session_id`, `scan_id`, `curation_id`, etc.)
- worker completion status for upstream computed tables

### Notebook runs but plots look wrong

Check:
- you selected correct `paramset_idx` and `curation_id`
- you are not mixing old/new DLC model names
- session alignment and timestamp event types are correct

## Performance and storage issues

### Home directory too large / low free space

Recommendations:
- do not store raw data in home
- clean old conda caches: `conda clean --all`
- remove obsolete environments

### Long-running population and silent failures

Check:
- worker logs and Slack notifications
- rerun with `suppress_errors=False` for local debugging only

## Last-resort debugging pattern

1. Restrict to one session/scan key.
2. Confirm all parent tables have rows.
3. Insert exactly one task row.
4. Run/observe one population step at a time.
5. Save full traceback and environment versions.

## Escalation checklist when asking for help

Include:
- exact error traceback
- table + key used
- whether run was manual or worker-managed
- host and username
- relevant `dj_local_conf` non-secret fields (`database.host`, prefix, root dirs)

# `dj_local_conf.json` Reference

`dj_local_conf.json` is the local DataJoint runtime configuration file.

It is **machine-local** and should never be committed.

## File location

Typical placement:
- `/path/to/adamacs_ingest/dj_local_conf.json`
- `/path/to/adamacs_analysis/dj_local_conf.json`

Both repos ship `Example_dj_local_conf.json` templates.

## Minimal required keys

```json
{
  "database.host": "172.25.64.3",
  "database.user": "your_username",
  "database.password": "your_password",
  "database.port": 3306,
  "database.use_tls": false,
  "custom": {
    "database.prefix": "roselab_",
    "imaging_root_data_dir": ["/datajoint-data/data/your_username"],
    "exp_root_data_dir": ["/datajoint-data/data/your_username"],
    "dlc_root_data_dir": ["/datajoint-data/data/your_username"]
  }
}
```

## Important custom keys

- `custom.database.prefix`
  - schema prefix used by this local config
- `custom.imaging_root_data_dir`
  - root directories where imaging session folders are discovered
- `custom.exp_root_data_dir`
  - behavior/aux root directories
- `custom.dlc_root_data_dir`
  - video/DLC root directories
- `custom.dlc_output_dir` (optional)
  - explicit processed DLC output target
- `custom.rspace_URL`, `custom.rspace_API_key` (optional)
  - RSpace integration credentials
- `custom.pyrat_client_token`, `custom.pyrat_user_token` (optional)
  - PyRAT API credentials for subject staging/pull

## TLS setting

If your DB endpoint is non-TLS, set:

```json
"database.use_tls": false
```

This avoids SSL handshake failures seen in some DataJoint `0.14.x` configurations.

## Security rules

- Never commit this file.
- Never post full file contents in public channels.
- Treat API keys and passwords as secrets.

## Quick validation

```bash
python - <<'PY'
import datajoint as dj
print("host:", dj.config.get("database.host"))
print("user:", dj.config.get("database.user"))
print("tls:", dj.config.get("database.use_tls"))
PY
```

Then confirm connection:

```python
import datajoint as dj
dj.conn()
```

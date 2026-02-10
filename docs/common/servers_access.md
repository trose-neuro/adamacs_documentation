# Server Access and Paths

This page summarizes practical server access for ADAMACS users.

## Current server IPs

- `TATCHU3`: `172.25.64.3`
  - primary DataJoint DB host
  - blob storage host
  - share host for ingest uploads
  - CPU worker host
- `ibehaveGPU1`: `172.25.70.3`
  - GPU worker host for model-heavy pipelines
- `LOKI`: `172.26.65.8`
  - backup host (rsync pulls + borg)

## Primary access modes

### SSH

```bash
ssh <username>@172.25.64.3
```

For GPU host:

```bash
ssh <username>@172.25.70.3
```

### SMB share (Windows)

Use the network share endpoint provided by lab ops.

Typical pattern:

```text
\\172.25.64.3\share
```

(or map with `net use`).

### VS Code remote tunnel / remote SSH

Either:
- Remote SSH directly to server hosts, or
- VS Code tunnel workflows if configured by lab ops.

Example tunnel CLI flow on server:

```bash
curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz
tar -xf vscode_cli.tar.gz
./code tunnel
```

Reference:
- https://code.visualstudio.com/docs/remote/tunnels

## SSH key setup (recommended)

Generate key pair locally:

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Copy public key to server:

```bash
ssh-copy-id <username>@172.25.64.3
```

Then test:

```bash
ssh <username>@172.25.64.3
```

## Standard upload path convention

Raw/consolidated data should live under:

```text
/datajoint-data/data/<username>
```

Do not store raw datasets in home directories.

## Jupyter on remote host

Start on server:

```bash
jupyter lab --no-browser --port=8080
```

Forward locally:

```bash
ssh -L 8080:localhost:8080 <username>@172.25.64.3
```

Open local browser:
- `http://localhost:8080`

## Access troubleshooting quick checks

- Ping host IP.
- Validate VPN status if remote.
- Check username/password or key registration.
- Check home directory quotas and permissions.
- Confirm your account has DB and share permissions.

See also:
- `Infrastructure -> Permissions and Ownership`
- `Common -> Troubleshooting`

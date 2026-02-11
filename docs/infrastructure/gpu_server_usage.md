# GPU Server Usage (`GPU_SERVER`)

This page documents practical usage of the lab GPU server for ADAMACS workflows.

## Server and connection

- Host role: GPU compute server for model-heavy workloads (for example DLC, denoising, cascade)
- Permanent IP: `172.25.70.3`
- Legacy note: ignore older references to `172.25.70.6`

Connect via SSH:

```bash
ssh <your_username>@172.25.70.3
```

## Account and security basics

- Keep credentials private and do not store passwords in notebooks, repos, or docs.
- Prefer SSH keys after first login.
- Do not modify system GPU drivers or CUDA installation.
- If credentials were shared by email, move them to a password manager and rotate when needed.

## Usage policy (important)

- Use GPU, CPU, and RAM responsibly (no automatic quota management is assumed).
- Stop jobs and close Jupyter kernels when done.
- Do not run uncontrolled 24/7 jobs.
- Do not occupy all GPUs without coordination.
- Treat this host as compute-first, not storage-first.

## Storage policy

- Home directories are limited and should not hold large datasets.
- Use `/mnt/data` (about 7 TB NVMe) only for temporary, active compute data.
- Store canonical datasets on mounted network shares.
- Clean temporary outputs after runs complete.

## Recommended workflow (headless-first)

The server is intended as a headless compute machine.

Recommended:
1. Develop GUI-heavy steps locally.
2. Use VS Code Remote SSH or terminal SSH for execution on `172.25.70.3`.
3. Run Jupyter on the server only as needed, then shut it down.

Official VS Code Remote SSH docs:
- <https://code.visualstudio.com/docs/remote/ssh>

## Optional GUI path (when required)

Preferred default is local GUI + remote compute.
If remote GUI is unavoidable, use SSH X-forwarding.

### macOS X-forwarding

1. Install XQuartz: <https://www.xquartz.org/>
2. Connect with X-forwarding:

```bash
ssh -X <your_username>@172.25.70.3
```

3. Run your GUI app on the server (example shown for DLC).

For GUI mode in this setup, a lab example is:

```bash
pip install "deeplabcut[gui]==2.3.8"
python -m deeplabcut
```

DeepLabCut docs:
- <https://deeplabcut.github.io/DeepLabCut/>

## DeepLabCut lab note (shared link)

Lab-specific walkthrough (with and without remote GUI):
- <https://share.evernote.com/note/d9f6646d-8072-9e61-4e26-6cc67f216c05>

Note:
- this link may require browser/session support not available in all environments.

## Copy-paste email templates

Use these as quick templates for future communication.

### Access request template

```text
Subject: GPU server account request (172.25.70.3)

Hello,

Could you please create GPU server access for me on 172.25.70.3?
Preferred username: <username>
Use case: <short use case, e.g. DeepLabCut training/inference for ADAMACS>

I confirm I will follow server policy:
- no driver/CUDA changes
- responsible shared GPU usage
- temporary data only on /mnt/data

Thank you.
```

### Acknowledgement template

```text
Subject: Re: GPU server access

Dear <Name>,

Thank you very much for setting up the account and for the detailed instructions.

Best regards,
<Your Name>
```

### Resource coordination template

```text
Subject: Planned long GPU run on 172.25.70.3

Hello,

I plan to run a longer GPU job:
- start: <date/time>
- expected duration: <hours>
- expected GPU usage: <N GPUs>
- workflow: <DLC/denoising/cascade/etc.>

Please let me know if this conflicts with other planned usage.
```

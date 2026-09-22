# Authorization and credential isolation

## Server authorization

Use DWS Device Flow for SSH, CI, Docker, and headless servers. The person authorizing must verify the organization and account in the browser. Do not use a remote browser callback that expects access to the server's `127.0.0.1`.

After authorization, select and pin the exact profile (`corpId:userId`). Every automated command should receive that profile explicitly and should run with the same Linux user, `HOME`, and `DWS_CONFIG_DIR` used during authorization.

Example shape (replace placeholders locally; never print their values):

```bash
sudo -u dwsapp env \
  HOME=/var/lib/dws-integration/home \
  DWS_CONFIG_DIR=/var/lib/dws-integration/config \
  /usr/local/bin/dws auth login --device \
  --client-id '<APP_KEY>' --client-secret '<APP_SECRET>'

sudo -u dwsapp env \
  HOME=/var/lib/dws-integration/home \
  DWS_CONFIG_DIR=/var/lib/dws-integration/config \
  /usr/local/bin/dws profile list --format json
```

If a self-built application is not required, use the organization's approved DWS login mode. Do not put an auth export archive in source control, chat, a normal file share, or a generated artifact.

## Runtime contract

At minimum define:

- `DWS_BINARY_PATH`: pinned, verified CLI path/version;
- `DWS_PROFILE`: exact stable `corpId:userId` value;
- `DWS_HOME`: dedicated home directory (mapped to process `HOME`);
- `DWS_CONFIG_DIR`: dedicated DWS credential/config directory.

A client should copy the process environment, override `HOME` and `DWS_CONFIG_DIR` for each subprocess, and pass `--profile` explicitly. Never read `token.json`, keychains, or encrypted DWS files from application code.

## Health and lifecycle

Expose a safe health result containing status and expiry timestamps, not tokens. `healthy` means usable; `expiring` means the short-lived access token is near refresh but the refresh authorization may still be valid; `expired` means reauthorization or permission repair is required. Typical reauthorization causes are refresh expiry/revocation, disabled user, revoked resource permission, changed runtime directories, partial credential migration, or a changed application authorization.

## Isolation checks

Before enabling a second application on a host, identify its systemd user, `HOME`, and `DWS_CONFIG_DIR`. Explicitly provision a separate home and config directory with restrictive ownership/permissions. If changing another running application or its service unit is required, obtain explicit authorization, back up that unit, and validate its own health after the change.

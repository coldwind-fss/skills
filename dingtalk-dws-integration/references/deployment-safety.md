# Deployment and rollback safety

Before changing a running application, create a new, timestamped backup of the exact production files that may change. Include deployed backend code, the active frontend distribution, service units/drop-ins, and the relevant Nginx site configuration. Do not overwrite an older backup.

Never copy `.env`, databases, DWS credential directories, auth export archives, SSH keys, or unrelated applications into a code release backup. Keep secrets in the host's protected secret mechanism.

Upload only files in the approved change set. Do not replace an entire application directory to deploy a small change. Frontend content changes must produce a new asset hash or an explicit cache strategy; do not change same-named hashed JavaScript while keeping the old hash.

Restart only when needed:

- backend or systemd environment change: `systemctl daemon-reload` and restart the target service;
- Nginx change: run `nginx -t`, then reload only after it passes;
- frontend-only static change: no service restart is normally required.

After deployment, verify the target service is active, local and public health endpoints, page HTTP status, DWS authorization health, and application-level counts. Roll back only the files changed by the release, after taking a fresh timestamped backup. Do not roll back source-group files, production data, credentials, or another application's service as part of an unrelated release.

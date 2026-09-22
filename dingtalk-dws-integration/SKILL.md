---
name: dingtalk-dws-integration
description: Design, implement, verify, and safely deploy reusable DingTalk Workspace CLI integrations for personal-authorized groups, Drive, Docs, and AI Tables. Use when an application needs DWS access; do not use for ordinary web login or enterprise-only Storage APIs.
---

# DingTalk DWS Integration

Use this skill to add DWS-backed DingTalk capabilities to an application without confusing three separate identities: the web-app login user, a DWS personal authorization, and an enterprise application access token.

## Decide the access model first

Default to the fixed-service-principal model: one explicitly authorized DingTalk user runs the backend DWS integration. Do not silently turn a request for one fixed operator into a multi-user credential system. Design per-user profiles only when the user explicitly requests it and accepts the additional credential isolation, account lifecycle, and revocation work.

Use DWS for resources visible to the authorized personal account: groups and group history/files, personal or shared Drive resources, Docs, and AI Tables. Use the enterprise Storage OpenAPI for an application-owned fixed archive directory when stable governance and rollback are required. Use web login only to identify the person opening the UI; it does not grant the backend DWS permissions.

## Non-negotiable invariants

- Authorize on the server with Device Flow; do not depend on a browser callback to a remote `127.0.0.1`.
- Pin a stable `corpId:userId` profile on every DWS call. Never rely on the CLI's current profile.
- Give every application its own Linux user (when practical), `HOME`, and `DWS_CONFIG_DIR`. Never share a credential directory between applications or copy individual token files.
- Keep the DWS credential store behind a subprocess/client boundary. Application code consumes structured results, never access/refresh tokens or the encrypted store.
- Use stable `spaceId`, `folderId`, `baseId`, `tableId`, and `fieldId` values for production targets. Names are display metadata only and must not select or roll back a resource.
- Redact tokens, AppSecrets, authorization headers, device codes, and credential paths from logs, API responses, test fixtures, and chat output.
- Treat reads and writes differently. Default to read-only discovery and a dedicated test target; perform production writes, authorization, migration, or deployment only after explicit user authorization.

## Implementation workflow

1. Inspect the host project, its existing DWS module, runtime user, and deployment files before adding code. Preserve a working production runtime; do not rebuild or replace a production virtual environment merely to make local development convenient.
2. Define a small adapter with structured JSON calls, timeout handling, non-JSON download handling, error redaction, and explicit `HOME`/`DWS_CONFIG_DIR` injection. Keep business rules outside the adapter.
3. Implement only the resource operations the application needs. Preserve DWS pagination, the team-space root-folder rule, and the three-step AI Table attachment flow. See [resource-operations.md](references/resource-operations.md).
4. Add an authorization-health check that reports identity, access expiry, refresh expiry, and status without exposing credentials. Refresh tokens normally renew short-lived access tokens; reauthorization is for expiry/revocation, account or permission changes, or changed runtime identity.
5. Validate in this order: configuration shape, binary/version, exact profile, current-user read, Drive listing, target document/table read, then isolated test writes and rollback if writes are required. The bundled [verify_dws_readonly.py](scripts/verify_dws_readonly.py) is the default smoke check.
6. Before production changes, make a timestamped backup of the exact files being changed and follow [deployment-safety.md](references/deployment-safety.md). Do not upload `.env`, databases, credential directories, or unrelated application files.

## Reference routing

- Read [architecture.md](references/architecture.md) when choosing DWS versus web login or Storage OpenAPI, or when deciding fixed-principal versus per-user authorization.
- Read [auth-and-isolation.md](references/auth-and-isolation.md) for Device Flow, profile pinning, credential directories, and lifecycle checks.
- Read [resource-operations.md](references/resource-operations.md) for CLI command boundaries, pagination, downloads, Drive roots, Docs, and AI Table attachments.
- Read [deployment-safety.md](references/deployment-safety.md) before any service, Nginx, runtime, or production file change.
- Read [troubleshooting.md](references/troubleshooting.md) when a resource is missing, a profile is wrong, or a command returns an unexpected format.

If a requested action would modify another application, revoke authorization, upgrade DWS, or write production data and the user has not explicitly authorized that action, stop and ask for direction.

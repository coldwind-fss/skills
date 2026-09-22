# Architecture and access-model decisions

## Three identities

| Capability | Identity | What it can do |
|---|---|---|
| Web application login | Person currently opening the DingTalk workbench app | Identify the UI user, apply application roles, and record audit context |
| DWS personal authorization | Explicitly authorized DingTalk user and pinned `corpId:userId` profile | Read and operate on groups, group history/files, Drive, Docs, and AI Tables visible to that user |
| Enterprise application access token | Self-built DingTalk application plus a fixed operator where required | Application-owned OpenAPI operations such as a governed archive directory |

The first identity does not grant the second. The second cannot bypass DingTalk ACLs. The third is not a replacement for personal group-history or personal-document access.

## Default deployment shape

```text
UI -> application API
       ├─ web-login identity (UI authorization/audit)
       ├─ DWS adapter -> dws CLI -> isolated personal credential store
       └─ Storage adapter -> DingTalk OpenAPI -> fixed archive target
```

Keep business orchestration, idempotency, retries, field mapping, and rollback outside the DWS adapter. The adapter should return stable IDs and structured data, not CLI text or credentials.

## Fixed principal versus per-user profiles

The fixed-principal model is the safe default for background workflows: one approved operator, one service runtime identity, one pinned profile, and one auditable permission boundary. It is appropriate when a workflow must run without a user keeping a browser open.

The per-user model requires an explicit mapping from application user to DWS profile, a separate encrypted credential directory for every profile, revocation and offboarding handling, and authorization-health reporting per account. Do not introduce it as an incidental convenience.

## Resource-target policy

Resource names can be shown to people, but production selection and rollback must use IDs returned by a trusted discovery step. A same-name Drive folder or AI Table may be a test copy. Store `spaceId`, `folderId`, `baseId`, `tableId`, `fieldId`, source message IDs, and source file IDs as part of the business record when those operations are used.

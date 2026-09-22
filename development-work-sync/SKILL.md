---
name: development-work-sync
description: Summarize a scoped development conversation into clean, reviewable product work records, preserve phase details under each record, and sync confirmed records to an authenticated project-management API.
---

# Development Work Sync

Use this skill when the user asks to summarize, register, sync, or write back development work from the current conversation or an explicitly scoped work session.

The goal is a small set of product-level records that the user can confirm. Do not turn every planning message, code change, deployment, test, or CSS adjustment into a separate top-level record.

## Workflow

Follow this order before drafting records:

1. Determine the source scope. Prefer the user's date range or explicitly named task/thread set. Otherwise run cumulative reconciliation from the latest successful sync checkpoint for the same target project through the current conversation. The checkpoint limits the incremental write scope; it must not be used as an excuse to inspect only the latest few turns. If no checkpoint exists, inspect all relevant history that is actually available and mark the result incomplete when older source threads cannot be read. Do not silently summarize unrelated conversations or projects.
2. Resolve the destination project by repository, project name, or alias. A project must be an exact, unambiguous match. Never create a project as a side effect.
3. Read the destination schema, the complete non-deleted L3 records for the target L2 project, each record's detail and activity data when available, and the target's prior sync batches/checkpoints when the adapter exposes them. This is required to distinguish a new product outcome from a missing phase of an existing outcome.
4. Extract only verified outcomes from the full accessible conversation scope, repository changes, build/test/deploy results, and explicitly named task threads. A request or proposal is not evidence of completion. Never silently reduce a long conversation to the most recent two rounds.
5. Group related work into product-level records. Put the meaningful phases beneath the parent record as `subRecords`; put chronological implementation events into `logs` when they are useful evidence.
6. Compare each parent candidate semantically with existing records and label it `create`, `append`, `skip`, or `needs_review`.
7. Show a clean confirmation preview. Do not write external data until the user confirms, unless the same user message explicitly authorizes writing.
8. After confirmation, commit one idempotent batch through the authenticated adapter and return created/existing IDs and links. Never expose credentials.

## Product-level decomposition

Create a separate top-level record only when the outcome is independently understandable and has a distinct acceptance result, user value, or release boundary. Use these questions:

- Can a user or manager describe the result without explaining the entire development process?
- Could it be accepted, released, or rolled back independently?
- Does it change a distinct product capability, module, integration, defect, or confirmed design decision?

If the answer is mostly no, keep it under the related parent record.

Examples that normally belong under one parent record:

- business confirmation, product design, data-model work, migration, page changes, testing, deployment, and rollback for one lifecycle redesign;
- API implementation, idempotency, production deployment, connectivity testing, and test-data cleanup for one integration;
- several small UI changes made to support one route or one user workflow.

Do not use the number of sub-records as the number of L3 records. A broad initiative can have one parent record with several phase descriptions.

If a phase itself has an independent user-facing result and acceptance boundary, promote it to a separate parent record. Otherwise keep it as a `subRecord`.

## Canonical record shape

Generate this shape before mapping it to the destination system:

```json
{
  "title": "独立、可说明产品结果的主记录标题",
  "kind": "feature|refactor|bug|ui|design|business|integration|validation|operations",
  "phase": "in_progress",
  "developerOwner": "真实开发负责人",
  "businessOwner": "真实业务负责人或需求提出人",
  "priority": "source-specific or null",
  "impact": "source-specific or null",
  "effort": "small|medium|large or source-specific",
  "effortScore": 0,
  "summary": "面向使用者的一句话产品结果",
  "acceptance": "可验证的完成标准或当前验收边界",
  "workDate": "YYYY-MM-DD",
  "subRecords": [
    {
      "title": "阶段或分记录标题",
      "kind": "business|design|refactor|feature|validation|operations",
      "summary": "该阶段实际完成的内容",
      "workDate": "YYYY-MM-DD",
      "effortScore": 0,
      "sourceRefs": ["conversation/task/file reference"]
    }
  ],
  "logs": [
    {
      "type": "progress|problem|delivery|next_step",
      "content": "具体工作动态或验证证据",
      "occurredAt": "YYYY-MM-DD HH:mm"
    }
  ],
  "sourceRefs": ["conversation/task/file reference"]
}
```

`subRecords` are descriptive phase details, not independent L3 records and not yet L4 database rows. Keep them out of the top-level count and do not create one `requirement_work_logs` row for each sub-record merely because it exists in the summary.

## Cross-conversation access and authentication

The skill is an instruction bundle, not a persistent login session or an always-on API connector. A new conversation can write directly only when its runtime provides both:

- a direct HTTP/API or connector tool for the target system; and
- an unexpired authenticated session or least-privilege service credential with the required write action.

For the internal PM adapter, the preferred cross-conversation path is the
runtime-injected `X-PM-Work-Sync-Token`. This narrow service credential is
scoped to work-intake operations; it is not the user's DingTalk session and
must never be copied into this file. The runtime may provide it through a
connector, secure credential store, or environment-backed wrapper. The skill
may reference the credential by name, but must not read it into the
conversation, print it, persist it, or include it in a preview.

On the configured local host, use the bundled `scripts/work_sync_api.py`
transport when direct HTTP calls need a stable implementation. It loads the
credential from `PM_WORK_SYNC_TOKEN` or the user-only credential file selected
by `PM_WORK_SYNC_CREDENTIAL_FILE`; it does not accept a token on the command
line. Use its `schema`, `projects`, `requirements`, `batch`, `sync`,
`owner-correction`, and `rollback` commands as the adapter operations. If the credential is absent,
stop before mutation and report the missing runtime prerequisite.

The browser is not part of the write path. Do not open a browser, scrape a DingTalk webview, or ask the user to re-login as a fallback for a missing API session. If direct transport or authentication is unavailable, stop before mutation and report exactly which prerequisite is missing. A self-developed application still needs this application-level identity and authorization so that a public endpoint cannot accept anonymous writes or misattribute work.

Likewise, a new conversation does not automatically contain every earlier conversation in the account. Read earlier tasks/threads only when they are available through the current runtime and are within the user-authorized project scope. If older history is unavailable, do not claim a complete backfill; show the missing history boundary in the preview and ask for the relevant thread IDs, date range, or handoff material.

## Status rule for generated records

For records generated by this skill, default the parent `phase` to `in_progress`, even when the source evidence shows that code has been deployed. This keeps automatic registration conservative and lets the developer confirm delivery separately. The current internal adapter maps this to `进行中` (the UI may call it “开发中”). Do not auto-write `已交付` unless the user explicitly confirms that status.

Sub-records may describe completed phases in natural language, but their wording must not silently change the parent status.

## Workload mapping

Do not use the number of parent records as a proxy for effort. Calculate the parent workload from the combined scope of its sub-records and verified work. Keep both a display level and, when the target supports it, a numeric score.

Score these dimensions from 0 to 2:

- product scope: field/page, workflow, module, or cross-module;
- engineering complexity: ordinary UI, full-stack linkage, data model, or architecture/integration;
- data and risk: no migration, field migration, historical backfill, or rollback risk;
- collaboration: single owner, business confirmation, multi-team, or external system;
- verification and release: ordinary check, regression, production connectivity, or rollback verification.

Use the aggregate score as guidance:

- 1–3: `small`;
- 4–7: `medium`;
- 8 or more: `large`.

Do not double-count the same effort in both a parent and a sub-record. The parent `effortScore` is the aggregate; each sub-record score explains its contribution. If the destination has a numeric effort/story-point field, map the aggregate score there. If it only supports small/medium/large, map the level and retain the score in the parent detail text when useful.

## Current internal adapter mapping

The skill is system-agnostic. Discover the target schema for every project. For the current internal project-management system only:

- The canonical production API base is `https://xzkj.flipbeltchina.com/pm/api`. Use this HTTPS domain for both reads and writes; do not derive the endpoint from historical baseline notes, old IP addresses, or an old server filesystem path.
- Read the live adapter before a sync with `GET /projects`, `GET /requirements/live?projectId=<L2 id>`, and `GET /work-intake/schema`. Use `/requirements/live` for verification so the result comes from the current database rather than a cached legacy route.
- For direct cross-conversation sync, prefer the runtime-injected `X-PM-Work-Sync-Token` header. It is scoped to reading PM sync context, committing `/work-intake`, correcting owner fields on records created by the same service, and rolling back batches created by the same service. If it is unavailable, an active `X-PM-Session` may be used for a normal authenticated editor/admin flow. Do not fall back to browser login.
- Write confirmed records with `POST /work-intake` using `mode: "commit"`, the resolved L2 `projectId`, a stable `idempotencyKey`, and either the runtime-injected service header or the current authenticated `X-PM-Session`. The credential must come from the active connector/runtime; never put a token, SSH key, or server credential in this skill, a prompt, or a report.
- After a commit, re-read the batch and `/requirements/live` from the same canonical domain and verify the created IDs, status, detail text, and excluded records. If the live endpoint and the configured deployment disagree, stop and resolve the deployment target before mutating data.

- destination project maps to L2;
- each confirmed parent record maps to one L3;
- `subRecords` are serialized into the L3 requirement detail/description field under a clearly labeled section such as `阶段分记录`;
- the parent `summary` remains the short product-level description;
- `developerOwner` maps to the L3 developer owner/assignee, and `businessOwner` maps to the L3 business owner/requester. These must be real people, never the integration service identity; they are required for service-authenticated commits;
- chronological `logs` map to L3 work-dynamic entries;
- `effort` maps to the L3 work-quantity level and `effortScore` maps to story points when supported;
- no L4 table is assumed or created in this phase.

The serialized detail should be human-readable, for example:

```text
产品结果：完成 L3 生命周期与需求底库体系重构。

阶段分记录：
1. 业务确认：明确 L3 既是开发台账，也要在展示端体现 L2 产品生命周期。
2. 产品设计：确定类型、状态、产品影响、工作量和展示路由的收紧方案。
3. 技术建设：完成数据模型、接口校验和前端录入展示调整。
4. 数据补录：完成历史记录的字段补录和批量校正。
5. 验证交付：完成构建、部署和生产环境验证。
```

If a future target supports real child records, the adapter may map `subRecords` to that child entity, but the parent record and its product-level summary must remain intact.

## Matching and sync decisions

Use semantic matching, not title equality alone. Consider project, product/module, outcome, time scope, and whether the existing record is an earlier release or the same unfinished work.

- `create`: a distinct outcome not already represented;
- `append`: the same continuing outcome or a new dynamic for an existing record;
- `skip`: already fully represented with no new verified evidence;
- `needs_review`: possible duplicate, ambiguous project, conflicting status, or insufficient evidence.

A later redesign of an old module may be a new parent record if it has a distinct product outcome and release boundary. In that case, reference the earlier record in `sourceRefs` or the summary rather than merging unrelated releases.

Use a stable idempotency key derived from source scope, resolved project, and approved parent/sub-record content. Re-running the same scope must not duplicate parent records or logs.

## Cumulative reconciliation and backfill

When the target project has been developed across many conversations, follow this reconciliation sequence:

1. Read the exact L2 project and all of its existing L3 records, including each description, phase section, work log, status, and source reference. Read prior successful sync batches/checkpoints if the adapter provides a history endpoint.
2. Build a coverage map. For each product-level parent, record which lifecycle phases, verified outcomes, work dates, source ranges, and logs are already represented. Treat an existing parent with missing phases as a partial record, not as evidence that the whole project is complete.
3. Assemble the source evidence from the current conversation plus every accessible, explicitly in-scope earlier task/thread since the checkpoint or requested start date. Use repository and deployment evidence to distinguish completed work from proposals. Do not use an arbitrary turn-count limit such as “latest two rounds.”
4. Reconcile the evidence against the coverage map. Add only missing phases/details to a matching parent; create a new parent only for an independently understandable outcome or a distinct release boundary; skip evidence already represented. Preserve the existing parent title and details when appending.
5. Show the user the coverage result before writing: existing phases, missing phases, new parent records, appended details, excluded proposals, and any inaccessible history boundary. The parent count is the number of product outcomes, not the number of conversations or phases.
6. On commit, use an idempotency key that includes the target project, source coverage range, source-history fingerprint, and approved content. If the adapter cannot safely append missing detail to an existing parent, mark it `needs_review` instead of creating a duplicate or overwriting the record.

## Interaction modes and response format

Support these modes:

1. `summarize`: return candidate parent records and their `subRecords`; do not mutate.
2. `preview`: resolve the project, read existing records, and show clean parent-level decisions.
3. `commit`: after explicit confirmation, submit the approved batch.
4. `append`: add verified new logs or phase details to an existing matching parent without creating a duplicate.

For `preview`, show only:

- source scope and target project;
- total parent-record count and total sub-record count;
- each parent title, type, status, impact, workload, and decision;
- its phase descriptions indented beneath the parent;
- excluded planned/unverified items, if any.

Hide canonical enum names, payloads, idempotency keys, implementation diagnostics, and adapter details unless an error or user request requires them. The preview should read like a clean confirmation list:

```text
目标项目：IT项目协作空间
待确认：1 条主记录，5 条阶段分记录

1. L3 生命周期与需求底库体系重构
   类型：技术建设｜状态：进行中｜影响：核心｜工作量：大
   结果：……
   阶段：
   - 业务确认：……
   - 产品设计：……
   - 技术建设：……
   - 数据补录：……
   - 验证交付：……

请回复：确认写入／修改第1条／删除第3阶段／取消
```

For `commit`, return the same concise summary plus created/existing IDs, links, failed items, and whether the batch was fully or partially written. Keep the parent product digest separate from the detailed ledger.

## Authentication and safety

Write only through an authenticated API or connector. Do not automate browser login, scrape a DingTalk webview, or depend on visual UI state. Use a least-privilege credential stored outside prompts, source files, and reports. Never expose access tokens.

Preview and summarize are read-only. A confirmed commit must resolve the target, validate the live schema, preserve historical `workDate` and `occurredAt` separately from write time, and stop before mutation if authentication, project identity, or required fields are ambiguous.

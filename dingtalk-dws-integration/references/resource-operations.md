# Resource operations and known DWS boundaries

## Groups and conversations

Use `chat list-all-conversations` for the authorized user's visible conversations, then exclude `singleChat` entries when populating a group selector. Respect `hasMore` and `nextCursor`; a `--limit 100` first page is not a complete result when `hasMore=true`. A group absent from the result usually means the authorized user is not a member, lacks history/file visibility, or the resource belongs to another organization. DWS cannot bypass that boundary.

## Drive

List spaces before browsing. For a team-space root, pass only `--space-id`; passing a `rootFolderId` as `--folder` can produce `RESOURCE_NOT_FOUND`. Pass `--folder` only when entering a real child folder. Persist returned stable IDs.

Downloads are file operations, not JSON operations: use a separate subprocess path, an explicit output path, and verify the output exists and is non-empty. Do not parse download progress from stdout as JSON.

## Docs and AI Tables

Read the target document/table fields by stable IDs before writing. AI Table attachments are a three-step operation:

1. Prepare an upload and obtain `uploadUrl` plus `fileToken`.
2. PUT the binary to `uploadUrl` with the correct `Content-Type`.
3. Create the record using the `fileToken` in the attachment field.

Do not treat an upload preparation response as a completed attachment. Before creating a production record, query by a business idempotency key or source IDs and skip an existing record.

## Error and output boundary

Use structured JSON for JSON commands and a separate non-JSON path for file downloads. Redact `accessToken`, `refreshToken`, `clientSecret`, `appSecret`, bearer values, device codes, and sensitive command output before raising or logging an error. Preserve the useful error category and stable target ID for the business layer.

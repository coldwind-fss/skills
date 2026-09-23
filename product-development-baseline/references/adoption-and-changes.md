# Existing Project Adoption and Change Handling

Use this reference when the repository predates the baseline method, has incomplete documentation, or the current request changes established behavior.

## Adopt an existing project

1. Inspect existing instructions, product/design documents, Git state, and files relevant to the current request.
2. Find the current source of intent. Reuse the existing baseline or connect its authoritative documents through a short index. Keep existing paths and terminology where practical.
3. Compare three views: user-confirmed intent, observed implementation, and unknowns. A working implementation is evidence of current behavior, not proof of intended business policy.
4. For an undocumented project, write only the minimum context needed for the current material change. Mark inferred facts as observations or assumptions. Do not backfill every past feature or label inferred behavior as approved.
5. Report material conflicts and assess the current task's impact. Continue independent work that does not depend on an unresolved decision.

Do not infer that an old repository needs a redesign, data migration, new database, new directory layout, or retrofit to every new convention merely because the baseline skill is active. Determine the need from the user's scope and the inspected project.

## Choose the right implementation shape

Record the order that fits the project. Stable, conventional applications can proceed by technical layers or modules, such as environment/database, backend APIs, frontend integration, and system acceptance. A cohesive feature slice or prototype is useful when it reduces a concrete uncertainty. Do not require each feature to be a tiny independently reviewed unit; group related behavior so the work remains efficient and testable.

## Classify a requested change

| Class | Questions | Typical record |
|---|---|---|
| Bug fix | Does intended behavior stay the same? | Issue/reproduction, focused code/test change, result |
| Feature | Which confirmed user flow and existing rules does it extend? | Work-package spec, API/data impact, acceptance |
| Business change | Do scope, workflow, state, domain meaning, or responsibility rules change? | User-confirmed decision and affected business baseline/model |
| Technical change | Do module ownership, shared API conventions, security boundary, or data-change rules change? | Technical baseline update; decision record if consequential |
| Discussion only | Has the user asked for analysis or planning rather than implementation? | Proposed options, no implied approval or code change |

Only update affected material. A bug fix does not rewrite the PRD when business intent is unchanged. A specific endpoint change does not rewrite shared API rules when those rules remain valid. A shared rule change updates the technical baseline and identifies affected endpoints/modules.

## Preserve approval and context

- Track approval against the actual scope and decisions, not vague labels such as “phase complete.”
- A confirmed plan or spec remains authorized while its scope and material assumptions remain unchanged. Do not repeatedly ask for the same approval.
- Ask for a decision only when a material product, data, authorization, compatibility, or external-action choice is missing and cannot be safely inferred. State the options and impact. Continue unrelated safe work.
- On resume, report the baseline used, current work-package status, relevant Git state, verification completed, blockers, and next action. Do not require full chat history.
- Keep current decisions in the baseline; keep significant rationale in the linked change spec or decision record; keep the actual code history in Git. Do not use an append-only transcript as the baseline.

## Optional repository `AGENTS.md` snippet

Adapt this short reminder when a project needs a repository-local entry point. Preserve existing instructions and avoid copying the full skill into each project.

> For application work, read the current product baseline and relevant work-package spec before changing behavior. Inspect the corresponding code and Git state. Keep confirmed intent separate from observed implementation. For material changes, record scope, affected business/technical decisions, and acceptance; update only affected baseline sections. Follow the project's chosen implementation order. Report what was implemented and verified, and leave open items and Git status clear.

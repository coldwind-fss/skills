---
name: product-development-baseline
description: Apply a lightweight, traceable workflow when creating, continuing, extending, or materially changing a software application with business, architecture, API, or cross-session decisions. Use the existing project baseline, plan proportionate work, and keep approved intent aligned with implementation and verification. For isolated fixes, use only the relevant parts of the workflow.
---

# Product Development Baseline

Keep project decisions usable across coding sessions. The skill describes how to work; the repository records what is true for this application; source code, tests, and Git record what exists and what was verified. Adapt the depth and implementation order to the product. Do not turn this workflow into a fixed waterfall or a requirement to produce a document for every conversation.

## Start or resume the work

For an application task that spans decisions, features, or sessions:

1. Inspect the repository instructions, current product baseline or linked product documents, the relevant work-package spec, Git status, and only the code/tests needed for this request.
2. Briefly establish which decisions and scope govern this task, what remains open, how the code behaves now, and the next useful action. Keep intended behavior and observed implementation separate.
3. Classify the request: product discussion, new application, feature, material business/technical change, narrow fix, or continuation. Do not turn a question or planning request into code changes.

Reuse the project's current authoritative documents and paths. Do not create a competing baseline because its name or layout differs from the template. For an undocumented existing application, infer only the context needed for this task, label observations and assumptions, and avoid reconstructing an unverified history.

If the request is narrow, apply only relevant checks. Do not require a full PRD, architecture review, or feature spec for an isolated fix that leaves recorded behavior and interfaces unchanged.

For a new application, establish the business intent before settling implementation details: clarify the product problem and scope, design the important workflows, and model the in-scope domain objects and relationships. Review that business baseline before defining the architecture and shared API conventions. Then prepare the overall delivery plan and its acceptance direction. If the user has already confirmed these decisions in an earlier session, use them and continue from the next unfinished part instead of restarting discovery. Do not make virtual-environment setup a prerequisite for product analysis.

## Maintain the business and technical baselines

Keep one clear entry point for the current confirmed intent, by default `docs/PRODUCT_BASELINE.md`. Link supporting documents such as a detailed workflow, ER diagram, architecture note, or OpenAPI file when they improve readability. If the project already has authoritative documents elsewhere, link and maintain those instead of duplicating them.

The business baseline captures the product problem, users, scope and non-goals, important workflows and states, domain concepts, relationships, rules, and business acceptance. The technical baseline captures only the conventions needed to build and evolve the application: technology constraints, module responsibilities and dependencies, data ownership, shared API rules, and relevant permission, configuration, logging, testing, and database-change practices. Distinguish business roles from application authorization roles when both exist.

Agree on shared API conventions before endpoints accumulate; define the concrete request and response contract for each work package as it enters implementation. Leave later feature details open until their scope is ready.

Mark decisions as confirmed, proposed, open, or out of scope. An AI proposal does not become a decision until the user confirms it. A baseline describes current accepted intent; keep material decision history in a concise change record or architecture decision record, not in a chat transcript.

## Plan delivery without forcing one implementation order

Make an implementation plan proportionate to the application. It should show useful delivery groups, dependencies, observable outcomes, and acceptance direction. Choose a practical order based on requirement stability, technical dependencies, integration risk, and team capacity. Layer-first, module-first, process slices, or a combination can all be appropriate.

For a small application with stable requirements, it can be efficient to establish the environment and database, implement the main backend modules and APIs, then connect the frontend and verify the whole flow. Integrate at meaningful checkpoints so major interface mismatches are found before the end. For uncertain interactions or high-risk integrations, consider an early prototype or one real end-to-end path. Neither is mandatory for every project. Do not predesign every future endpoint or add production infrastructure before it is needed.

## Specify and implement a work package

Before a material feature or planned work package, prepare a concise spec that states:

- purpose and links to the governing baseline decisions;
- in-scope behavior and exclusions;
- affected workflows, data, modules, APIs, permissions, and compatibility, when relevant;
- implementation sequence or dependencies at useful granularity;
- observable acceptance conditions and needed verification.

Present an unconfirmed spec for review before implementing that scope. Record what the user approved and any still-open decisions. Approval of a roadmap alone does not silently resolve material business, data, authorization, or breaking API choices. When a prior explicit approval already covers the current scope and decisions, continue without asking the user to approve the same thing again. Routine implementation and debugging within approved scope do not need per-file or per-endpoint approval.

Before changing code, inspect existing modules, routes, data relationships, tests, and conventions relevant to the package. Reuse the established design where it fits; explain a material conflict or required deviation. Do not silently expand scope or treat accidental implementation as the business rule.

## Classify changes and update only what they affect

| Change | Record and update |
|---|---|
| Bug fix with no intended behavior change | Reproduction, code/test change, and verification; leave product decisions unchanged |
| Feature within the current baseline | Work-package spec, delivery status, and acceptance evidence |
| Change to product scope, workflow, domain meaning, or business rule | Confirm the change and update the affected business baseline, model, interfaces, and acceptance criteria |
| Change to a specific API | Update its canonical API contract, affected callers, compatibility notes, and tests |
| Change to shared architecture or API conventions | Update the relevant technical baseline; record consequential trade-offs as a concise decision record |
| Discussion or unapproved proposal | Keep it marked as proposed/open; do not implement dependent behavior |

Do not rewrite every baseline for every change. Do not create a separate long report for routine edits. Keep the current baseline concise and current; use the work-package spec or a material decision record to preserve why a significant change happened.

## Verify and leave a usable checkpoint

At the end of a work package or meaningful session checkpoint:

1. Update implementation and verification status separately. Distinguish automated checks, manual/business acceptance, and release; claim each only with evidence.
2. Record material changes, the reason, impacted baseline/API areas, results, unresolved issues, and the next actionable work. Link a Git commit when one exists; state when changes remain uncommitted.
3. Check Git status and preserve unrelated user changes. Do not stage, commit, push, deploy, migrate data, or contact an external system unless it is within the user's explicit request or existing authorization.

When resuming, read the current baseline, the relevant work-package spec and decision record, and Git status. Continue from the recorded checkpoint; do not replay the whole conversation or redo completed work. If code, tests, and accepted intent disagree, describe the discrepancy and resolve it against confirmed intent or a newly confirmed decision.

## Reference material

- For onboarding an existing or undocumented project, classifying changes, and resuming after context loss, read [references/adoption-and-changes.md](references/adoption-and-changes.md).
- For a new project baseline, adapt [assets/product-baseline-template.md](assets/product-baseline-template.md).
- For a material feature or change, adapt [assets/work-package-spec-template.md](assets/work-package-spec-template.md).

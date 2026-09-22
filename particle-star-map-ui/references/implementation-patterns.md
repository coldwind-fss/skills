# Implementation patterns

## Data contract

Keep a renderer-neutral graph shape such as:

```ts
type StarNode = {
  id: string;          // stable internal id, never a display name
  kind: string;        // application-defined category, used for color and filtering
  label: string;
  parentId?: string;
  nativeId?: string;   // optional provider-native identifier
  maskedMeta?: string;
};
type StarEdge = { source: string; target: string; relation: string };
```

Normalize API records once, then pass the normalized graph to the renderer. Keep authorization and visibility filtering on the server and treat labels as untrusted display text.

## Deterministic constellation layout

1. Select the view anchor from the route's focus node. Prefer the business-defined direct parent/owner/dependency relation; otherwise use the focus node itself. Do not pick the center by array order.
2. Partition nodes into direct neighbors, second-order neighbors, and background context. Place direct neighbors on 1–2 rings with a golden-angle offset; place context nodes on wider rings. Sort each partition by `kind`, then `id`.
3. Apply deterministic jitter from a hash of `id` and a bounded minimum-separation relaxation (roughly 50–80 iterations is enough for small graphs). Clamp to the canvas and leave a safe label margin.
4. Cache positions by graph fingerprint and viewport. Recompute only when the graph or viewport changes; selection must not trigger a layout pass.

For a small SVG implementation, a fixed `viewBox` with a transform for pan/zoom is easier to keep stable than absolute DOM positioning. Use `pointer capture` for drag and multiply pointer deltas by a modest configurable factor (for example 1.5–2.0), then clamp zoom to a safe range.

## SVG visual recipe

- Background: `#080e18` to `#0d1522` gradient, with low-opacity dot particles on a separate non-interactive layer.
- Node core: filled circle by object kind, 1.5–2px colored stroke, soft shadow/glow only for the active node.
- Inactive ring: approximately 32px radius; active core: approximately 30px radius with inner ring around 58px and outer ring around 80px. Scale these as design tokens so responsive views can tune them together.
- Labels are centered below the core, use a readable monospace/serif-compatible fallback, and clamp to one or two lines with ellipsis. Do not put long labels inside the circle.
- Edges are straight SVG lines with low-opacity strokes. Active edges may use a brighter stroke and a short transition; avoid curved elbows and animated force lines when matching the reference.

## Migrating an existing graph page

- Keep the existing graph engine for any legacy/light theme, but mount the particle renderer as a separate branch. Before switching branches, destroy the old engine instance and detach its listeners; leaving both renderers alive is a common source of duplicate canvases, stutter, and blank refreshes.
- Make theme state explicit and persist only the user-facing preference. On route entry, derive the center from the route focus node and normalized graph, not from a stale previous selection.
- Render the page shell and loading/error state independently from graph data. An API timeout should produce a visible retry message (around 10–15 seconds is a reasonable default), not an unhandled promise or all-white page.
- When integrating with an existing API, verify the full chain in order: normalized response, component props, SVG node count/labels, click state, and only then deploy. A successful HTTP response alone does not prove that the graph is interactive.

## Test matrix

Check these cases before handoff:

- Empty graph, one node, and a dense graph with duplicate display names.
- Focus node belongs to each application-defined category and has direct, indirect, or peer relationships.
- Click/keyboard activation, click background to clear, drag from empty space, drag after selecting a node, wheel zoom, and resize.
- Slow API, timeout, 401/403, malformed relationship record, and a node removed between refreshes.
- `prefers-reduced-motion: reduce` and a narrow viewport.

Record screenshots only as QA artifacts; never store production credentials or raw personal data in the skill.

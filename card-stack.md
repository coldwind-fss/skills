# Card Stack Style

> 3D card stack layout with Z-axis depth, hover shuffle, and 3D peel.
> Source: https://www.stylekit.top/styles/card-stack
> Verified Aug 2026.

A complete visual style kit for generating Card Stack UI — web pages, dashboards, mobile apps, onboarding flows. Works in any Tailwind CSS environment (CDN, PostCSS, or framework). One file. Copy, paste, replace placeholders.

---

## When to use

- "Stacked cards" / "card deck" / "card carousel" / "swipeable cards" UI
- Pricing page with stacked tiers
- Tinder-style product browser
- Multi-step onboarding with stacked step cards
- Hero or feature area that needs "depth" or "3D" or "shuffle" feel

## When NOT to use

- Dense data tables (cards obscure data)
- Forms longer than one viewport (motion distracts)
- Pages where every section needs focal-point weight (stack pulls focus)

---

## Tokens

### Colors

| Token | Hex | Tailwind | Usage |
|---|---|---|---|
| Primary | `#1a1a2e` | `bg-[#1a1a2e]` | Body bg in light contexts |
| Secondary | `#f0f0f5` | `bg-[#f0f0f5]` | Card surface alt |
| Accent 1 | `#6c5ce7` | `bg-[#6c5ce7]` | Primary accent, top bars, focus |
| Accent 2 | `#00cec9` | `bg-[#00cec9]` | Secondary accent |
| Accent 3 | `#fd79a8` | `bg-[#fd79a8]` | Tertiary accent |
| Accent 4 | `#ffeaa7` | `bg-[#ffeaa7]` | Quaternary accent |
| Text primary | — | `text-zinc-900` | Headings, body on white |
| Text secondary | — | `text-zinc-600` | Body copy |
| Text muted | — | `text-zinc-400` | Meta labels, captions |
| Section dark bg | — | `bg-gradient-to-br from-slate-900 to-slate-800` | Dark feature sections |
| Card surface | — | `bg-white` | All cards |
| Border | — | `border-zinc-200` | Subtle borders on inputs/outline buttons |
| Button primary | — | `bg-zinc-900 text-white` | Filled button |
| Button accent | — | `bg-[#6c5ce7] text-white` | Accent button |
| Hero bg | — | `bg-[#6c5ce7]` | Hero section (purple) |

Use only the 4 accent hex values. Do not introduce a 5th.

### Typography

- Use `font-sans` (Tailwind default). Do **not** import display fonts (Inter, Roboto, Geist, Fraunces, Plus Jakarta Sans are banned — they're overused in AI output).
- Headings: `font-bold tracking-tight`.

| Level | Classes |
|---|---|
| Hero | `text-3xl md:text-4xl lg:text-5xl` |
| H1 | `text-2xl md:text-3xl` |
| H2 | `text-xl md:text-2xl` |
| H3 | `text-lg md:text-xl` |
| Body | `text-sm md:text-base` |
| Small | `text-xs md:text-sm` |

### Spacing

| Token | Classes |
|---|---|
| Section | `py-16 md:py-20 lg:py-24` |
| Container | `px-4 md:px-8` |
| Card | `p-6 md:p-8` |
| Card (mobile-tight) | `p-4 md:p-8` |
| Gap sm | `gap-2 md:gap-3` |
| Gap md | `gap-4 md:gap-6` |
| Gap lg | `gap-6 md:gap-8` |

### Radii

| Component | Class |
|---|---|
| Card | `rounded-2xl` (mandatory) |
| Button | `rounded-full` (mandatory) |
| Input | `rounded-xl` |
| Pill / badge | `rounded-full` |

### Shadow

| Token | Class |
|---|---|
| Card default | `shadow-xl` |
| Card hover | `hover:shadow-2xl` (paired with `hover:scale-105`) |
| Button default | `shadow-lg` |
| Button hover | `hover:shadow-xl` |

### Interaction

| Token | Classes |
|---|---|
| Hover scale | `hover:scale-105` |
| Active scale | `active:scale-95` |
| Focus (button) | `focus:outline-none focus:shadow-xl` |
| Transition (cards) | `transition-all duration-300` |
| Transition (stack) | `all 400ms cubic-bezier(0.16, 1, 0.3, 1)` (custom, see Stack CSS below) |

---

## Stack — the core technique

The stack is what defines the style. Two variants: **3-card (default)** and **5-card (showcase)**. Pick by visual weight, not by content.

**Critical principle**: all cards share `position: absolute; top: 0; left: 0; right: 0;` and offset via `transform`. Do not center each card individually — that produces "floating cards" instead of "tilted stack".

### Stack CSS (paste into every page that uses a stack)

```css
@media (prefers-reduced-motion: reduce) {
  .sk-card { transition: none !important; }
}
.sk-deck { position: relative; }
.sk-card {
  position: absolute;
  top: 0; left: 0; right: 0;
  transition: all 400ms cubic-bezier(0.16, 1, 0.3, 1);
}

/* 3-card hover shuffle */
.sk-deck.three:hover .sk-card:nth-child(2) {
  transform: translate(-30px, 60px) scale(0.86) rotate(5deg) !important;
}
.sk-deck.three:hover .sk-card:nth-child(3) {
  transform: translate(60px, 30px) scale(0.92) rotate(8deg) !important;
}
.sk-deck.three:hover .sk-card:nth-child(4) {
  transform: translate(0, -32px) scale(1.05) rotate(0) !important;
  box-shadow: 0 30px 60px rgba(0,0,0,0.20);
}

/* 5-card hover shuffle */
.sk-deck.five:hover .sk-card:nth-child(2) { transform: translate(-80px, 120px) scale(0.78) rotate(8deg) !important; opacity: 0.5; }
.sk-deck.five:hover .sk-card:nth-child(3) { transform: translate(-30px, 100px) scale(0.84) rotate(6deg) !important; opacity: 0.6; }
.sk-deck.five:hover .sk-card:nth-child(4) { transform: translate(40px, 80px)  scale(0.90) rotate(4deg) !important; }
.sk-deck.five:hover .sk-card:nth-child(5) { transform: translate(100px, 40px) scale(0.94) rotate(2deg) !important; }
.sk-deck.five:hover .sk-card:nth-child(6) { transform: translate(0, -36px)   scale(1.05) rotate(0)   !important;
  box-shadow: 0 30px 60px rgba(0,0,0,0.20);
}
```

### 3-card stack (default — for most pages)

```html
<div class="sk-deck three group h-80">

  <!-- Card 3: back, z-10 -->
  <div class="sk-card rounded-2xl shadow-xl bg-white p-6 md:p-8"
       style="z-index: 10; transform: translate(16px, 32px) scale(0.9) rotate(-3deg); transform-origin: top left; opacity: 0.6;">
    <div class="h-1 w-10 rounded-full bg-[#fd79a8] mb-4"></div>
    <p class="text-xs uppercase tracking-wider font-bold text-zinc-400 mb-2">{CARD_3_LABEL}</p>
    <p class="text-sm text-zinc-600">{CARD_3_COPY}</p>
  </div>

  <!-- Card 2: mid, z-20 -->
  <div class="sk-card rounded-2xl shadow-xl bg-white p-6 md:p-8"
       style="z-index: 20; transform: translate(8px, 16px) scale(0.95) rotate(2deg); transform-origin: top left; opacity: 0.8;">
    <div class="h-1 w-10 rounded-full bg-[#00cec9] mb-4"></div>
    <p class="text-xs uppercase tracking-wider font-bold text-zinc-400 mb-2">{CARD_2_LABEL}</p>
    <p class="text-sm text-zinc-600">{CARD_2_COPY}</p>
  </div>

  <!-- Card 1: front, z-30 -->
  <div class="sk-card rounded-2xl shadow-xl bg-white p-6 md:p-8"
       style="z-index: 30; transform: translate(0, 0) scale(1) rotate(0); transform-origin: top left; opacity: 1;">
    <div class="h-1 w-10 rounded-full bg-[#6c5ce7] mb-4"></div>
    <p class="text-xs uppercase tracking-wider font-bold text-[#6c5ce7] mb-2">{CARD_1_LABEL}</p>
    <p class="text-lg md:text-xl font-bold tracking-tight text-zinc-900 mb-2">{CARD_1_TITLE}</p>
    <p class="text-sm text-zinc-600 leading-relaxed">{CARD_1_COPY}</p>
  </div>
</div>
```

### 5-card stack (for hero / signature moments)

```html
<div class="sk-deck five group h-[28rem]">

  <!-- Card 5: deepest back -->
  <div class="sk-card rounded-2xl shadow-xl bg-white p-6 md:p-8"
       style="z-index: 5; transform: translate(32px, 64px) scale(0.84) rotate(6deg); transform-origin: top left; opacity: 0.6;">
    <div class="h-1 w-10 rounded-full bg-[#ffeaa7] mb-4"></div>
    <p class="text-xs uppercase tracking-wider font-bold text-zinc-400 mb-2">{CARD_5_LABEL}</p>
  </div>

  <!-- Card 4 -->
  <div class="sk-card rounded-2xl shadow-xl bg-white p-6 md:p-8"
       style="z-index: 10; transform: translate(24px, 48px) scale(0.88) rotate(4.5deg); transform-origin: top left; opacity: 0.7;">
    <div class="h-1 w-10 rounded-full bg-[#fd79a8] mb-4"></div>
    <p class="text-xs uppercase tracking-wider font-bold text-zinc-400 mb-2">{CARD_4_LABEL}</p>
  </div>

  <!-- Card 3 -->
  <div class="sk-card rounded-2xl shadow-xl bg-white p-6 md:p-8"
       style="z-index: 20; transform: translate(16px, 32px) scale(0.92) rotate(3deg); transform-origin: top left; opacity: 0.8;">
    <div class="h-1 w-10 rounded-full bg-[#00cec9] mb-4"></div>
    <p class="text-xs uppercase tracking-wider font-bold text-zinc-400 mb-2">{CARD_3_LABEL}</p>
    <p class="text-sm text-zinc-600">{CARD_3_COPY}</p>
  </div>

  <!-- Card 2 -->
  <div class="sk-card rounded-2xl shadow-xl bg-white p-6 md:p-8"
       style="z-index: 25; transform: translate(8px, 16px) scale(0.96) rotate(1.5deg); transform-origin: top left; opacity: 0.9;">
    <div class="h-1 w-10 rounded-full bg-[#6c5ce7] mb-4"></div>
    <p class="text-xs uppercase tracking-wider font-bold text-zinc-400 mb-2">{CARD_2_LABEL}</p>
    <p class="text-sm text-zinc-600">{CARD_2_COPY}</p>
  </div>

  <!-- Card 1: front -->
  <div class="sk-card rounded-2xl shadow-xl bg-white p-6 md:p-8"
       style="z-index: 30; transform: translate(0, 0) scale(1) rotate(0); transform-origin: top left; opacity: 1;">
    <div class="h-1 w-10 rounded-full bg-[#6c5ce7] mb-4"></div>
    <p class="text-xs uppercase tracking-wider font-bold text-[#6c5ce7] mb-2">{CARD_1_LABEL} · front</p>
    <p class="text-lg md:text-xl font-bold tracking-tight text-zinc-900 mb-2">{CARD_1_TITLE}</p>
    <p class="text-sm text-zinc-600 leading-relaxed">{CARD_1_COPY}</p>
  </div>
</div>
```

Stack container must be tall enough for the deepest card's offset + its own height. For 5-card: `h-[28rem]` (448px) on desktop. For 3-card: `h-80` (320px) is enough.

---

## Component templates

### Hero section (purple bg + right-side 5-card stack)

```html
<section class="bg-[#6c5ce7] text-zinc-900 py-16 md:py-20 lg:py-24 px-4 md:px-8">
  <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center">
    <div>
      <h1 class="font-bold tracking-tight text-3xl md:text-4xl lg:text-5xl leading-tight max-w-xl">
        {HERO_HEADLINE}
      </h1>
      <p class="font-sans text-sm md:text-base text-zinc-900/80 max-w-md mt-5 leading-relaxed">
        {HERO_SUBHEADLINE}
      </p>
      <div class="mt-8 flex flex-wrap gap-3">
        <button class="rounded-full shadow-lg hover:shadow-xl transition-shadow bg-zinc-900 text-white text-sm font-semibold px-6 py-3 active:scale-95">
          {PRIMARY_CTA}
        </button>
        <button class="rounded-full shadow-lg hover:shadow-xl transition-shadow bg-white/10 text-zinc-900 text-sm font-semibold px-6 py-3 active:scale-95">
          {SECONDARY_CTA}
        </button>
      </div>
    </div>
    <!-- 5-card stack goes here, see Stack section above -->
  </div>
</section>
```

### Card grid (3 white cards on dark slate-gradient bg)

```html
<section class="bg-gradient-to-br from-slate-900 to-slate-800 text-zinc-900 py-16 md:py-20 lg:py-24 px-4 md:px-8">
  <div class="max-w-6xl mx-auto">
    <h2 class="font-bold tracking-tight text-2xl md:text-3xl text-white">{SECTION_TITLE}</h2>
    <p class="font-sans text-sm md:text-base text-zinc-400 max-w-xl mt-3">{SECTION_SUBTITLE}</p>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 mt-10">
      <div class="rounded-2xl shadow-xl transition-all duration-300 bg-white p-6 md:p-8 hover:shadow-2xl">
        <div class="h-1 w-10 rounded-full bg-[#6c5ce7] mb-5"></div>
        <h3 class="font-bold tracking-tight text-lg md:text-xl text-zinc-900">{CARD_1_TITLE}</h3>
        <p class="font-sans text-sm md:text-base text-zinc-600 mt-3 leading-relaxed">{CARD_1_COPY}</p>
      </div>
      <div class="rounded-2xl shadow-xl transition-all duration-300 bg-white p-6 md:p-8 hover:shadow-2xl">
        <div class="h-1 w-10 rounded-full bg-[#00cec9] mb-5"></div>
        <h3 class="font-bold tracking-tight text-lg md:text-xl text-zinc-900">{CARD_2_TITLE}</h3>
        <p class="font-sans text-sm md:text-base text-zinc-600 mt-3 leading-relaxed">{CARD_2_COPY}</p>
      </div>
      <div class="rounded-2xl shadow-xl transition-all duration-300 bg-white p-6 md:p-8 hover:shadow-2xl">
        <div class="h-1 w-10 rounded-full bg-[#fd79a8] mb-5"></div>
        <h3 class="font-bold tracking-tight text-lg md:text-xl text-zinc-900">{CARD_3_TITLE}</h3>
        <p class="font-sans text-sm md:text-base text-zinc-600 mt-3 leading-relaxed">{CARD_3_COPY}</p>
      </div>
    </div>
  </div>
</section>
```

### Pricing 3-card deck

```html
<section class="bg-white py-16 md:py-20 lg:py-24 px-4 md:px-8">
  <div class="max-w-6xl mx-auto text-center">
    <h2 class="font-bold tracking-tight text-2xl md:text-3xl text-zinc-900">{PRICING_TITLE}</h2>
    <p class="font-sans text-sm md:text-base text-zinc-600 max-w-xl mx-auto mt-3">{PRICING_SUBTITLE}</p>
    <div class="sk-deck three group h-[640px] mt-12">
      <!-- paste the 3-card stack above, with these labels/prices:
           - Card 3 (back): "Enterprise", $99/mo
           - Card 2 (mid): "Starter", $9/mo
           - Card 1 (front): "Pro" with "Popular" badge, $29/mo
      -->
    </div>
  </div>
</section>
```

### Onboarding 4-step (mobile-first, 420px)

```html
<main class="max-w-md mx-auto bg-white min-h-screen flex flex-col">
  <header class="px-4 md:px-8 pt-10 pb-4 flex items-center justify-between">
    <button class="text-sm text-zinc-400 hover:text-zinc-900 transition-colors focus:outline-none focus:shadow-xl rounded-full">Skip</button>
    <p class="text-sm text-zinc-600 font-mono">{CURRENT_STEP} / {TOTAL_STEPS}</p>
    <button class="text-sm text-zinc-400 hover:text-zinc-900 transition-colors focus:outline-none focus:shadow-xl rounded-full">Help</button>
  </header>
  <div class="px-4 md:px-8 mb-8">
    <div class="flex items-center gap-1.5" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
      <!-- 4 segments: fill bg-[#6c5ce7] for completed, bg-zinc-200 for remaining -->
    </div>
  </div>
  <section class="px-4 md:px-8 mb-6">
    <h1 class="font-bold tracking-tight text-2xl md:text-3xl text-zinc-900">{STEP_TITLE}</h1>
    <p class="font-sans text-sm md:text-base text-zinc-600 mt-2 max-w-xs leading-relaxed">{STEP_SUBTITLE}</p>
  </section>
  <section class="flex-1 px-4 md:px-8">
    <!-- 4-card stack: 3 + 1 extra back card with scale-88.
         Each card offsets +8px X / +16px Y / +1.5deg rotate / -4% scale / -10% opacity.
         Front card uses p-4 (not p-6) so copy doesn't overflow at 360-420px. -->
  </section>
  <footer class="px-4 md:px-8 pt-6 pb-10 flex items-center gap-3">
    <button class="flex-1 rounded-full shadow-lg hover:shadow-xl transition-shadow bg-white text-zinc-900 text-sm font-semibold px-6 py-3 border border-zinc-200 active:scale-95 focus:outline-none focus:shadow-xl">Back</button>
    <button class="flex-[1.4] rounded-full shadow-lg hover:shadow-xl transition-shadow bg-zinc-900 text-white text-sm font-semibold px-6 py-3 active:scale-95 focus:outline-none focus:shadow-xl">Continue</button>
  </footer>
</main>
```

### Form input (search or text)

```html
<div class="relative">
  <input
    type="text"
    placeholder="Search cards..."
    class="w-full bg-white/80 backdrop-blur border border-zinc-200 rounded-xl px-5 py-3 text-zinc-900 placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-purple-500/30 transition-all"
  />
  <svg class="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-zinc-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
</div>
```

### Footer (white, 3 columns)

```html
<footer class="bg-white text-zinc-600 py-16 md:py-20 lg:py-24 px-4 md:px-8 border-t border-zinc-200">
  <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
    <div>
      <span class="font-bold tracking-tight text-lg md:text-xl text-zinc-900">{LOGO_TEXT}</span>
      <p class="font-sans text-xs md:text-sm mt-2 text-zinc-600">{TAGLINE}</p>
    </div>
    <div>
      <h4 class="font-bold tracking-tight text-lg md:text-xl text-zinc-900">{COLUMN_1_TITLE}</h4>
      <ul class="font-sans text-xs md:text-sm mt-3 space-y-2 text-zinc-600">
        <li><a href="#" class="hover:text-zinc-900 transition-colors">{LINK_1}</a></li>
      </ul>
    </div>
    <div>
      <h4 class="font-bold tracking-tight text-lg md:text-xl text-zinc-900">{COLUMN_2_TITLE}</h4>
      <ul class="font-sans text-xs md:text-sm mt-3 space-y-2 text-zinc-600">
        <li><a href="#" class="hover:text-zinc-900 transition-colors">{LINK_1}</a></li>
      </ul>
    </div>
  </div>
</footer>
```

---

## Do (required)

### Every button must include

```
rounded-full shadow-lg hover:shadow-xl transition-shadow
+ bg-zinc-900 text-white | bg-white text-zinc-900 border border-zinc-200 | bg-[#6c5ce7] text-white
+ active:scale-95
+ focus:outline-none focus:shadow-xl
+ min-height py-3 (44px touch target)
```

### Every card must include

```
rounded-2xl shadow-xl bg-white
+ p-6 md:p-8 (or p-4 md:p-8 for mobile-tight)
+ transition-all duration-300
+ hover:shadow-2xl (if interactive)
+ 5px top color bar (h-1 w-10 rounded-full + accent hex)
```

### Every input must include

```
bg-white/80 backdrop-blur border border-zinc-200 rounded-xl
+ px-5 py-3
+ placeholder-zinc-400
+ focus:outline-none focus:ring-2 focus:ring-purple-500/30
+ transition-all
```

### Every stack must include

1. The CSS block from "Stack CSS" above
2. `prefers-reduced-motion` fallback
3. `class="sk-deck {variant} group"` on the container
4. Each card positioned `absolute top:0 left:0 right:0` with transform offsets
5. Front card lifts on group-hover (translate-Y up + scale up + shadow up)
6. Back cards fan out on group-hover with different rotate + translate-x per layer

### Every interactive element must have

- Visible focus state (`focus:outline-none focus:shadow-xl`)
- Hover state (color, scale, or shadow)
- Active state for buttons (`active:scale-95`)

### Every section must have

- `py-16 md:py-20 lg:py-24` (vertical rhythm)
- `px-4 md:px-8` (horizontal gutter)
- Heading in the type scale (Hero / H1 / H2 / H3)

---

## Don't (banned)

### Banned classes

- `rounded-none` — use `rounded-2xl`
- `shadow-none` — use `shadow-xl`
- `border-4`, `border-8` — use `border` or no border

### Banned style drift

- ❌ Purple-to-blue linear or radial gradients
- ❌ `Inter`, `Roboto`, `Geist`, `Fraunces`, `Plus Jakarta Sans` as body or heading
- ❌ Cards inside cards (nested card elements)
- ❌ Gray text on colored backgrounds (use `zinc-900` or `white`)
- ❌ Bounce or elastic easing curves (use `cubic-bezier(0.16, 1, 0.3, 1)` only)
- ❌ `bg-clip-text` (gradient text)
- ❌ Backdrop-blur as default surface (the style is opaque)
- ❌ Tiny uppercase tracked eyebrow labels above every section heading
- ❌ `border-left`/`border-right` accent stripes > 1px
- ❌ A 5th accent color (stick to the 4 hex values)

### Banned patterns

- ❌ Stack too many cards (max 5 visible)
- ❌ Completely overlap cards (each card must remain distinguishable)
- ❌ Leave back cards static on hover (kills the depth illusion)
- ❌ Use overly complex animations (transform + opacity only, never width/height/top/left)
- ❌ Use complex gestures on mobile (click and tap only)
- ❌ Animate width/height/top/left (use transform + opacity, GPU path)

---

## Self-check (run before delivery)

```
Token presence
  [ ] Every button: rounded-full shadow-lg hover:shadow-xl transition-shadow
  [ ] Every card: rounded-2xl shadow-xl transition-all duration-300 bg-white
  [ ] Every input: bg-white/80 backdrop-blur border border-zinc-200 rounded-xl focus:ring-2 focus:ring-purple-500/30
  [ ] Every button: active:scale-95 + focus:outline-none focus:shadow-xl
  [ ] Touch targets >= 44px (py-3 minimum)

Forbidden
  [ ] No rounded-none, shadow-none, border-4, border-8
  [ ] No purple-to-blue gradient
  [ ] No Inter/Roboto/Geist/Fraunces/Plus Jakarta Sans font
  [ ] No nested cards
  [ ] No bg-clip-text
  [ ] No tiny uppercase eyebrow labels above section headings

Style
  [ ] Stack uses transform + z-index only
  [ ] Stack back cards scale down + offset
  [ ] Stack has progressive opacity (100/80/60 minimum for 3-card)
  [ ] Stack visible card count 3-5
  [ ] On group-hover, back cards fan out (different rotate + translate-x)
  [ ] On group-hover, front card lifts dramatically
  [ ] Stack uses cubic-bezier(0.16, 1, 0.3, 1) 400ms

Accessibility
  [ ] Every interactive element has visible focus
  [ ] Touch targets >= 44px
  [ ] Animations have prefers-reduced-motion fallback
  [ ] No animation shifts layout
  [ ] Body text contrast >= 4.5:1 (WCAG AA)
  [ ] Body text line length <= 75 characters

Delivery
  [ ] No placeholder text remains (replace {CARD_1_COPY} etc.)
  [ ] No "Lorem ipsum" or "TODO"
  [ ] Layout holds at 360px / 768px / 1280px widths
  [ ] No horizontal overflow at any breakpoint
```

---

## Example prompts (3 from official spec)

### 1. Pricing plans

```
Create pricing cards with stack layout:
1. 3 cards stacked: Starter, Pro, Enterprise
2. Front card fully visible with details
3. Back cards scaled down, offset, and slightly rotated
4. On group-hover: back cards fan out sideways with different rotations
5. Front card lifts with scale-105 and large shadow on hover
6. Each card: plan name, price, features list, CTA
7. Navigation arrows on sides with hover feedback
Dark gradient background, white cards
```

→ Use `templates/pricing-3-card` style. Pro is front (z-30) with "Popular" badge. Starter mid, Enterprise back.

### 2. Product cards (Tinder-style)

```
Create a Tinder-style product card stack:
1. Stack of product cards (5 cards, 3 visible)
2. Swipe right to like, left to pass
3. Each card: product image, name, price, rating
4. On hover: top card peels up (scale-105, shadow-2xl, -translate-y-6), back cards fan out
5. Swipe animation with rotation + opacity fade
6. Undo last action button
7. Fun, interactive, mobile-friendly design
```

→ Use the 5-card stack. Each card has product image + name + price + rating. Like / Pass buttons below the deck.

### 3. Onboarding step guide

```
Create an onboarding flow with card stack:
1. 4 step cards stacked
2. group-hover causes back cards to fan out with rotate + translate-x
3. Front card lifts with scale-105 and shadow-2xl
4. Click Next to advance (card slides out with rotation)
5. Progress indicator dots
6. Each card: step number, title, illustration, description
7. Final card has CTA button
Clean design with duration-[400ms] ease-out transitions
```

→ Use the 4-card mobile pattern from the Onboarding template. Step 1 (front) shows form, steps 2-4 are progressively smaller behind.

---

## How to invoke this skill

When asked to build any Card Stack UI:

1. Read the `Tokens` section. Pick the colors, type, spacing.
2. Read the `Stack` section. Choose 3-card or 5-card.
3. Read the relevant `Component templates` section. Copy the HTML, replace placeholders.
4. Paste the `Stack CSS` once per page (if using a stack).
5. Run the `Self-check` before delivery.
6. If a use case is not covered, follow `Tokens` + `Do/Don't` + `Stack CSS` to build from scratch.

Do not skip steps. The Self-check catches ~80% of style drift.

---

## Source & updates

Source: https://www.stylekit.top/styles/card-stack (StyleKit, open source)
Verified: Aug 2026
If the source spec changes, re-fetch the official page, diff against the `Tokens` section, and update.

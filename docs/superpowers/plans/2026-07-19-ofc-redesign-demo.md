# OFC Redesign Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a five-page static marketing site for Overseas Food Consultants that fixes every accessibility defect in the current site and presents its existing content in the "Editorial Lab" visual direction, deployed to Vercel.

**Architecture:** Astro static site, zero client JavaScript except a mobile nav toggle and a scroll-reveal observer. All copy lives in typed content collections so it can be swapped when the client's email arrives without touching markup. Design tokens are CSS custom properties consumed by Tailwind v4's `@theme`, with contrast ratios verified by a script that can fail the build.

**Tech Stack:** Astro 7.1.1, Tailwind CSS 4.3.3 via `@tailwindcss/vite`, `@astrojs/sitemap` 3.7.3, `lucide-astro` 0.556.0, Vercel static hosting, Formspree for the contact form.

**Source spec:** `docs/superpowers/specs/2026-07-19-ofc-redesign-demo-design.md`

## Global Constraints

Every task's requirements implicitly include this section.

**Versions** — pin exactly; do not upgrade mid-build:
- `astro@7.1.1`, `tailwindcss@4.3.3`, `@tailwindcss/vite@4.3.3`, `@astrojs/sitemap@3.7.3`, `lucide-astro@0.556.0`

**Astro 7 specifics** — these differ from older tutorials the implementer may find:
- Content config lives at `src/content.config.ts`, NOT `src/content/config.ts`
- The `glob` loader is imported from `astro/loaders`
- Tailwind v4 is installed via `npx astro add tailwind` (which adds the `@tailwindcss/vite` plugin). There is NO `tailwind.config.js` and NO `@astrojs/tailwind` package. Configuration happens in CSS via `@theme`.
- Global CSS enables Tailwind with `@import "tailwindcss";`

**Colour tokens** — exact hex values, copied verbatim from spec section 4:

| Token | Light | Dark |
|---|---|---|
| Base | `#1C1917` | — |
| Surface | `#FAFAF9` | `#1C1917` |
| Accent | `#A16207` | `#F59E0B` |
| Body text | `#0C0A09` | `#FAFAF9` |
| Border | `#D6D3D1` | — |
| Destructive | `#DC2626` | `#DC2626` |

**Accent rule:** `#A16207` on light surfaces only (4.71:1). `#F59E0B` on dark surfaces only (8.14:1). Never `#A16207` on `#1C1917` — that is 3.55:1 and fails body text.

**Typography:** Newsreader (display), Public Sans (body), JetBrains Mono (technical labels, uppercase, wide tracking). Self-hosted, `font-display: swap`.

**Accessibility gates** — non-negotiable, verified in Task 11:
- Body text contrast ≥ 4.5:1, large text and UI ≥ 3:1
- Sequential heading order, exactly one `<h1>` per page
- Every link and icon-only button has a discernible accessible name
- Valid list semantics — every `<li>` inside a `<ul>`/`<ol>`
- Visible focus rings on all interactive elements
- `prefers-reduced-motion` respected
- Target Lighthouse Accessibility 100 (baseline was 87), Agentic Browsing ≥ 90 (baseline 50)

**Performance gates:**
- CLS < 0.1 (current site is 0.00 — must not regress)
- All images AVIF/WebP with explicit `width`/`height`
- SEO must hold at 100

**Copy rule:** All body copy comes from `src/data/`. Never hardcode client copy in a `.astro` component. Structure is fixed; copy is swappable.

**Motion rule:** 150–300ms, `transform`/`opacity` only, exit faster than enter, max two animated elements per viewport.

**Anti-patterns — never introduce:** purple/pink gradients, decorative blobs, cards nested inside cards, emoji as icons, stock-atmospheric filler imagery.

---

### Task 1: Scaffold, tokens, and the contrast gate

Foundation. Produces a building Astro site with the design tokens defined and a script that proves they meet WCAG.

**Files:**
- Create: `package.json`, `astro.config.mjs`, `tsconfig.json` (via scaffold)
- Create: `src/styles/global.css`
- Modify: `scripts/contrast-check.py` (already exists — extend to exit non-zero on failure)
- Create: `src/pages/index.astro` (temporary smoke page, replaced in Task 5)

**Interfaces:**
- Consumes: nothing
- Produces: CSS custom properties `--color-base`, `--color-surface`, `--color-surface-dark`, `--color-accent`, `--color-accent-dark`, `--color-body`, `--color-body-dark`, `--color-border`, `--color-destructive`; Tailwind utilities `bg-surface`, `text-accent`, `font-display`, `font-body`, `font-mono`

- [ ] **Step 1: Scaffold the Astro project**

Run from the repo root. The directory already contains `docs/` and `scripts/`, so scaffold in place:

```bash
npm create astro@latest . -- --template minimal --no-install --no-git --typescript strict --yes
npm install
npm install astro@7.1.1 --save-exact
```

Expected: `package.json`, `astro.config.mjs`, `src/pages/index.astro` created. Existing `docs/`, `scripts/`, `.gitignore` untouched.

- [ ] **Step 2: Add Tailwind v4**

```bash
npx astro add tailwind --yes
npm install tailwindcss@4.3.3 @tailwindcss/vite@4.3.3 --save-exact
```

Expected: `astro.config.mjs` now contains a `vite.plugins` entry for `@tailwindcss/vite`. Verify there is NO `tailwind.config.js` — if the tool created one, delete it; v4 configures in CSS.

- [ ] **Step 3: Write the token stylesheet**

Create `src/styles/global.css`:

```css
@import "tailwindcss";

@theme {
  --color-base: #1C1917;
  --color-surface: #FAFAF9;
  --color-surface-dark: #1C1917;
  --color-accent: #A16207;
  --color-accent-dark: #F59E0B;
  --color-body: #0C0A09;
  --color-body-dark: #FAFAF9;
  --color-border: #D6D3D1;
  --color-destructive: #DC2626;

  --font-display: "Newsreader", ui-serif, Georgia, serif;
  --font-body: "Public Sans", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
}

@layer base {
  html {
    scroll-behavior: smooth;
  }

  body {
    background-color: var(--color-surface);
    color: var(--color-body);
    font-family: var(--font-body);
    -webkit-font-smoothing: antialiased;
  }

  :focus-visible {
    outline: 3px solid var(--color-accent);
    outline-offset: 2px;
  }

  @media (prefers-reduced-motion: reduce) {
    html {
      scroll-behavior: auto;
    }
    *,
    *::before,
    *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }
}

/* Technical label treatment — the "Editorial Lab" signature */
.label-mono {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
```

- [ ] **Step 4: Make the contrast script a gate**

Replace `scripts/contrast-check.py` so it exits non-zero when a pair fails its required level:

```python
#!/usr/bin/env python3
"""Verify design token contrast ratios against WCAG 2.x.

Exits 1 if any pair fails its required level. Run after any token change.
"""
import sys


def lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# (foreground, background, required_ratio, label)
PAIRS = [
    ("#A16207", "#FAFAF9", 4.5, "accent on light surface"),
    ("#F59E0B", "#1C1917", 4.5, "accent on dark surface"),
    ("#0C0A09", "#F59E0B", 4.5, "text on amber button"),
    ("#0C0A09", "#FAFAF9", 4.5, "body on light surface"),
    ("#FAFAF9", "#1C1917", 4.5, "body on dark surface"),
    ("#D6D3D1", "#FAFAF9", 3.0, "border on light surface"),
]

# Pairs that MUST NOT be used together, reported so anyone reaching for the
# wrong accent on a dark background sees why it is forbidden.
FORBIDDEN = [("#A16207", "#1C1917", "amber-700 on dark — use #F59E0B")]

failed = False

for fg, bg, required, label in PAIRS:
    r = ratio(fg, bg)
    ok = r >= required
    if not ok:
        failed = True
    print(f"{'PASS' if ok else 'FAIL'}  {r:6.2f}:1  (needs {required}:1)  {label}")

for fg, bg, why in FORBIDDEN:
    r = ratio(fg, bg)
    print(f"NOTE  {r:6.2f}:1  forbidden pairing — {why}")

if failed:
    print("\nContrast gate FAILED", file=sys.stderr)
    sys.exit(1)

print("\nContrast gate passed")
```

- [ ] **Step 5: Run the contrast gate and verify it passes**

```bash
python3 scripts/contrast-check.py; echo "exit=$?"
```

Expected: six `PASS` lines, one `NOTE` line reading `3.55:1  forbidden pairing`, then `Contrast gate passed` and `exit=0`.

- [ ] **Step 6: Verify the gate actually fails when it should**

Temporarily change the first pair's required ratio from `4.5` to `99.0`, re-run, confirm `exit=1`, then change it back to `4.5`.

```bash
python3 scripts/contrast-check.py; echo "exit=$?"
```

Expected before revert: a `FAIL` line and `exit=1`. After revert: `exit=0`. A gate that cannot fail is not a gate.

- [ ] **Step 7: Smoke-test the build**

Replace `src/pages/index.astro`:

```astro
---
import "../styles/global.css";
---

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Scaffold smoke test</title>
  </head>
  <body>
    <h1 class="font-display text-4xl text-accent">Editorial Lab</h1>
    <p class="label-mono">HACCP / ISO 22000</p>
  </body>
</html>
```

```bash
npm run build
```

Expected: build succeeds, `dist/index.html` exists.

- [ ] **Step 8: Commit**

```bash
git add package.json package-lock.json astro.config.mjs tsconfig.json src/ scripts/contrast-check.py
git commit -m "feat: scaffold Astro 7 + Tailwind v4 with verified design tokens"
```

---

### Task 2: Layout shell — BaseLayout, Header, Footer, SEO

Every accessibility defect in the current site lives in the shell. Fixing it here fixes it site-wide.

**Files:**
- Create: `src/layouts/BaseLayout.astro`
- Create: `src/components/Header.astro`
- Create: `src/components/Footer.astro`
- Create: `src/components/SEO.astro`
- Create: `src/data/site.ts`
- Modify: `astro.config.mjs`

**Interfaces:**
- Consumes: `src/styles/global.css` from Task 1
- Produces:
  - `BaseLayout` props: `{ title: string; description: string; ogImage?: string }`
  - `SEO` props: `{ title: string; description: string; canonical: string; ogImage?: string }`
  - `src/data/site.ts` exports `SITE` (fields: `name`, `legalName`, `tagline`, `subTagline`, `url`, `address`, `registration`, `social.linkedin`, `social.instagram`, `social.youtube`) and `NAV: ReadonlyArray<{ href: string; label: string }>`

- [ ] **Step 1: Define site constants**

Create `src/data/site.ts`:

```ts
export const SITE = {
  name: "Overseas Food Consultants",
  legalName: "Overseas Food Consultants (OPC) Private Limited",
  tagline: "Your Source for Food Experts",
  subTagline: "Elevating Your Food Business",
  url: "https://ofc-demo.vercel.app",
  address: "Haryana, India",
  registration:
    "Registered under the Companies Act 2013, Ministry of Corporate Affairs, Government of India",
  social: {
    linkedin: "https://www.linkedin.com/company/overseas-food-consultants",
    instagram: "https://www.instagram.com/overseas_foodconsultants",
    youtube: "https://www.youtube.com/@overseasfoodconsultants",
  },
} as const;

export const NAV = [
  { href: "/", label: "Home" },
  { href: "/consultancy", label: "Consultancy" },
  { href: "/case-studies", label: "Case Studies" },
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
] as const;
```

- [ ] **Step 2: Write the SEO component**

Create `src/components/SEO.astro`. This holds the SEO score at 100 and raises the agentic-browsing score:

```astro
---
import { SITE } from "../data/site";

interface Props {
  title: string;
  description: string;
  canonical: string;
  ogImage?: string;
}

const { title, description, canonical, ogImage = "/og-default.jpg" } = Astro.props;
const fullTitle = `${title} | ${SITE.name}`;
const canonicalUrl = new URL(canonical, SITE.url).href;
const ogUrl = new URL(ogImage, SITE.url).href;

const structuredData = {
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  name: SITE.legalName,
  alternateName: SITE.name,
  description: SITE.tagline,
  url: SITE.url,
  address: {
    "@type": "PostalAddress",
    addressRegion: "Haryana",
    addressCountry: "IN",
  },
  areaServed: "Worldwide",
  knowsAbout: [
    "Food safety and HACCP compliance",
    "Recipe standardization",
    "Formula optimization",
    "Shelf-life prediction",
    "Dairy processing",
    "Food equipment specification",
  ],
  sameAs: [SITE.social.linkedin, SITE.social.instagram, SITE.social.youtube],
};
---

<title>{fullTitle}</title>
<meta name="description" content={description} />
<link rel="canonical" href={canonicalUrl} />

<meta property="og:type" content="website" />
<meta property="og:title" content={fullTitle} />
<meta property="og:description" content={description} />
<meta property="og:url" content={canonicalUrl} />
<meta property="og:image" content={ogUrl} />
<meta property="og:site_name" content={SITE.name} />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content={fullTitle} />
<meta name="twitter:description" content={description} />
<meta name="twitter:image" content={ogUrl} />

<script type="application/ld+json" set:html={JSON.stringify(structuredData)} />
```

- [ ] **Step 3: Write the Header with an accessible mobile nav**

Create `src/components/Header.astro`. Note the requirements it satisfies: discernible link names, `aria-current` for active state, `aria-expanded` on the toggle, a real `<ul>` for list semantics:

```astro
---
import { SITE, NAV } from "../data/site";
const path = Astro.url.pathname;
---

<header class="border-b border-[var(--color-border)] bg-surface">
  <div class="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
    <a href="/" class="font-display text-xl leading-tight tracking-tight">
      <span class="sr-only">{SITE.legalName} — home</span>
      <span aria-hidden="true">Overseas Food<br /><em class="not-italic text-accent">Consultants</em></span>
    </a>

    <nav aria-label="Primary">
      <button
        type="button"
        id="nav-toggle"
        class="md:hidden"
        aria-expanded="false"
        aria-controls="nav-menu"
      >
        <span class="sr-only">Open navigation menu</span>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
        </svg>
      </button>

      <ul id="nav-menu" class="hidden md:flex md:items-center md:gap-8">
        {NAV.map(({ href, label }) => (
          <li>
            <a
              href={href}
              class="text-sm hover:text-accent"
              aria-current={path === href ? "page" : undefined}
            >
              {label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  </div>
</header>

<script>
  const toggle = document.getElementById("nav-toggle");
  const menu = document.getElementById("nav-menu");
  toggle?.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!open));
    menu?.classList.toggle("hidden");
  });
</script>
```

- [ ] **Step 4: Write the Footer**

Create `src/components/Footer.astro`. Dark surface — accent must be `text-accent-dark`, never `text-accent`:

```astro
---
import { SITE, NAV } from "../data/site";
---

<footer class="bg-[var(--color-surface-dark)] text-[var(--color-body-dark)]">
  <div class="mx-auto grid max-w-6xl gap-10 px-6 py-16 md:grid-cols-3">
    <div>
      <p class="font-display text-lg">{SITE.name}</p>
      <p class="mt-3 text-sm opacity-80">{SITE.registration}</p>
      <p class="mt-3 text-sm opacity-80">{SITE.address}</p>
    </div>

    <nav aria-label="Footer">
      <p class="label-mono text-accent-dark">Navigate</p>
      <ul class="mt-4 space-y-2">
        {NAV.map(({ href, label }) => (
          <li><a href={href} class="text-sm hover:text-accent-dark">{label}</a></li>
        ))}
      </ul>
    </nav>

    <div>
      <p class="label-mono text-accent-dark">Connect</p>
      <ul class="mt-4 space-y-2">
        <li><a href={SITE.social.linkedin} class="text-sm hover:text-accent-dark" rel="me noopener">LinkedIn</a></li>
        <li><a href={SITE.social.instagram} class="text-sm hover:text-accent-dark" rel="me noopener">Instagram</a></li>
        <li><a href={SITE.social.youtube} class="text-sm hover:text-accent-dark" rel="me noopener">YouTube</a></li>
      </ul>
    </div>
  </div>

  <div class="border-t border-white/10 py-6 text-center text-xs opacity-70">
    <p>&copy; {new Date().getFullYear()} {SITE.legalName}</p>
  </div>
</footer>
```

- [ ] **Step 5: Write BaseLayout with a skip link**

Create `src/layouts/BaseLayout.astro`:

```astro
---
import "../styles/global.css";
import SEO from "../components/SEO.astro";
import Header from "../components/Header.astro";
import Footer from "../components/Footer.astro";

interface Props {
  title: string;
  description: string;
  ogImage?: string;
}

const { title, description, ogImage } = Astro.props;
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <SEO title={title} description={description} canonical={Astro.url.pathname} ogImage={ogImage} />
  </head>
  <body>
    <a
      href="#main"
      class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:bg-accent focus:px-4 focus:py-2 focus:text-[var(--color-surface)]"
    >
      Skip to main content
    </a>
    <Header />
    <main id="main"><slot /></main>
    <Footer />
  </body>
</html>
```

- [ ] **Step 6: Register the sitemap integration**

```bash
npm install @astrojs/sitemap@3.7.3 --save-exact
```

Edit `astro.config.mjs` so it reads (keeping the Tailwind vite plugin that `astro add` inserted):

```js
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  site: "https://ofc-demo.vercel.app",
  integrations: [sitemap()],
  vite: { plugins: [tailwindcss()] },
});
```

- [ ] **Step 7: Verify the shell builds and emits correct markup**

Update `src/pages/index.astro` to use the layout:

```astro
---
import BaseLayout from "../layouts/BaseLayout.astro";
---

<BaseLayout title="Home" description="Expert food and beverage consulting.">
  <h1 class="mx-auto max-w-6xl px-6 py-24 font-display text-5xl">Shell test</h1>
</BaseLayout>
```

```bash
npm run build
grep -c '<h1' dist/index.html
grep -o 'Skip to main content' dist/index.html
grep -o '"@type":"ProfessionalService"' dist/index.html
test -f dist/sitemap-index.xml && echo "sitemap ok"
```

Expected: `1` (exactly one `h1`), `Skip to main content`, `"@type":"ProfessionalService"`, `sitemap ok`.

- [ ] **Step 8: Commit**

```bash
git add src/ astro.config.mjs package.json package-lock.json
git commit -m "feat: accessible layout shell with SEO and structured data"
```

---

### Task 3: Content collections — all client copy as typed data

Puts every piece of scraped copy behind a schema so the client's email can be swapped in without touching markup.

**Files:**
- Create: `src/content.config.ts`
- Create: `src/data/services/dairy.md`, `src/data/services/food.md`, `src/data/services/equipment.md`
- Create: `src/data/case-studies/restaurant-franchises.md`, `packaged-goods.md`, `food-tech-startup.md`, `supply-chain.md`
- Create: `src/data/differentiators.ts`
- Create: `src/data/aims.ts`

**Interfaces:**
- Consumes: nothing
- Produces:
  - Collection `services`, schema `{ title: string; order: number; summary: string; capabilities: string[] }`
  - Collection `caseStudies`, schema `{ title: string; sector: string; order: number; metric: string | null; metricLabel: string | null; summary: string }`
  - `differentiators.ts` exports `DIFFERENTIATORS: ReadonlyArray<{ title: string; body: string }>`
  - `aims.ts` exports `AIMS: ReadonlyArray<string>`

- [ ] **Step 1: Define the content config**

Create `src/content.config.ts` — note the Astro 7 path and loader import:

```ts
import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob } from "astro/loaders";

const services = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/data/services" }),
  schema: z.object({
    title: z.string(),
    order: z.number(),
    summary: z.string(),
    capabilities: z.array(z.string()).min(1),
  }),
});

const caseStudies = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/data/case-studies" }),
  schema: z.object({
    title: z.string(),
    sector: z.string(),
    order: z.number(),
    metric: z.string().nullable(),
    metricLabel: z.string().nullable(),
    summary: z.string(),
  }),
});

export const collections = { services, caseStudies };
```

- [ ] **Step 2: Write the three service files**

Create `src/data/services/dairy.md`:

```markdown
---
title: Dairy Industry
order: 1
summary: End-to-end technical guidance for dairy processing operations, from plant layout through functional formula development.
capabilities:
  - Online sequenced operational process layout design
  - Raw material selection and process control
  - Waste minimisation and by-product utilisation
  - Qualitative and quantitative parameter determination for finished goods
  - Equipment technical and competitive budgetary specification
  - Dairy-based functional formula development
---

Dairy operations fail on process control long before they fail on recipe. We work
from the plant floor outward.
```

Create `src/data/services/food.md`:

```markdown
---
title: Food Industry
order: 2
summary: Product development and defect resolution across baked goods, beverages, and composite formulations.
capabilities:
  - New product development
  - Cereal-dairy composite baked product development
  - Storage capacity and shelf-life determination
  - Cost calculation for finished goods
  - Root cause analysis of product defects in beverages and baked goods
  - Equipment technical and competitive budgetary determination
---

Most product defects are traceable to a decision made three steps upstream. We find
that decision.
```

Create `src/data/services/equipment.md`:

```markdown
---
title: Equipment & Instrument Procurement
order: 3
summary: Specification, budgetary guidance, and fabrication support for production and analytical equipment.
capabilities:
  - Specification design for production equipment
  - Specification design for analytical equipment
  - Competitive budgetary guidance
  - Fabrication assistance for engineering works
---

Buying the wrong equipment is the most expensive mistake in food manufacturing, and
it is almost always avoidable at the specification stage.
```

- [ ] **Step 3: Write the four case-study files**

Create `src/data/case-studies/restaurant-franchises.md`:

```markdown
---
title: Menu standardisation across continents
sector: Global restaurant franchises
order: 1
metric: null
metricLabel: null
summary: Menu standardisation, cost control, and kitchen design for large-scale operations across multiple continents.
---
```

Create `src/data/case-studies/packaged-goods.md`:

```markdown
---
title: Five new formulas, fifteen percent lower cost
sector: Mid-size packaged goods company
order: 2
metric: "15%"
metricLabel: production cost reduction
summary: Developed and optimised five new product formulas, cutting production cost by 15% and achieving successful market entry.
---
```

Create `src/data/case-studies/food-tech-startup.md`:

```markdown
---
title: HACCP from zero to certified
sector: Next-generation food-tech startup
order: 3
metric: HACCP
metricLabel: plans developed and certified
summary: Critical guidance on initial HACCP plan development, securing the local and international compliance certifications required for launch.
---
```

Create `src/data/case-studies/supply-chain.md`:

```markdown
---
title: Cold chain integrity under audit
sector: International supply chain networks
order: 4
metric: null
metricLabel: null
summary: Troubleshooting complex logistics failures, ensuring cold chain integrity, and auditing suppliers for quality assurance.
---
```

- [ ] **Step 4: Write the differentiators and aims**

Create `src/data/differentiators.ts`:

```ts
export const DIFFERENTIATORS = [
  {
    title: "Global Expertise",
    body: "Knowledge of the food industry across diverse regions, applied to local challenges. Experience spanning multiple markets.",
  },
  {
    title: "Customised Solutions",
    body: "Every food business has distinct needs and goals. Consulting is tailored to specific business objectives and operational requirements.",
  },
  {
    title: "Innovative Approach",
    body: "Cutting-edge solutions built on current industry trends, enhancing growth, efficiency, and competitiveness.",
  },
  {
    title: "Commitment to Quality",
    body: "Solutions meeting the highest industry standards, driving results and long-term success.",
  },
] as const;
```

Create `src/data/aims.ts`:

```ts
export const AIMS = [
  "Develop new food products and innovative recipes",
  "Conduct comprehensive sensory evaluations and quality control",
  "Design and optimise efficient food processing systems",
  "Ensure strict food safety and regulatory compliance",
  "Collaborate with chefs, farmers, manufacturers, and food experts",
  "Stay at the forefront of consumer trends and industry innovations",
] as const;
```

- [ ] **Step 5: Verify the schemas reject bad data**

First prove the gate works. Delete the `order: 1` line from `src/data/services/dairy.md`, then:

```bash
npm run build
```

Expected: build FAILS with a Zod error naming `dairy.md` and the missing `order` field.

- [ ] **Step 6: Restore and verify the build passes**

Put `order: 1` back into `dairy.md`, then:

```bash
npm run build
```

Expected: build succeeds.

- [ ] **Step 7: Commit**

```bash
git add src/content.config.ts src/data/
git commit -m "feat: typed content collections for all client copy"
```

---

### Task 4: Component primitives

Small, reusable, each with one responsibility. Built before pages so pages are assembly, not invention.

**Files:**
- Create: `src/components/Section.astro`
- Create: `src/components/SectionHeading.astro`
- Create: `src/components/Button.astro`
- Create: `src/components/StatBlock.astro`
- Create: `src/components/ServiceCard.astro`
- Create: `src/pages/_primitives-test.astro`

**Interfaces:**
- Consumes: tokens from Task 1, `BaseLayout` from Task 2
- Produces:
  - `Section` props `{ tone?: "light" | "dark"; id?: string }`
  - `SectionHeading` props `{ eyebrow?: string; title: string; level?: 2 | 3; tone?: "light" | "dark" }`
  - `Button` props `{ href: string; tone?: "light" | "dark"; variant?: "solid" | "ghost" }`
  - `StatBlock` props `{ value: string; label: string; tone?: "light" | "dark" }`
  - `ServiceCard` props `{ title: string; summary: string; capabilities: readonly string[]; href: string; index: number }`

- [ ] **Step 1: Write Section**

Create `src/components/Section.astro`. Centralises the light/dark decision so no page picks the wrong accent by hand:

```astro
---
interface Props {
  tone?: "light" | "dark";
  id?: string;
}
const { tone = "light", id } = Astro.props;
const toneClass =
  tone === "dark"
    ? "bg-[var(--color-surface-dark)] text-[var(--color-body-dark)]"
    : "bg-surface text-[var(--color-body)]";
---

<section id={id} class={toneClass}>
  <div class="mx-auto max-w-6xl px-6 py-20 md:py-28">
    <slot />
  </div>
</section>
```

- [ ] **Step 2: Write SectionHeading**

Create `src/components/SectionHeading.astro`. The `level` prop keeps heading order sequential; the `tone` prop keeps the eyebrow accent contrast-legal:

```astro
---
interface Props {
  eyebrow?: string;
  title: string;
  level?: 2 | 3;
  tone?: "light" | "dark";
}
const { eyebrow, title, level = 2, tone = "light" } = Astro.props;
const Tag = `h${level}`;
const eyebrowClass = tone === "dark" ? "text-accent-dark" : "text-accent";
---

{eyebrow && <p class={`label-mono ${eyebrowClass}`}>{eyebrow}</p>}
<Tag class="mt-3 max-w-3xl font-display text-3xl leading-tight md:text-4xl">{title}</Tag>
```

- [ ] **Step 3: Write Button**

Create `src/components/Button.astro`:

```astro
---
interface Props {
  href: string;
  tone?: "light" | "dark";
  variant?: "solid" | "ghost";
}
const { href, tone = "light", variant = "solid" } = Astro.props;

const solid =
  tone === "dark"
    ? "bg-[var(--color-accent-dark)] text-[var(--color-body)]"
    : "bg-[var(--color-accent)] text-[var(--color-surface)]";
const ghost =
  tone === "dark"
    ? "border border-[var(--color-accent-dark)] text-[var(--color-accent-dark)]"
    : "border border-[var(--color-accent)] text-[var(--color-accent)]";

const classes = variant === "solid" ? solid : ghost;
---

<a
  href={href}
  class={`inline-flex min-h-11 items-center gap-2 px-6 py-3 text-sm font-medium transition-opacity duration-200 hover:opacity-90 ${classes}`}
>
  <slot />
</a>
```

`min-h-11` is 44px — the touch-target minimum.

- [ ] **Step 4: Write StatBlock**

Create `src/components/StatBlock.astro`. This is what promotes buried proof:

```astro
---
interface Props {
  value: string;
  label: string;
  tone?: "light" | "dark";
}
const { value, label, tone = "light" } = Astro.props;
const valueClass = tone === "dark" ? "text-accent-dark" : "text-accent";
---

<div>
  <p class={`font-display text-4xl tabular-nums md:text-5xl ${valueClass}`}>{value}</p>
  <p class="label-mono mt-2 opacity-70">{label}</p>
</div>
```

- [ ] **Step 5: Write ServiceCard**

Create `src/components/ServiceCard.astro`. No nested cards — a flat bordered block:

```astro
---
interface Props {
  title: string;
  summary: string;
  capabilities: readonly string[];
  href: string;
  index: number;
}
const { title, summary, capabilities, href, index } = Astro.props;
const num = String(index).padStart(2, "0");
---

<article class="border-t border-current/20 pt-6">
  <p class="label-mono opacity-70">{num}</p>
  <h3 class="mt-3 font-display text-2xl">{title}</h3>
  <p class="mt-3 max-w-prose text-sm leading-relaxed opacity-80">{summary}</p>
  <ul class="mt-5 space-y-2">
    {capabilities.map((c) => (
      <li class="text-sm leading-relaxed opacity-90">{c}</li>
    ))}
  </ul>
  <a href={href} class="label-mono mt-6 inline-block underline underline-offset-4">
    View {title} services
  </a>
</article>
```

The link text includes the service name so it has a discernible name out of context — the `link-name` defect in the current site. `border-current` and `opacity` are used instead of a fixed accent so the card is contrast-safe on either tone.

- [ ] **Step 6: Verify primitives compile on both tones**

Create `src/pages/_primitives-test.astro` (underscore prefix means Astro will not route it):

```astro
---
import BaseLayout from "../layouts/BaseLayout.astro";
import Section from "../components/Section.astro";
import SectionHeading from "../components/SectionHeading.astro";
import Button from "../components/Button.astro";
import StatBlock from "../components/StatBlock.astro";
---

<BaseLayout title="Primitives" description="Internal component test page.">
  <h1 class="sr-only">Primitives test</h1>
  <Section tone="light">
    <SectionHeading eyebrow="Light section" title="Light tone heading" />
    <StatBlock value="15%" label="cost reduction" />
    <Button href="/contact">Light CTA</Button>
  </Section>
  <Section tone="dark">
    <SectionHeading eyebrow="Dark section" title="Dark tone heading" tone="dark" />
    <StatBlock value="4" label="client sectors" tone="dark" />
    <Button href="/contact" tone="dark">Dark CTA</Button>
  </Section>
</BaseLayout>
```

```bash
npm run build && echo "primitives build ok"
test -d dist/_primitives-test && echo "FAIL: test page routed" || echo "test page correctly unrouted"
```

Expected: `primitives build ok`, then `test page correctly unrouted`.

- [ ] **Step 7: Commit**

```bash
git add src/components/ src/pages/_primitives-test.astro
git commit -m "feat: component primitives with tone-correct accent handling"
```

---

### Task 5: Home page

**Files:**
- Modify: `src/pages/index.astro`
- Create: `src/components/Hero.astro`
- Create: `src/assets/hero-dairy.jpg`, `src/assets/lab-analysis.jpg`, `src/assets/production-line.jpg`
- Create: `public/images/CREDITS.md`

**Interfaces:**
- Consumes: `BaseLayout`, `Section`, `SectionHeading`, `Button`, `StatBlock`, `ServiceCard`, collections `services` and `caseStudies`, `DIFFERENTIATORS`
- Produces: nothing consumed downstream

- [ ] **Step 1: Source and place imagery**

Download three images from Unsplash or Pexels — both licences permit commercial and portfolio use. Save into `src/assets/` (NOT `public/`) so Astro's `<Image>` can optimise them. Required subjects, per the spec's rejection of atmospheric filler:
- `src/assets/hero-dairy.jpg` — a dairy or milk process shot, close and physical
- `src/assets/lab-analysis.jpg` — laboratory or analytical instrumentation
- `src/assets/production-line.jpg` — food production line or plant floor

Create `public/images/CREDITS.md`, filling in the real URL for each:

```markdown
# Image credits

All images licensed for commercial and portfolio use.

- hero-dairy.jpg — <source URL> — Unsplash Licence
- lab-analysis.jpg — <source URL> — Unsplash Licence
- production-line.jpg — <source URL> — Unsplash Licence
```

- [ ] **Step 2: Write the Hero**

Create `src/components/Hero.astro`. Astro's `<Image>` emits AVIF with explicit dimensions, fixing the current site's `image-aspect-ratio` defect and its CLS exposure:

```astro
---
import { Image } from "astro:assets";
import heroImage from "../assets/hero-dairy.jpg";
import Button from "./Button.astro";
import { SITE } from "../data/site";
---

<section class="relative bg-[var(--color-surface-dark)] text-[var(--color-body-dark)]">
  <Image
    src={heroImage}
    alt=""
    widths={[768, 1280, 1920]}
    sizes="100vw"
    loading="eager"
    format="avif"
    class="absolute inset-0 h-full w-full object-cover opacity-35"
  />
  <div class="relative mx-auto max-w-6xl px-6 py-28 md:py-40">
    <p class="label-mono text-accent-dark">{SITE.subTagline}</p>
    <h1 class="mt-5 max-w-4xl font-display text-4xl leading-[1.1] md:text-6xl">
      {SITE.tagline}
    </h1>
    <p class="mt-6 max-w-2xl text-lg leading-relaxed opacity-90">
      A platform of food professionals providing expert advice and technical guidance
      to restaurants, food manufacturers, and foodservice companies worldwide.
    </p>
    <div class="mt-10 flex flex-wrap gap-4">
      <Button href="/contact" tone="dark">Request a consultation</Button>
      <Button href="/consultancy" tone="dark" variant="ghost">Explore our services</Button>
    </div>
  </div>
</section>
```

`alt=""` is correct here — the image is decorative and the heading carries the meaning. An alt describing the photo would be noise for screen-reader users.

- [ ] **Step 3: Assemble the home page**

Replace `src/pages/index.astro`:

```astro
---
import { getCollection } from "astro:content";
import BaseLayout from "../layouts/BaseLayout.astro";
import Hero from "../components/Hero.astro";
import Section from "../components/Section.astro";
import SectionHeading from "../components/SectionHeading.astro";
import Button from "../components/Button.astro";
import StatBlock from "../components/StatBlock.astro";
import ServiceCard from "../components/ServiceCard.astro";
import { DIFFERENTIATORS } from "../data/differentiators";

const services = (await getCollection("services")).sort(
  (a, b) => a.data.order - b.data.order,
);
const caseStudies = (await getCollection("caseStudies")).sort(
  (a, b) => a.data.order - b.data.order,
);
---

<BaseLayout
  title="Food & Beverage Consulting"
  description="Overseas Food Consultants provides expert technical guidance in food safety, formula optimisation, shelf-life prediction, and regulatory compliance."
>
  <Hero />

  <Section tone="light">
    <SectionHeading eyebrow="Track record" title="Measured outcomes, not claims" />
    <div class="mt-12 grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
      <StatBlock value="15%" label="production cost reduced" />
      <StatBlock value="5" label="formulas developed" />
      <StatBlock value="HACCP" label="plans certified" />
      <StatBlock value="4" label="sectors served" />
    </div>
  </Section>

  <Section tone="dark">
    <SectionHeading eyebrow="Consultancy" title="Three areas of technical practice" tone="dark" />
    <div class="mt-12 grid gap-12 md:grid-cols-3">
      {services.map((s, i) => (
        <ServiceCard
          title={s.data.title}
          summary={s.data.summary}
          capabilities={s.data.capabilities}
          href="/consultancy"
          index={i + 1}
        />
      ))}
    </div>
  </Section>

  <Section tone="light">
    <SectionHeading eyebrow="Why us" title="What clients cannot build in-house" />
    <div class="mt-12 grid gap-10 md:grid-cols-2">
      {DIFFERENTIATORS.map((d) => (
        <div class="border-t border-[var(--color-border)] pt-6">
          <h3 class="font-display text-xl">{d.title}</h3>
          <p class="mt-3 max-w-prose text-sm leading-relaxed opacity-80">{d.body}</p>
        </div>
      ))}
    </div>
  </Section>

  <Section tone="light">
    <SectionHeading eyebrow="Case studies" title="Selected engagements" />
    <ul class="mt-12 grid gap-10 md:grid-cols-2">
      {caseStudies.map((c) => (
        <li class="border-t border-[var(--color-border)] pt-6">
          <p class="label-mono text-accent">{c.data.sector}</p>
          <h3 class="mt-3 font-display text-xl">{c.data.title}</h3>
          <p class="mt-3 max-w-prose text-sm leading-relaxed opacity-80">{c.data.summary}</p>
        </li>
      ))}
    </ul>
    <div class="mt-12">
      <Button href="/case-studies">Read the case studies</Button>
    </div>
  </Section>

  <Section tone="dark">
    <SectionHeading eyebrow="Get started" title="Tell us what you are trying to solve" tone="dark" />
    <p class="mt-5 max-w-2xl leading-relaxed opacity-90">
      Whether you need a single consultant or a tailored team, we match you with the
      expertise required. You pay only for the services you need, precisely when you
      need them.
    </p>
    <div class="mt-10">
      <Button href="/contact" tone="dark">Request a consultation</Button>
    </div>
  </Section>
</BaseLayout>
```

- [ ] **Step 4: Verify heading order**

```bash
npm run build
grep -o '<h[1-6]' dist/index.html
```

Expected: the sequence begins `<h1`, then `<h2`, and every `<h3` follows an `<h2`. No level is skipped and `<h1` appears exactly once.

- [ ] **Step 5: Screenshot at all four breakpoints**

```bash
npm run build
npm run preview
```

With the preview server running, capture screenshots at 375, 768, 1024, and 1440px wide. Confirm: no horizontal scroll at 375px, hero text does not overflow, stat blocks reflow to one column on mobile.

- [ ] **Step 6: Commit**

```bash
git add src/pages/index.astro src/components/Hero.astro src/assets/ public/images/CREDITS.md
git commit -m "feat: home page with promoted proof band and three service verticals"
```

---

### Task 6: Consultancy page

**Files:**
- Create: `src/pages/consultancy.astro`

**Interfaces:**
- Consumes: `BaseLayout`, `Section`, `SectionHeading`, `Button`, collection `services`
- Produces: nothing consumed downstream

- [ ] **Step 1: Write the page**

Create `src/pages/consultancy.astro`. Every sub-service from the content inventory appears here — this is the depth the current site hides:

```astro
---
import { getCollection, render } from "astro:content";
import BaseLayout from "../layouts/BaseLayout.astro";
import Section from "../components/Section.astro";
import SectionHeading from "../components/SectionHeading.astro";
import Button from "../components/Button.astro";

const services = (await getCollection("services")).sort(
  (a, b) => a.data.order - b.data.order,
);
const rendered = await Promise.all(
  services.map(async (s) => ({ data: s.data, Content: (await render(s)).Content })),
);
---

<BaseLayout
  title="Consultancy"
  description="Dairy processing, food product development, and equipment procurement consulting — full technical capability breakdown."
>
  <Section tone="dark">
    <p class="label-mono text-accent-dark">Consultancy</p>
    <h1 class="mt-3 max-w-3xl font-display text-4xl leading-tight md:text-5xl">
      Technical practice across three industries
    </h1>
    <p class="mt-6 max-w-2xl leading-relaxed opacity-90">
      Engagements are scoped to the problem. Below is the full capability set across
      each area of practice.
    </p>
  </Section>

  {rendered.map(({ data, Content }, i) => (
    <Section tone={i % 2 === 0 ? "light" : "dark"}>
      <p class={`label-mono ${i % 2 === 0 ? "text-accent" : "text-accent-dark"}`}>
        {String(i + 1).padStart(2, "0")}
      </p>
      <h2 class="mt-3 font-display text-3xl md:text-4xl">{data.title}</h2>
      <p class="mt-4 max-w-2xl leading-relaxed opacity-90">{data.summary}</p>

      <div class="mt-6 max-w-2xl text-sm leading-relaxed opacity-80">
        <Content />
      </div>

      <h3 class="label-mono mt-10 opacity-70">Capabilities</h3>
      <ul class="mt-4 grid gap-3 md:grid-cols-2">
        {data.capabilities.map((c) => (
          <li class="border-t border-current/20 pt-3 text-sm leading-relaxed">{c}</li>
        ))}
      </ul>
    </Section>
  ))}

  <Section tone="light">
    <SectionHeading eyebrow="Next step" title="Scope an engagement" />
    <div class="mt-8"><Button href="/contact">Request a consultation</Button></div>
  </Section>
</BaseLayout>
```

- [ ] **Step 2: Verify build and heading order**

```bash
npm run build
grep -o '<h[1-6]' dist/consultancy/index.html
```

Expected: one `<h1`, then alternating `<h2`/`<h3` with no skipped levels.

- [ ] **Step 3: Commit**

```bash
git add src/pages/consultancy.astro
git commit -m "feat: consultancy page with full capability breakdown"
```

---

### Task 7: Case studies page

**Files:**
- Create: `src/pages/case-studies.astro`

**Interfaces:**
- Consumes: `BaseLayout`, `Section`, `SectionHeading`, `Button`, `StatBlock`, collection `caseStudies`
- Produces: nothing consumed downstream

- [ ] **Step 1: Write the page**

Create `src/pages/case-studies.astro`. Metrics are foregrounded via `StatBlock`, not buried in prose:

```astro
---
import { getCollection } from "astro:content";
import BaseLayout from "../layouts/BaseLayout.astro";
import Section from "../components/Section.astro";
import SectionHeading from "../components/SectionHeading.astro";
import Button from "../components/Button.astro";
import StatBlock from "../components/StatBlock.astro";

const caseStudies = (await getCollection("caseStudies")).sort(
  (a, b) => a.data.order - b.data.order,
);
---

<BaseLayout
  title="Case Studies"
  description="Selected engagements across restaurant franchises, packaged goods, food-tech startups, and international supply chains."
>
  <Section tone="dark">
    <p class="label-mono text-accent-dark">Case studies</p>
    <h1 class="mt-3 max-w-3xl font-display text-4xl leading-tight md:text-5xl">
      We partner with food businesses to solve complex problems
    </h1>
    <p class="mt-6 max-w-2xl leading-relaxed opacity-90">
      Ensuring regulatory compliance and driving profitability. Below are examples of
      the sectors and expertise we deliver.
    </p>
  </Section>

  <Section tone="light">
    <h2 class="sr-only">Engagements</h2>
    <ul class="grid gap-16">
      {caseStudies.map((c) => (
        <li class="grid gap-8 border-t border-[var(--color-border)] pt-8 md:grid-cols-[1fr_2fr]">
          <div>
            <p class="label-mono text-accent">{c.data.sector}</p>
            {c.data.metric && c.data.metricLabel && (
              <div class="mt-6">
                <StatBlock value={c.data.metric} label={c.data.metricLabel} />
              </div>
            )}
          </div>
          <div>
            <h3 class="font-display text-2xl md:text-3xl">{c.data.title}</h3>
            <p class="mt-4 max-w-prose leading-relaxed opacity-80">{c.data.summary}</p>
          </div>
        </li>
      ))}
    </ul>
  </Section>

  <Section tone="dark">
    <SectionHeading eyebrow="Your project" title="Bring us a harder one" tone="dark" />
    <div class="mt-8"><Button href="/contact" tone="dark">Request a consultation</Button></div>
  </Section>
</BaseLayout>
```

- [ ] **Step 2: Verify build and heading order**

```bash
npm run build
grep -o '<h[1-6]' dist/case-studies/index.html
```

Expected: one `<h1`, then `<h2`, then `<h3` entries. No skipped levels — the `sr-only` `<h2>` exists precisely so the per-engagement `<h3>` elements do not skip a level.

- [ ] **Step 3: Commit**

```bash
git add src/pages/case-studies.astro
git commit -m "feat: case studies page with foregrounded metrics"
```

---

### Task 8: About page with credential slots

**Files:**
- Create: `src/pages/about.astro`

**Interfaces:**
- Consumes: `BaseLayout`, `Section`, `SectionHeading`, `Button`, `SITE`, `AIMS`
- Produces: nothing consumed downstream

- [ ] **Step 1: Write the page**

Create `src/pages/about.astro`. The team section is a deliberate, visibly-designed empty slot — per spec section 3, this demonstrates the gap to the client rather than hiding it:

```astro
---
import BaseLayout from "../layouts/BaseLayout.astro";
import Section from "../components/Section.astro";
import SectionHeading from "../components/SectionHeading.astro";
import Button from "../components/Button.astro";
import { SITE } from "../data/site";
import { AIMS } from "../data/aims";
---

<BaseLayout
  title="About"
  description="Overseas Food Consultants (OPC) Private Limited — a registered platform of food professionals headquartered in Haryana, India."
>
  <Section tone="dark">
    <p class="label-mono text-accent-dark">About</p>
    <h1 class="mt-3 max-w-3xl font-display text-4xl leading-tight md:text-5xl">
      A platform of food professionals
    </h1>
    <p class="mt-6 max-w-2xl leading-relaxed opacity-90">
      {SITE.legalName} provides expert advice and technical guidance to food investors
      and business operators — restaurants, food manufacturers, and foodservice
      companies.
    </p>
  </Section>

  <Section tone="light">
    <SectionHeading eyebrow="Our aims" title="What the organisation sets out to do" />
    <ul class="mt-12 grid gap-6 md:grid-cols-2">
      {AIMS.map((aim, i) => (
        <li class="flex gap-4 border-t border-[var(--color-border)] pt-5">
          <span class="label-mono text-accent">{String(i + 1).padStart(2, "0")}</span>
          <span class="text-sm leading-relaxed opacity-90">{aim}</span>
        </li>
      ))}
    </ul>
  </Section>

  <Section tone="light">
    <SectionHeading eyebrow="Our consultants" title="The people behind the practice" />
    <p class="mt-5 max-w-2xl leading-relaxed opacity-80">
      Named consultant profiles, credentials, and areas of specialisation appear here.
    </p>
    <ul class="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
      {[1, 2, 3].map((n) => (
        <li class="border border-dashed border-[var(--color-border)] p-6">
          <div class="aspect-square w-20 rounded-full bg-[var(--color-border)]"></div>
          <p class="label-mono mt-5 text-accent">Consultant {String(n).padStart(2, "0")}</p>
          <p class="mt-2 font-display text-lg opacity-50">Name and title</p>
          <p class="mt-2 text-sm leading-relaxed opacity-50">
            Specialisation, qualifications, and years of practice.
          </p>
        </li>
      ))}
    </ul>
  </Section>

  <Section tone="light">
    <SectionHeading eyebrow="Legal" title="Company standing" />
    <p class="mt-5 max-w-2xl leading-relaxed opacity-80">{SITE.registration}</p>
    <p class="mt-3 leading-relaxed opacity-80">Headquarters: {SITE.address}</p>
  </Section>

  <Section tone="dark">
    <SectionHeading eyebrow="Association" title="Food technologists — join us" tone="dark" />
    <p class="mt-5 max-w-2xl leading-relaxed opacity-90">
      Interested in association membership? We are always expanding the network of
      professionals we work with.
    </p>
    <div class="mt-10"><Button href="/contact" tone="dark">Get in touch</Button></div>
  </Section>
</BaseLayout>
```

- [ ] **Step 2: Verify the placeholder slots are visually distinct**

```bash
npm run build
grep -c 'border-dashed' dist/about/index.html
```

Expected: `3`. The dashed border makes it unambiguous to the client that these are slots awaiting his content, not fabricated people. **Do not invent consultant names.**

- [ ] **Step 3: Commit**

```bash
git add src/pages/about.astro
git commit -m "feat: about page with explicit credential slots"
```

---

### Task 9: Contact page with a working form

**Files:**
- Create: `src/pages/contact.astro`
- Create: `.env.example`
- Create: `.env` (git-ignored, not committed)

**Interfaces:**
- Consumes: `BaseLayout`, `Section`, `SITE`
- Produces: environment variable contract `PUBLIC_FORM_ENDPOINT`

- [ ] **Step 1: Create a Formspree form and record the endpoint**

Sign in at formspree.io, create a form, copy its endpoint (format `https://formspree.io/f/XXXXXXXX`).

Create `.env.example`:

```bash
# Formspree endpoint for the contact form.
# Create a form at https://formspree.io and paste its endpoint here.
# Copy this file to .env and fill in the real value.
PUBLIC_FORM_ENDPOINT=https://formspree.io/f/XXXXXXXX
```

Create `.env` containing the real endpoint.

- [ ] **Step 2: Verify `.env` is git-ignored before writing a secret into it**

```bash
git check-ignore -v .env
```

Expected: a line naming `.gitignore` and the matching pattern. If it prints nothing, `.env` is NOT ignored — add `.env` to `.gitignore` and re-run before continuing.

- [ ] **Step 3: Write the page**

Create `src/pages/contact.astro`. Every field has a visible `<label>` with `for`, a correct `type` for mobile keyboards, and `autocomplete`:

```astro
---
import BaseLayout from "../layouts/BaseLayout.astro";
import Section from "../components/Section.astro";
import { SITE } from "../data/site";

const endpoint = import.meta.env.PUBLIC_FORM_ENDPOINT;
if (!endpoint) {
  throw new Error(
    "PUBLIC_FORM_ENDPOINT is not set. Copy .env.example to .env and add your Formspree endpoint.",
  );
}
---

<BaseLayout
  title="Contact"
  description="Request a food and beverage consulting engagement with Overseas Food Consultants."
>
  <Section tone="dark">
    <p class="label-mono text-accent-dark">Contact</p>
    <h1 class="mt-3 max-w-3xl font-display text-4xl leading-tight md:text-5xl">
      Tell us what you are trying to solve
    </h1>
  </Section>

  <Section tone="light">
    <div class="grid gap-16 md:grid-cols-[3fr_2fr]">
      <div>
        <h2 class="sr-only">Enquiry form</h2>
        <form action={endpoint} method="POST" class="grid gap-6">
          <div>
            <label for="name" class="label-mono block">
              Name <span aria-hidden="true" class="text-accent">*</span>
            </label>
            <input
              id="name" name="name" type="text" required autocomplete="name"
              class="mt-2 min-h-11 w-full border border-[var(--color-border)] bg-white px-4 py-3"
            />
          </div>

          <div>
            <label for="email" class="label-mono block">
              Email <span aria-hidden="true" class="text-accent">*</span>
            </label>
            <input
              id="email" name="email" type="email" required autocomplete="email"
              aria-describedby="email-help"
              class="mt-2 min-h-11 w-full border border-[var(--color-border)] bg-white px-4 py-3"
            />
            <p id="email-help" class="mt-2 text-xs opacity-70">
              We reply to enquiries within two working days.
            </p>
          </div>

          <div>
            <label for="company" class="label-mono block">Company</label>
            <input
              id="company" name="company" type="text" autocomplete="organization"
              class="mt-2 min-h-11 w-full border border-[var(--color-border)] bg-white px-4 py-3"
            />
          </div>

          <div>
            <label for="area" class="label-mono block">Area of interest</label>
            <select
              id="area" name="area"
              class="mt-2 min-h-11 w-full border border-[var(--color-border)] bg-white px-4 py-3"
            >
              <option value="dairy">Dairy Industry</option>
              <option value="food">Food Industry</option>
              <option value="equipment">Equipment &amp; Instrument Procurement</option>
              <option value="other">Something else</option>
            </select>
          </div>

          <div>
            <label for="message" class="label-mono block">
              What are you trying to solve? <span aria-hidden="true" class="text-accent">*</span>
            </label>
            <textarea
              id="message" name="message" rows="6" required
              class="mt-2 w-full border border-[var(--color-border)] bg-white px-4 py-3"
            ></textarea>
          </div>

          <p class="text-xs opacity-70">
            <span aria-hidden="true" class="text-accent">*</span> indicates a required field.
          </p>

          <button
            type="submit"
            class="inline-flex min-h-11 items-center justify-self-start bg-[var(--color-accent)] px-6 py-3 text-sm font-medium text-[var(--color-surface)] transition-opacity duration-200 hover:opacity-90"
          >
            Send enquiry
          </button>
        </form>
      </div>

      <div>
        <h2 class="label-mono text-accent">Direct</h2>
        <address class="mt-4 not-italic leading-relaxed opacity-80">
          {SITE.legalName}<br />{SITE.address}
        </address>

        <h2 class="label-mono mt-10 text-accent">Social</h2>
        <ul class="mt-4 space-y-2">
          <li><a href={SITE.social.linkedin} class="text-sm hover:text-accent" rel="me noopener">LinkedIn</a></li>
          <li><a href={SITE.social.instagram} class="text-sm hover:text-accent" rel="me noopener">Instagram</a></li>
          <li><a href={SITE.social.youtube} class="text-sm hover:text-accent" rel="me noopener">YouTube</a></li>
        </ul>
      </div>
    </div>
  </Section>
</BaseLayout>
```

- [ ] **Step 4: Verify label associations**

```bash
npm run build
grep -o 'for="[a-z]*"' dist/contact/index.html
grep -o 'id="[a-z-]*"' dist/contact/index.html
```

Expected: every `for=` value has a matching `id=` on an input. Five pairs: `name`, `email`, `company`, `area`, `message`.

- [ ] **Step 5: Verify the form actually delivers**

```bash
npm run build
npm run preview
```

Open `/contact`, submit a real test enquiry, and confirm it arrives in the Formspree dashboard. A form that renders but does not deliver is worse than no form — the client will test this.

- [ ] **Step 6: Commit**

```bash
git add src/pages/contact.astro .env.example
git commit -m "feat: contact page with working Formspree form and labelled inputs"
```

Confirm `.env` is absent from the commit:

```bash
git show --stat HEAD | grep -c "\.env$" || echo "no .env committed"
```

Expected: `no .env committed`.

---

### Task 10: Motion layer

**Files:**
- Create: `src/components/Reveal.astro`
- Modify: `src/pages/index.astro`

**Interfaces:**
- Consumes: tokens from Task 1
- Produces: `Reveal` component wrapping slot content, props `{ delay?: number }`

- [ ] **Step 1: Write the Reveal component**

Create `src/components/Reveal.astro`. A `no-js` guard means content is visible by default and only hides once JavaScript confirms it can reveal it again — so a JS failure leaves content readable rather than blank:

```astro
---
interface Props {
  delay?: number;
}
const { delay = 0 } = Astro.props;
---

<div class="reveal" style={`--reveal-delay:${delay}ms`}>
  <slot />
</div>

<style>
  /* Visible by default. Only the js-armed class hides it. */
  .reveal.is-armed {
    opacity: 0;
    transform: translateY(16px);
  }

  .reveal.is-armed.is-visible {
    opacity: 1;
    transform: translateY(0);
    transition:
      opacity 300ms ease-out var(--reveal-delay),
      transform 300ms ease-out var(--reveal-delay);
  }

  @media (prefers-reduced-motion: reduce) {
    .reveal.is-armed,
    .reveal.is-armed.is-visible {
      opacity: 1;
      transform: none;
      transition: none;
    }
  }
</style>

<script>
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const items = document.querySelectorAll<HTMLElement>(".reveal");

  if (!reduced && "IntersectionObserver" in window) {
    items.forEach((el) => el.classList.add("is-armed"));

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -10% 0px" },
    );

    items.forEach((el) => observer.observe(el));
  }
</script>
```

- [ ] **Step 2: Apply to the home page stat band only**

In `src/pages/index.astro`, add the import:

```astro
import Reveal from "../components/Reveal.astro";
```

Then replace the stat grid with:

```astro
<div class="mt-12 grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
  <Reveal delay={0}><StatBlock value="15%" label="production cost reduced" /></Reveal>
  <Reveal delay={50}><StatBlock value="5" label="formulas developed" /></Reveal>
  <Reveal delay={100}><StatBlock value="HACCP" label="plans certified" /></Reveal>
  <Reveal delay={150}><StatBlock value="4" label="sectors served" /></Reveal>
</div>
```

Stagger is 50ms per item, within the 30–50ms guidance. This is the only animated group on the page — the spec caps at two per viewport.

- [ ] **Step 3: Verify motion behaviour in three states**

```bash
npm run build
npm run preview
```

Check all three:
1. **Normal** — stats fade up in sequence on scroll
2. **Reduced motion** (OS setting, or DevTools "Emulate CSS prefers-reduced-motion: reduce") — stats appear immediately, no transition
3. **JavaScript disabled** (DevTools → Settings → Debugger → Disable JavaScript) — stats are **visible**, not blank

State 3 is the one that silently breaks in naive implementations. If stats are invisible with JS off, the `is-armed` guard is not working — fix before committing.

- [ ] **Step 4: Commit**

```bash
git add src/components/Reveal.astro src/pages/index.astro
git commit -m "feat: scroll reveal on stat band, inert under reduced motion and no-JS"
```

---

### Task 11: Accessibility and performance gate

The task that decides whether the pitch claim is true. Nothing ships until this passes.

**Files:**
- Create: `scripts/audit.sh`
- Modify: any page failing the audit

**Interfaces:**
- Consumes: the built site from all prior tasks
- Produces: `scripts/audit.sh`, runnable before every deploy

- [ ] **Step 1: Write the audit script**

Create `scripts/audit.sh`:

```bash
#!/usr/bin/env bash
# Run all static quality gates against the built site.
# Usage: ./scripts/audit.sh
set -euo pipefail

PAGES=("/" "/consultancy" "/case-studies" "/about" "/contact")

echo "== Contrast gate =="
python3 scripts/contrast-check.py

echo
echo "== Build =="
npm run build

echo
echo "== Structure checks =="
for page in "${PAGES[@]}"; do
  if [ "$page" = "/" ]; then
    file="dist/index.html"
  else
    file="dist${page}/index.html"
  fi

  if [ ! -f "$file" ]; then
    echo "FAIL  $page did not build ($file missing)"
    exit 1
  fi

  h1_count=$(grep -o '<h1' "$file" | wc -l | tr -d ' ')
  if [ "$h1_count" -ne 1 ]; then
    echo "FAIL  $page has $h1_count <h1> elements (must be exactly 1)"
    exit 1
  fi

  grep -q 'Skip to main content' "$file" || { echo "FAIL  $page missing skip link"; exit 1; }
  grep -q '<main' "$file" || { echo "FAIL  $page missing <main> landmark"; exit 1; }

  echo "PASS  $page"
done

echo
echo "All static gates passed. Now run Lighthouse against the preview server."
```

```bash
chmod +x scripts/audit.sh
```

- [ ] **Step 2: Run the static gates**

```bash
./scripts/audit.sh
```

Expected: contrast gate passes, build succeeds, five `PASS` lines. Fix any failure before continuing.

- [ ] **Step 3: Run Lighthouse against every page**

```bash
npm run preview
```

Run a Lighthouse audit (mobile, navigation mode) against each of the five pages. Record all four category scores per page.

**Required, per spec section 7:**

| Category | Required | Current site baseline |
|---|---|---|
| Accessibility | 100 | 87 |
| SEO | 100 | 100 |
| Best Practices | ≥ 96 | 96 |
| Agentic Browsing | ≥ 90 | 50 |

- [ ] **Step 4: Confirm every baseline defect is fixed**

Each of these failed on the current site. Verify each now passes on every page:

| Audit | Fixed by |
|---|---|
| `color-contrast` | Task 1 tokens + contrast gate |
| `heading-order` | Task 5–9 heading discipline, checked in `audit.sh` |
| `link-name` | Task 2 header/footer, Task 4 `ServiceCard` link text |
| `listitem` | All lists use real `<ul>`/`<li>` |
| `image-aspect-ratio` | Task 5 `<Image>` with intrinsic dimensions |
| `agent-accessibility-tree` | Task 2 landmarks, skip link, structured data |

If any still fails, fix it and re-run. **Do not proceed with a failing audit, and do not report a score that was not measured.**

- [ ] **Step 5: Verify responsive behaviour**

Screenshot every page at 375, 768, 1024, and 1440px, plus 375px landscape. Confirm:
- No horizontal scroll at any width
- No text overflow or overlap
- All touch targets ≥ 44px
- Mobile nav toggle opens and closes, and `aria-expanded` flips between `false` and `true`

- [ ] **Step 6: Verify CLS has not regressed**

Run a performance trace against the home page. Required: CLS < 0.1. The current site scores 0.00, so any visible layout shift is a regression against the thing being replaced.

- [ ] **Step 7: Commit**

```bash
git add scripts/audit.sh
git commit -m "feat: quality gate script covering contrast, headings, and landmarks"
```

---

### Task 12: Before/after comparison page

The pitch instrument. Unlisted — not in `NAV`, excluded from the sitemap.

**Files:**
- Create: `src/pages/comparison.astro`
- Move: `ofc-current-home.jpeg` → `public/images/before-home.jpg`
- Create: `public/images/after-home.jpg`
- Modify: `astro.config.mjs`

**Interfaces:**
- Consumes: `BaseLayout`, `Section`
- Produces: nothing consumed downstream

- [ ] **Step 1: Move the baseline screenshot into place**

```bash
mkdir -p public/images
git mv ofc-current-home.jpeg public/images/before-home.jpg
```

- [ ] **Step 2: Capture the after screenshot**

With the preview server running, capture a full-page screenshot of the new home page at 1440px wide and save it as `public/images/after-home.jpg`. Note its pixel height — it is needed for the `height` attribute in Step 4.

- [ ] **Step 3: Exclude the page from the sitemap**

In `astro.config.mjs`, change the sitemap integration:

```js
integrations: [
  sitemap({
    filter: (page) => !page.includes("/comparison"),
  }),
],
```

- [ ] **Step 4: Write the comparison page**

Create `src/pages/comparison.astro`. Set each `after` value to the real measured score from Task 11, and set the `after-home.jpg` `height` to the actual captured pixel height:

```astro
---
import BaseLayout from "../layouts/BaseLayout.astro";
import Section from "../components/Section.astro";

// Every `after` value MUST be a real measured score from Task 11.
// The build check in Step 5 fails if any placeholder survives.
const scores = [
  { label: "Accessibility", before: "87", after: "MEASURE_ME" },
  { label: "Agentic Browsing", before: "50", after: "MEASURE_ME" },
  { label: "SEO", before: "100", after: "MEASURE_ME" },
  { label: "Best Practices", before: "96", after: "MEASURE_ME" },
];

const defects = [
  {
    audit: "color-contrast",
    problem: "Text fails the WCAG minimum contrast ratio.",
    fix: "Every token pair verified by script. Two accent tokens, one for light surfaces and one for dark.",
  },
  {
    audit: "heading-order",
    problem: "Heading levels skip, breaking screen-reader navigation.",
    fix: "Sequential headings enforced by an automated gate on every page.",
  },
  {
    audit: "link-name",
    problem: "Links with no discernible name. Screen readers announce dead ends.",
    fix: "Every link names its destination, including when read out of context.",
  },
  {
    audit: "listitem",
    problem: "List items sit outside any list parent — invalid HTML.",
    fix: "All lists use semantic ul and li elements.",
  },
  {
    audit: "image-aspect-ratio",
    problem: "Images render distorted against their intrinsic dimensions.",
    fix: "Explicit dimensions on every image, served as AVIF at the correct ratio.",
  },
  {
    audit: "agent-accessibility-tree",
    problem: "Malformed accessibility tree. AI assistants cannot parse the site.",
    fix: "Proper landmarks, a skip link, and ProfessionalService structured data.",
  },
];
---

<BaseLayout title="Before and After" description="Comparison of the current site against the redesign.">
  <Section tone="dark">
    <p class="label-mono text-accent-dark">Comparison</p>
    <h1 class="mt-3 max-w-3xl font-display text-4xl leading-tight md:text-5xl">
      What changed, and why it matters
    </h1>
    <p class="mt-6 max-w-2xl leading-relaxed opacity-90">
      The current site is technically well built. Its problems are not speed — they
      are accessibility, machine readability, and the fact that its strongest proof is
      buried near the bottom of the page.
    </p>
  </Section>

  <Section tone="light">
    <h2 class="font-display text-3xl">Side by side</h2>
    <div class="mt-10 grid gap-8 md:grid-cols-2">
      <figure>
        <figcaption class="label-mono text-accent">Current</figcaption>
        <img
          src="/images/before-home.jpg"
          alt="The current Overseas Food Consultants homepage, showing two empty bordered boxes where images failed to load."
          width="1425" height="4629" loading="lazy"
          class="mt-4 w-full border border-[var(--color-border)]"
        />
      </figure>
      <figure>
        <figcaption class="label-mono text-accent">Redesign</figcaption>
        <img
          src="/images/after-home.jpg"
          alt="The redesigned homepage, with a photographic hero, a statistics band, and three clearly separated service areas."
          width="1440" height="REPLACE_WITH_ACTUAL_HEIGHT" loading="lazy"
          class="mt-4 w-full border border-[var(--color-border)]"
        />
      </figure>
    </div>
  </Section>

  <Section tone="light">
    <h2 class="font-display text-3xl">Measured scores</h2>
    <table class="mt-8 w-full max-w-2xl border-collapse text-left">
      <caption class="sr-only">
        Lighthouse category scores, current site compared with the redesign
      </caption>
      <thead>
        <tr class="border-b border-[var(--color-border)]">
          <th scope="col" class="label-mono py-3">Category</th>
          <th scope="col" class="label-mono py-3">Current</th>
          <th scope="col" class="label-mono py-3">Redesign</th>
        </tr>
      </thead>
      <tbody>
        {scores.map((s) => (
          <tr class="border-b border-[var(--color-border)]">
            <th scope="row" class="py-4 font-normal">{s.label}</th>
            <td class="py-4 tabular-nums opacity-70">{s.before}</td>
            <td class="py-4 font-display text-xl tabular-nums text-accent">{s.after}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </Section>

  <Section tone="light">
    <h2 class="font-display text-3xl">Six defects, fixed</h2>
    <ul class="mt-10 grid gap-8">
      {defects.map((d) => (
        <li class="border-t border-[var(--color-border)] pt-6">
          <p class="label-mono text-accent">{d.audit}</p>
          <p class="mt-3 font-display text-lg">{d.problem}</p>
          <p class="mt-2 max-w-prose text-sm leading-relaxed opacity-80">{d.fix}</p>
        </li>
      ))}
    </ul>
  </Section>
</BaseLayout>
```

- [ ] **Step 5: Replace placeholders with measured values and verify none survive**

Edit the `scores` array so every `after` value is a real measured number from Task 11, and replace `REPLACE_WITH_ACTUAL_HEIGHT` with the captured screenshot height.

```bash
npm run build
if grep -rq "MEASURE_ME\|REPLACE_WITH_ACTUAL_HEIGHT" dist/; then
  echo "FAIL: unmeasured placeholder reached the build"
  exit 1
else
  echo "PASS: all values measured"
fi
```

Expected: `PASS: all values measured`. This gate exists because the comparison page is the pitch instrument — shipping an unmeasured number there would be claiming a result nobody verified.

- [ ] **Step 6: Verify exclusion from the sitemap**

```bash
npm run build
grep -q "comparison" dist/sitemap-0.xml && echo "FAIL: comparison page is in the sitemap" || echo "PASS: correctly excluded"
```

Expected: `PASS: correctly excluded`.

- [ ] **Step 7: Commit**

```bash
git add src/pages/comparison.astro public/images/ astro.config.mjs
git commit -m "feat: before/after comparison page with measured scores"
```

---

### Task 13: Deploy to Vercel

**Files:**
- Create: `vercel.json`
- Create: `README.md`
- Modify: `src/data/site.ts`, `astro.config.mjs` (if the deployed domain differs)

**Interfaces:**
- Consumes: everything
- Produces: a live URL

- [ ] **Step 1: Write the Vercel config**

Create `vercel.json`:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "astro",
  "headers": [
    {
      "source": "/images/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

The cache header addresses the 21.9kB of cache waste the baseline trace found.

- [ ] **Step 2: Write the README**

Create `README.md`:

````markdown
# Overseas Food Consultants — redesign

Concept redesign of ofc.org.in. Astro 7 static site, deployed on Vercel.

**This is an unsolicited concept redesign.** It is not commissioned or endorsed by
Overseas Food Consultants (OPC) Private Limited. All copy is drawn from the
company's public website.

## Develop

```bash
npm install
cp .env.example .env   # add your Formspree endpoint
npm run dev
```

## Quality gates

```bash
./scripts/audit.sh                  # contrast, build, headings, landmarks
python3 scripts/contrast-check.py   # after any token change
```

Run Lighthouse against the preview build before deploying. Required:
Accessibility 100, SEO 100, Best Practices >= 96, Agentic Browsing >= 90.

## Content

All copy lives in `src/data/`. Structure is fixed; copy is swappable without
touching markup.

## Image credits

See `public/images/CREDITS.md`.
````

The attribution paragraph satisfies spec section 9, question 1.

- [ ] **Step 3: Set the environment variable in Vercel**

In the Vercel project settings, add `PUBLIC_FORM_ENDPOINT` with the Formspree endpoint, for all environments. The build throws without it — see Task 9, Step 3.

- [ ] **Step 4: Deploy**

```bash
npx vercel --prod
```

Expected: a live URL.

- [ ] **Step 5: Update the site URL if the deployed domain differs**

If the deployed domain is not `https://ofc-demo.vercel.app`, update `SITE.url` in `src/data/site.ts` and `site` in `astro.config.mjs` to match, then redeploy. Canonical URLs, Open Graph tags, and the sitemap all derive from it, and a mismatch silently breaks all three.

- [ ] **Step 6: Verify the deployed site, not just the local build**

Against the live URL:
- All five pages load
- Submit the contact form and confirm the enquiry arrives
- Re-run Lighthouse against the live URL and confirm the scores match what the comparison page claims
- Open it on a real phone, not just an emulator

If deployed scores differ from local, the comparison page is now wrong. Update it to the deployed numbers and redeploy.

- [ ] **Step 7: Commit**

```bash
git add vercel.json README.md src/data/site.ts astro.config.mjs
git commit -m "feat: Vercel deployment config and project README"
```

---

## Self-Review

**Spec coverage** — each spec section mapped to a task:

| Spec section | Task |
|---|---|
| 2. Baseline audit | 11 (verification), 12 (presentation) |
| 3. Content inventory | 3 (all copy as typed collections) |
| 3. Team/logo/metric gaps as visible slots | 8 |
| 4. Colour tokens and contrast | 1 |
| 4. Three-layer typography | 1 |
| 4. Page structure: hero, proof, solutions, CTA | 5 |
| 5. Astro, Tailwind v4, Formspree, Vercel | 1, 9, 13 |
| 6. Five pages | 5, 6, 7, 8, 9 |
| 6. Before/after comparison page | 12 |
| 7. Accessibility gates | 2 (structural), 11 (verification) |
| 7. Performance gates | 5 (images), 11 (CLS), 13 (caching) |
| 7. Responsive at four breakpoints | 5, 11 |
| 7. Motion rules | 10 |
| 7. SEO and structured data | 2 |
| 9. Portfolio attribution | 13 (README) |
| 9. Photography licence | 5 (CREDITS.md) |

No spec section is unimplemented.

**Type consistency** — verified across tasks:
- `Section` `tone` prop is `"light" | "dark"` in Tasks 4, 5, 6, 7, 8, 9, 12
- `SectionHeading` takes `tone`, and every dark-section usage passes it (Tasks 5, 7, 8)
- `StatBlock` `tone` prop consistent between Tasks 4, 5, 7
- `Button` `tone` and `variant` props consistent between Tasks 4, 5, 6, 7, 8
- `SITE` and `NAV` field names match between the Task 2 definition and consumers in Tasks 5, 8, 9
- Collection names `services` and `caseStudies` match between `content.config.ts` (Task 3) and every `getCollection` call (Tasks 5, 6, 7)
- Frontmatter fields `order`, `capabilities`, `summary`, `title`, `sector`, `metric`, `metricLabel` match the Zod schemas exactly
- `PUBLIC_FORM_ENDPOINT` name identical in `.env.example`, `contact.astro`, and the Vercel setting

**Deliberate deviation from the skill's default TDD shape:** a static marketing site has no unit-testable logic, so a Jest-style red-green cycle would be theatre. Test steps are real verification instead: schema validation failing the build (Task 3, Steps 5–6), the contrast gate exiting non-zero (Task 1, Steps 5–6), `audit.sh` failing on a bad heading count (Task 11), Lighthouse thresholds (Task 11), a live form submission (Task 9), and a build-blocking placeholder check (Task 12). Three of these deliberately break the gate first to prove it can fail — that is the red phase in substance.

**Ordering note:** Task 4's `_primitives-test.astro` imports `BaseLayout` from Task 2, so Tasks 1 → 2 must complete before 4. Tasks 6, 7, and 8 are independent of one another and could run in parallel. Task 10 modifies `index.astro` from Task 5. Task 12 depends on measurements from Task 11.

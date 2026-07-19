# Overseas Food Consultants — Redesign Demo

**Date:** 2026-07-19
**Status:** Approved (direction), pending implementation plan
**Owner:** Owais
**Client path:** Owais → Diptisha's agency → Proshottam Rahul (OFC)

---

## 1. Context

Overseas Food Consultants (OPC) Private Limited is a B2B food & beverage technical
consultancy in Haryana, India. Its current site is `ofc.org.in`.

The client asked the agency for a demo showing how they would redesign it. The
agency does not want to over-invest before the client commits, so this demo must
be high perceived value at low build cost, and must double as the production
codebase if he signs.

**Deliverable:** a live, coded, static site on Vercel. Not a Figma prototype. The
client opens a real URL on his phone.

**Constraint:** no backend. Contact form posts to a third-party endpoint
(Formspree or equivalent) so it genuinely works without server code.

---

## 2. Baseline audit of the current site

Measured 2026-07-19 via Lighthouse (mobile, navigation mode) and a Chrome
performance trace.

| Category | Score |
|---|---|
| SEO | 100 |
| Best Practices | 96 |
| Accessibility | 87 |
| Agentic Browsing | 50 |
| CLS | 0.00 |

**The current site is technically competent.** Performance and SEO are not a
credible line of attack, and the pitch must not claim otherwise. The client can
verify these numbers himself.

### Real defects found

| Defect | Audit | Impact |
|---|---|---|
| Insufficient contrast | `color-contrast` | WCAG failure |
| Headings not sequential | `heading-order` | Breaks screen-reader navigation |
| Links without discernible name | `link-name` | Screen readers hit dead ends |
| `<li>` outside a list parent | `listitem` | Invalid HTML |
| Distorted images | `image-aspect-ratio` | Visible quality defect |
| Malformed accessibility tree | `agent-accessibility-tree` | Score 50 — AI assistants cannot parse the site |
| Two empty bordered boxes on the homepage | (visual) | Images fail to load in production |
| 828ms document latency | `DocumentLatency` | Slow first response |
| 204kB unoptimized image bytes | `ImageDelivery` | Wasted bandwidth |

### Design and content defects

- No food photography anywhere. A food consultancy illustrated with generic
  clipart infographics.
- Wall-of-text body copy with no scannable hierarchy.
- Proof is buried. "15% cost reduction", "5 new formulas", "HACCP certification"
  appear as plain body text near the bottom of the page.
- One call to action on the entire homepage.
- Three distinct service verticals exist on `/consultancy` but never surface on
  the homepage.
- No team, no named consultants, no client logos, no process, no engagement model.
  The site claims a "platform of food professionals" and names zero of them.

### Honest pitch angle

Lead with accessibility and machine-readability, not speed:

> Your site is invisible to screen readers and AI assistants, ships broken
> images, and fails colour contrast. Here is the same content, fixed — and
> better looking.

This is the one class of problem the client cannot see for himself, which makes
it persuasive rather than arguable.

---

## 3. Content inventory

All copy below was scraped from the live site on 2026-07-19. **The build does not
block on the client's promised email.** When that email arrives, copy is swapped
into the existing structure; the structure does not change.

**Identity**
- Overseas Food Consultants (OPC) Private Limited
- Tagline: "Your Source for Food Experts"
- Sub-tagline: "Elevating Your Food Business"
- Registered under the Companies Act 2013, Ministry of Corporate Affairs
- Headquarters: Haryana, India

**Three service verticals**
1. **Dairy Industry** — operational process layout design, raw material selection,
   process control, waste minimisation and by-product utilisation, qualitative and
   quantitative parameter determination, equipment specification, dairy-based
   functional formula development
2. **Food Industry** — new product development, cereal-dairy composite baked
   product development, storage capacity and shelf-life determination, cost
   calculation, root-cause analysis of product defects in beverages and baked
   goods, equipment specification
3. **Equipment & Instrument Procurement** — specification design for production
   and analytical equipment, competitive budgetary guidance, fabrication
   assistance

**Four differentiators** — Global Expertise, Customised Solutions, Innovative
Approach, Commitment to Quality

**Four case studies**
- Global restaurant franchises — menu standardisation, cost control, kitchen design
- Mid-size packaged goods company — 5 new formulas, 15% production cost reduction
- Next-generation food-tech startup — HACCP plan development, local and
  international compliance certification
- International supply chain networks — logistics troubleshooting, cold chain
  integrity, supplier auditing

**Six organisational aims** — new product and recipe development, sensory
evaluation and quality control, food processing system optimisation, food safety
and regulatory compliance, collaboration across chefs/farmers/manufacturers, and
consumer trend tracking

**Social** — LinkedIn `@overseas-food-consultants`, Instagram
`@overseas_foodconsultants`, Facebook Group, YouTube

**Known content gaps** — no team members, no client logos, no pricing or
engagement model, no metrics beyond the single 15% figure.

The demo builds **visible, well-designed slots** for team, logos, and metrics
with tasteful placeholders. This shows the client what he is missing and is
itself an argument for a larger engagement.

---

## 4. Design direction: "Editorial Lab"

Derived from the `ui-ux-pro-max` design-system database, cross-checked against
`frontend-design-direction`.

The database's top pattern match was **Trust & Authority + Conversion**, whose
listed anti-pattern is "hidden credentials" — precisely the current site's
failure. The direction keeps that pattern's conversion skeleton and applies an
editorial-scientific visual treatment.

### Positioning

A global expert practice, not a local vendor. The client's real differentiator is
technical depth — HACCP, shelf-life prediction, formula optimisation, equipment
specification. Precision work reads as editorial and scientific, not friendly and
illustrated.

### Page structure

1. **Hero** — mission and credibility, backed by real food photography
2. **Proof** — certifications, statistics, client sectors (promoted from position 5)
3. **Solution overview** — the three verticals, surfaced on the homepage
4. **Clear CTA path** — "Get a Consultation" in nav and inline

### Colour tokens

Rejected the database's food-sector matches (grocery green `#059669` / orange
`#D97706`) as consumer-retail and wrong for a B2B compliance firm. Adopted the
WCAG-adjusted premium palette instead.

| Token | Light surfaces | Dark surfaces |
|---|---|---|
| Base | `#1C1917` (stone-900) | — |
| Surface | `#FAFAF9` | `#1C1917` |
| Accent | `#A16207` (amber-700) | `#F59E0B` (amber-500) |
| Body text | `#0C0A09` | `#FAFAF9` |
| Border | `#D6D3D1` | — |
| Destructive | `#DC2626` | `#DC2626` |

**Two accent tokens, deliberately.** Measured contrast ratios:

- `#A16207` on `#FAFAF9` → **3.58:1**. Passes 3:1 for large text and UI chrome,
  fails 4.5:1 for body copy. Restricted to headings, rules, and icons.
- `#A16207` on `#1C1917` → **3.58:1**. Too low for a dark-surface CTA.
- `#F59E0B` on `#1C1917` → **8.25:1**. Used for all dark-surface accents.
- `#0C0A09` on `#F59E0B` → **9.78:1**. Used for amber CTA buttons.

A single amber token would silently fail WCAG across roughly half the page.

Warm stone plus amber also reads as grain, caramelisation, and oil without
resorting to literal food-brand orange.

### Typography — three layers

| Layer | Font | Role |
|---|---|---|
| Display | Newsreader | Editorial authority, headings |
| Body | Public Sans | Neutral, high legibility |
| Technical | JetBrains Mono | Uppercase, wide tracking — HACCP/ISO codes, spec numbers, service IDs, stat labels |

The mono layer is the memorable detail. It encodes a spec-sheet and lab-report
character without going brutalist, and no competitor in Indian food consulting is
using it. It is the element the client will point at.

### Explicit anti-patterns

Flagged by both skills, avoided throughout:

- AI purple/pink gradients
- Decorative blobs
- Cards nested inside cards
- Oversized vague hero copy
- Emoji used as icons (SVG only — Lucide or Heroicons)
- Stock-atmospheric filler imagery
- Hidden credentials

---

## 5. Technical approach

| Choice | Decision | Reason |
|---|---|---|
| Framework | Astro | Zero JS by default, markdown content collections the agency can edit, best-in-class image pipeline |
| Styling | Tailwind CSS v4 | Token-driven via CSS variables |
| Icons | Lucide | Single consistent stroke family |
| Images | Astro `<Image>`, AVIF/WebP, explicit dimensions | Prevents CLS, fixes the aspect-ratio defect |
| Forms | Formspree or equivalent | Genuinely functional without a backend |
| Hosting | Vercel | Instant preview URL to share |
| Fonts | Self-hosted, `font-display: swap`, preload display face only | Avoids FOIT and third-party latency |

Astro is chosen over Next.js because the site is pure marketing with no
application state. If the client later wants a CMS or blog, Astro content
collections or a headless CMS both slot in without a rewrite.

---

## 6. Scope

Five pages.

| Page | Contents |
|---|---|
| **Home** | Hero, proof band, three verticals, differentiators, case-study teasers, CTA |
| **Consultancy** | Full breakdown of all three verticals with every sub-service |
| **About** | Company, legal standing, aims, team slots with placeholders |
| **Case Studies** | The four engagements, expanded, metrics foregrounded |
| **Contact** | Working form, address, social links |

Plus one non-navigable **before/after comparison page**, unlisted, used only in
the pitch. Shows the current homepage beside the redesign, and lists the six
audit failures with their fixes.

### Out of scope

- CMS integration
- Blog
- Multi-language
- Any backend, authentication, or database
- Custom photography (licensed stock for the demo; production shoot is a
  separate line item in the quotation)

---

## 7. Quality gates

Every gate must pass before the URL is sent to the client.

**Accessibility** — target Lighthouse 100, up from 87
- Contrast ≥ 4.5:1 body, ≥ 3:1 large text and UI, verified not assumed
- Sequential heading order, single `h1` per page
- Every link and icon-only button has a discernible accessible name
- Valid list semantics
- Visible focus rings on all interactive elements
- Full keyboard navigation, skip-to-content link
- `prefers-reduced-motion` respected
- Agentic Browsing score raised from 50 toward 100

**Performance**
- CLS < 0.1 (currently 0.00 — must not regress)
- All images AVIF/WebP with explicit dimensions
- Lazy-load below the fold
- Document latency under the current 828ms

**Responsive** — verified at 375, 768, 1024, and 1440px, plus landscape

**Motion** — 150–300ms micro-interactions, `transform`/`opacity` only, exit
faster than enter, one to two animated elements per viewport maximum

**SEO** — hold at 100. Meta descriptions, Open Graph, `LocalBusiness` and
`ProfessionalService` structured data, sitemap, robots.

### Verification method

Design iterates through the `gan-design` generator/evaluator loop: build, capture
Playwright screenshots at all four breakpoints, score against the rubric above,
revise. Bounded iterations. Not a single pass declared finished.

---

## 8. Build-stage skills

| Skill | Applied to |
|---|---|
| `frontend-design` | Core build |
| `design-system` | Token file, component primitives |
| `motion-patterns` | Scroll reveals, state transitions |
| `frontend-a11y` | The accessibility gate |
| `seo` | Structured data, metadata |
| `gan-design` | Iteration and scoring loop |

---

## 9. Open questions

1. **Commercial terms.** Owais's cut is unagreed. The agency proposed that Owais
   "help a little" while they build; the actual decision is that Owais drives the
   build. This must be settled before implementation starts, not after the client
   approves.
2. **Domain for the demo.** Vercel subdomain, or something closer to the client's
   brand.
3. **Photography licence.** Stock is acceptable for the demo. Production use
   requires either licensed stock or a shoot — priced separately in the quotation.
4. **Who sends the quotation.** The client asked for it by email to himself. The
   agency owns that relationship.

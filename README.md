# Overseas Food Consultants — redesign

Concept redesign of [ofc.org.in](https://www.ofc.org.in/). Astro 7 static site,
deployed on Vercel.

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

Run Lighthouse against a production preview before deploying — never against the
dev server, whose injected toolbar corrupts the scores:

```bash
npm run build && npx astro preview --port 4399
```

### Measured results

All five pages, mobile, against a production build:

| Category | Current site | This redesign |
|---|---|---|
| Accessibility | 87 | 100 |
| Agentic Browsing | 50 | 100 |
| Best Practices | 96 | 100 |
| SEO | 100 | 100 |
| CLS | 0.00 | 0.00 |

The current site is not slow, and this project makes no speed claim. Its failures
are accessibility and machine readability: `color-contrast`, `heading-order`,
`link-name`, `listitem`, `image-aspect-ratio`, and a malformed accessibility tree.
All six pass here.

## Design system

Two tokens exist where one would normally do, in both cases because a single value
cannot satisfy WCAG across contexts:

- **Accent is surface-bound.** `--color-accent` `#A16207` on light surfaces
  (4.71:1); `--color-accent-dark` `#F59E0B` on dark (8.14:1). Amber-700 on the dark
  surface is 3.55:1 and fails body text.
- **Border is role-bound.** `--color-border` `#D6D3D1` for decorative dividers,
  exempt under WCAG 1.4.11. `--color-border-strong` `#78716C` (4.59:1) for form
  controls, which are UI component boundaries and require 3:1.

`scripts/contrast-check.py` enforces both and exits non-zero on violation.

## Content

All copy lives in `src/data/`. Structure is fixed; copy is swappable without
touching markup. Service and case-study entries are Zod-validated content
collections, so a malformed entry fails the build rather than rendering blank.

The three dashed consultant slots on `/about` are intentionally empty. The client's
site claims a "platform of food professionals" and names none — the slots make that
gap visible rather than papering over it. Do not fill them with invented people.

## Image credits

See `public/images/CREDITS.md`. All images are Pexels-licensed for commercial and
portfolio use.

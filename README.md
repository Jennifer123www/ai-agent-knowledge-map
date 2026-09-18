# AI Agent Knowledge Map

A static Chinese learning site for the AI Agent knowledge map. It presents one shared topic system through two complementary paths: a beginner guide for concepts and an interview guide for answer practice.

## Structure

```text
site/
  index.html                 # Editorial home page
  learn/
    index.html               # Beginner overview
    concepts.html            # Concept diagrams and "大话" explanations
  interview/
    index.html               # Interview topic map
    questions.html           # Interview question drill-down
  assets/js/
    site-search.js           # Shared cross-site search
scripts/
  check-site.mjs             # Link and syntax validation
```

The `site/` directory is the publish root for GitHub Pages, Netlify, Vercel, or any ordinary static-file host. The paths use stable English lowercase URLs, while the pages and learning material remain in Chinese.

## Local Preview

```sh
npm run serve
```

Open [http://127.0.0.1:4173/](http://127.0.0.1:4173/).

## Validation

```sh
npm run check
```

The check confirms expected pages, local HTML links, inline script syntax, and the shared search script.

## Project Metadata

- Version: `0.2.1`
- Stage: GitHub repository linked and initial `main` history pushed
- Git status before this metadata update: clean; `main` tracked `origin/main` at `c9c366f`
- Updated: `2026-09-19 00:05 CST`

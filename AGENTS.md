# AGENTS.md

## Project

This repository is `sauhard2701/CS-Notes`, branch `CS-Notes-english`.

Goal: maintain an English, locally hostable study website for CS/interview notes using Docsify.

## Current Status

The repository has already been translated from Chinese to English.

Completed:
- Chinese filenames translated.
- Markdown body content translated.
- Headings translated.
- Code comments translated.
- Docsify site created.
- Internal Docsify navigation fixed.
- Sidebar validation passed.
- Broken internal links: 0.
- Relative `notes/*.md` links that should be `/notes/...`: 0.
- `node_modules` references in `index.html`: 0.
- Malformed one-line Markdown files: 0.

Current issue:
Some pages have top contents/TOC links that should scroll to headings in the same page, but some anchors do not work. The next task is to validate and fix same-file in-page anchors across the repo.

## Important Rules

Do not translate content again.
Do not rename files unless explicitly asked.
Do not rewrite study explanations.
Do not change external links unless they are broken.
Do not modify code syntax.
Preserve Markdown structure, links, images, code fences, tables, and lists.

## Website

The site uses Docsify.

Important files:
- `index.html`
- `_sidebar.md`
- `_navbar.md`
- `_coverpage.md`
- `README.md`
- `docs/local-hosting.md`
- `docs/github-pages.md`
- `notes/`

Use root-based Docsify links:
- Good: `/notes/java-basics.md`
- Bad: `java-basics.md` inside `notes/*.md`

Docsify routes look like:
- `http://localhost:3000/#/notes/java-basics.md`

## Validation Commands

Run these before considering work complete:

```bash
python3 scripts/validate-docsify-links.py
python3 scripts/validate-docsify-anchors.py
npm run docs:serve
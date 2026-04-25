# Migration Plan

Generated on 2026-04-26 from the current repository file tree using `git ls-files --cached --others --exclude-standard`, excluding vendor/media paths listed below. The generated reports intentionally do not translate source content.

## Excluded Paths

- `docs/_style/prism-master/**`
- `docs/_media/**`

## Generated Files

- `translation-file-map.csv`: file inventory with Chinese filename, heading, Markdown body, Markdown/HTML link, code-comment, and asset-name flags.
- `internal-link-map.csv`: internal Markdown/HTML link inventory normalized to repository paths for scanned source files.
- `migration-plan.md`: this summary and follow-up checklist.

## Inventory Summary

| Metric | Count |
| --- | ---: |
| Files inventoried | 809 |
| Files excluded | 1748 |
| Markdown files | 182 |
| Asset/media files | 623 |
| Files needing translation review | 181 |
| Files with Chinese filenames | 0 |
| Assets with Chinese names | 0 |
| Files with Chinese headings | 173 |
| Chinese headings found | 1671 |
| Files with Chinese Markdown body content | 175 |
| Chinese Markdown body lines found | 5987 |
| Files with Chinese Markdown/HTML links | 113 |
| Chinese Markdown/HTML links found | 1523 |
| Files with Chinese code comments | 57 |
| Chinese code comments found | 244 |
| Internal links mapped | 1472 |
| Internal links to excluded targets | 0 |
| Internal links needing path update | 0 |
| Internal links needing content/anchor update | 1214 |
| Anchor-only internal links | 1268 |
| Broken internal file/directory links | 0 |

## Repository Shape

| Area | Files |
| --- | ---: |
| `.` | 3 |
| `assets` | 10 |
| `docs` | 5 |
| `notes` | 790 |
| `scripts` | 1 |

## Detection Rules

- Chinese detection uses CJK unified ideograph ranges and checks URL-decoded, HTML-decoded, and `_uXXXX` decoded text where relevant.
- Chinese filenames are literal or decoded basenames containing Chinese characters.
- Chinese asset names are asset/media basenames containing Chinese characters after literal or decoded checks.
- Chinese headings are Markdown ATX headings outside fenced code blocks.
- Chinese Markdown body content is non-heading Markdown text outside fenced code blocks.
- Chinese code comments are detected in Markdown fenced code blocks and code-like files using common comment syntaxes.
- Internal links include Markdown inline/reference/image links and HTML `href`/`src` attributes from scanned Markdown and HTML files.
- Target existence is checked against the actual repository tree, including excluded folders, so links into excluded media/vendor paths are not treated as broken.
- Internal GitHub `CyC2018/CS-Notes` blob/raw URLs are normalized back to repository paths; true external URLs, including protocol-relative `//...` URLs, are not listed.

## Current Migration State

- Filename migration appears complete if `Files with Chinese filenames` and `Assets with Chinese names` are zero.
- Path-level link migration appears complete if `Internal links needing path update` and `Broken internal file/directory links` are zero.
- Remaining work is primarily content translation: headings, Markdown body text, visible link text, anchors, and code comments.

## Suggested Next Steps

1. Translate headings in small batches and regenerate heading anchors.
2. Update anchor-only and same-file TOC links after heading translation.
3. Translate Markdown body content while preserving code examples and technical terms.
4. Translate code comments only after confirming examples still make sense.
5. Regenerate these reports after each batch and monitor broken links.

## Review Hotspots

The files with the most remaining Chinese text surfaces are:
- `notes/Linux.md` (395 heading/body/comment hits)
- `notes/HTTP.md` (383 heading/body/comment hits)
- `notes/java-concurrency.md` (316 heading/body/comment hits)
- `notes/jvm.md` (294 heading/body/comment hits)
- `notes/java-basics.md` (272 heading/body/comment hits)
- `notes/sql-syntax.md` (264 heading/body/comment hits)
- `notes/SQL.md` (262 heading/body/comment hits)
- `notes/database-system-principles.md` (232 heading/body/comment hits)
- `notes/design-patterns.md` (214 heading/body/comment hits)
- `notes/leetcode-solutions-dynamic-programming.md` (214 heading/body/comment hits)
- `notes/MySQL.md` (200 heading/body/comment hits)
- `notes/Redis.md` (200 heading/body/comment hits)
- `notes/java-collections.md` (181 heading/body/comment hits)
- `notes/Java IO.md` (170 heading/body/comment hits)
- `notes/distributed-systems.md` (170 heading/body/comment hits)
- `notes/operating-systems-process-management.md` (157 heading/body/comment hits)
- `notes/regular-expressions.md` (155 heading/body/comment hits)
- `notes/algorithms-symbol-tables.md` (150 heading/body/comment hits)
- `notes/leetcode-solutions-trees.md` (132 heading/body/comment hits)
- `notes/computer-networking-network-layer.md` (121 heading/body/comment hits)
- `notes/leetcode-solutions-search.md` (120 heading/body/comment hits)
- `notes/object-oriented-programming.md` (111 heading/body/comment hits)
- `notes/leetcode-solutions-math.md` (102 heading/body/comment hits)
- `notes/caching.md` (97 heading/body/comment hits)
- `notes/clustering.md` (96 heading/body/comment hits)

Broken internal file/directory links sample:
- None found.

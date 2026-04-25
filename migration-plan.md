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
| Files needing translation review | 40 |
| Files with Chinese filenames | 0 |
| Assets with Chinese names | 0 |
| Files with Chinese headings | 0 |
| Chinese headings found | 0 |
| Files with Chinese Markdown body content | 38 |
| Chinese Markdown body lines found | 3780 |
| Files with Chinese Markdown/HTML links | 39 |
| Chinese Markdown/HTML links found | 893 |
| Files with Chinese code comments | 18 |
| Chinese code comments found | 127 |
| Internal links mapped | 1461 |
| Internal links to excluded targets | 0 |
| Internal links needing path update | 0 |
| Internal links needing content/anchor update | 693 |
| Anchor-only internal links | 1253 |
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
- `notes/Linux.md` (333 heading/body/comment hits)
- `notes/java-concurrency.md` (261 heading/body/comment hits)
- `notes/java-basics.md` (245 heading/body/comment hits)
- `notes/SQL.md` (232 heading/body/comment hits)
- `notes/sql-syntax.md` (232 heading/body/comment hits)
- `notes/jvm.md` (230 heading/body/comment hits)
- `notes/database-system-principles.md` (185 heading/body/comment hits)
- `notes/leetcode-solutions-dynamic-programming.md` (174 heading/body/comment hits)
- `notes/Redis.md` (162 heading/body/comment hits)
- `notes/MySQL.md` (155 heading/body/comment hits)
- `notes/java-collections.md` (147 heading/body/comment hits)
- `notes/operating-systems-process-management.md` (133 heading/body/comment hits)
- `notes/regular-expressions.md` (132 heading/body/comment hits)
- `notes/distributed-systems.md` (126 heading/body/comment hits)
- `notes/algorithms-symbol-tables.md` (121 heading/body/comment hits)
- `notes/leetcode-solutions-trees.md` (97 heading/body/comment hits)
- `notes/leetcode-solutions-search.md` (96 heading/body/comment hits)
- `notes/object-oriented-programming.md` (86 heading/body/comment hits)
- `notes/leetcode-solutions-math.md` (77 heading/body/comment hits)
- `notes/leetcode-solutions-bit-manipulation.md` (74 heading/body/comment hits)
- `notes/operating-systems-deadlocks.md` (64 heading/body/comment hits)
- `notes/algorithms-sorting.md` (62 heading/body/comment hits)
- `notes/sql-exercises.md` (57 heading/body/comment hits)
- `notes/operating-systems-overview.md` (51 heading/body/comment hits)
- `notes/leetcode-solutions-binary-search.md` (49 heading/body/comment hits)

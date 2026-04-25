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
| Files needing translation review | 7 |
| Files with Chinese filenames | 0 |
| Assets with Chinese names | 0 |
| Files with Chinese headings | 0 |
| Chinese headings found | 0 |
| Files with Chinese Markdown body content | 0 |
| Chinese Markdown body lines found | 0 |
| Files with Chinese Markdown/HTML links | 7 |
| Chinese Markdown/HTML links found | 11 |
| Files with Chinese code comments | 0 |
| Chinese code comments found | 0 |
| Internal links mapped | 1461 |
| Internal links to excluded targets | 0 |
| Internal links needing path update | 0 |
| Internal links needing content/anchor update | 0 |
| Anchor-only internal links | 1260 |
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

- Filename migration appears complete: `Files with Chinese filenames` and `Assets with Chinese names` are zero.
- Path-level link migration appears complete: `Internal links needing path update` and `Broken internal file/directory links` are zero.
- No remaining Chinese headings, Markdown body lines, or code comments were detected in inventoried files.

## Suggested Next Steps

1. Review any remaining Chinese detections and decide whether they are intentional external references or translatable content.
2. Translate remaining source content in small batches while preserving links, URLs, anchors, and code syntax.
3. Regenerate these reports after each batch and monitor broken links.

## Review Hotspots

No Chinese heading, body, or code-comment hotspots remain in inventoried files.

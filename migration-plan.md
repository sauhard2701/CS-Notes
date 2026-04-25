# Migration Plan

Generated on 2026-04-25 from tracked files reported by `git ls-files`. The generated reports intentionally do not translate any source content yet; translation and rename targets are left blank for human review.

## Generated Files

- `translation-file-map.csv`: complete tracked-file inventory with Chinese filename, heading, Markdown/HTML link, code-comment, and asset-name flags.
- `internal-link-map.csv`: internal Markdown and Markdown-embedded HTML link inventory, including GitHub `CyC2018/CS-Notes/blob/master/...` links normalized back to repository paths.
- `migration-plan.md`: this summary and staged migration checklist.

## Inventory Summary

| Metric | Count |
| --- | ---: |
| Tracked files inventoried | 2555 |
| Markdown files | 183 |
| Asset/media files | 637 |
| Files needing translation or rename review | 202 |
| Files with Chinese filenames | 185 |
| Assets with Chinese names | 18 |
| Files with Chinese headings | 173 |
| Chinese headings found | 1671 |
| Files with Chinese Markdown/HTML links | 115 |
| Chinese Markdown/HTML links found | 1525 |
| Files with Chinese code comments | 58 |
| Chinese code comments found | 245 |
| Internal links mapped | 1472 |
| Internal links needing update if renamed | 1215 |
| Internal links to missing targets | 0 |

## Repository Shape

| Area | Tracked files |
| --- | ---: |
| `.` | 2 |
| `assets` | 10 |
| `docs` | 1753 |
| `notes` | 790 |

## Detection Rules

- Chinese detection uses CJK unified ideograph ranges and also checks URL-decoded, HTML-decoded, and `_uXXXX` decoded path/target forms.
- Chinese filenames are any tracked basename whose literal or decoded form contains Chinese characters.
- Chinese asset names are asset/media basenames with literal or decoded Chinese characters, including image names such as `_uXXXX...gif`.
- Chinese headings are Markdown ATX headings outside fenced code blocks.
- Chinese Markdown/HTML links are Markdown inline links, Markdown images, reference definitions, and Markdown-embedded `href`/`src` attributes whose text/alt or target contains Chinese after decoding.
- Chinese code comments are detected inside Markdown fenced code blocks and code-like text files using common comment syntaxes (`//`, `/* */`, `<!-- -->`, `#`, `--`, `%`, `;`, `'`, `REM`).
- Internal link normalization prefers an existing repo-root path, then falls back to a source-relative path; this covers both `/notes/...` style and `notes/...` style links used from nested Markdown files.

## Migration Checklist

1. Freeze content changes while path and link migrations are in flight.
2. Fill `proposed_english_path` in `translation-file-map.csv` for rows where `needs_filename_migration` is `yes`.
3. Choose a stable slug policy before renaming: lowercase ASCII, hyphen-separated words, preserve numeric problem prefixes, and avoid case-only renames.
4. Rename Markdown files and assets in small batches with `git mv` so history is preserved.
5. Use `internal-link-map.csv` to update every row where `needs_update_if_renamed` is `yes`, including GitHub blob URLs that point back into this repository.
6. Translate headings after filename/link migration, then regenerate anchor links because translated headings will change heading slugs.
7. Translate Chinese code comments only after examples still compile or remain semantically equivalent.
8. Rebuild or serve the docs site and run a link checker against generated pages.
9. Regenerate these three reports and compare counts; remaining Chinese surfaces should be intentional or queued for a later pass.

## Review Hotspots

The first Chinese filename rows are:
- `assets/今日头条招聘海报.png`
- `assets/公众号二维码-2.png`
- `assets/公众号海报7.png`
- `assets/内推.md`
- `docs/_media/公众号.jpg`
- `notes/10.1 斐波那契数列.md`
- `notes/10.2 矩形覆盖.md`
- `notes/10.3 跳台阶.md`
- `notes/10.4 变态跳台阶.md`
- `notes/11. 旋转数组的最小数字.md`
- `notes/12. 矩阵中的路径.md`
- `notes/13. 机器人的运动范围.md`
- `notes/14. 剪绳子.md`
- `notes/15. 二进制中 1 的个数.md`
- `notes/16. 数值的整数次方.md`
- `notes/17. 打印从 1 到最大的 n 位数.md`
- `notes/18.1 在 O(1) 时间内删除链表节点.md`
- `notes/18.2 删除链表中重复的结点.md`
- `notes/19. 正则表达式匹配.md`
- `notes/20. 表示数值的字符串.md`
- `notes/21. 调整数组顺序使奇数位于偶数前面.md`
- `notes/22. 链表中倒数第 K 个结点.md`
- `notes/23. 链表中环的入口结点.md`
- `notes/24. 反转链表.md`
- `notes/25. 合并两个排序的链表.md`

The first Chinese asset-name rows are:
- `assets/今日头条招聘海报.png`
- `assets/公众号二维码-2.png`
- `assets/公众号海报7.png`
- `docs/_media/公众号.jpg`
- `notes/pics/_u4E0B_u8F7D.png`
- `notes/pics/_u4E8C_u53C9_u6811_u7684_u4E0B_.gif`
- `notes/pics/_u4E8C_u53C9_u6811_u7684_u4E0B_1548504426508.gif`
- `notes/pics/_u4E8C_u7EF4_u6570_u7EC4_u4E2D_.gif`
- `notes/pics/_u4ECE_u5C3E_u5230_u5934_u6253_1548293972480.gif`
- `notes/pics/_u4ECE_u5C3E_u5230_u5934_u6253_1548295232667.gif`
- `notes/pics/_u4ECE_u5C3E_u5230_u5934_u6253_1548296249372.gif`
- `notes/pics/_u4ECE_u5C3E_u5230_u5934_u6253_1548503461113.gif`
- `notes/pics/_u6590_u6CE2_u90A3_u5951_u6570_u5217.gif`
- `notes/pics/_u66FF_u6362_u7A7A_u683C.gif`
- `notes/pics/_u7528_u4E24_u4E2A_u6808_u5B9E_.gif`
- `notes/pics/_u91CD_u5EFA_u4E8C_u53C9_u6811-1.gif`
- `notes/pics/_u91CD_u5EFA_u4E8C_u53C9_u6811-21548502782193.gif`
- `notes/pics/公众号海报4.png`

Internal targets currently missing or unresolved most often:
- None found.

## Notes Before Translation

- Do not translate content directly in this pass; use the CSV maps to decide scope and ordering first.
- Preserve existing numeric prefixes for algorithm/problem notes unless the site navigation is redesigned at the same time.
- The vendored Prism tree is included in the inventory because it is tracked; consider excluding or replacing it separately if it should not be part of translation work.

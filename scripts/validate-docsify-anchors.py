#!/usr/bin/env python3
"""Validate Docsify/GitHub-style same-file Markdown anchors."""

from __future__ import annotations

import html
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PREFIXES = (
    "docs/_style/prism-master/",
    "docs/_media/",
    "node_modules/",
    "reports/",
)

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
INLINE_MD_LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
HTML_HREF_RE = re.compile(r"""(?i)\bhref\s*=\s*(["'])(.*?)\1""")


def repo_path(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        rel = repo_path(path)
        if any(rel.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
            continue
        files.append(path)
    return sorted(files, key=repo_path)


def strip_markdown(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\\", "")
    return html.unescape(text)


def slug_base(heading_text: str) -> str:
    text = strip_markdown(heading_text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = text.strip()
    text = re.sub(r"\s", "-", text)
    return text


def heading_slug_map(headings: list[tuple[int, str]]) -> dict[str, list[tuple[int, str]]]:
    seen: Counter[str] = Counter()
    result: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for line_no, text in headings:
        base = slug_base(text)
        slug = base if seen[base] == 0 else f"{base}-{seen[base]}"
        seen[base] += 1
        result[slug].append((line_no, text))
    return dict(result)


def iter_content_lines(path: Path):
    in_fence = False
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            yield line_no, line, False
            in_fence = not in_fence
            continue
        yield line_no, line, not in_fence


def find_headings(path: Path) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    for line_no, line, is_content in iter_content_lines(path):
        if not is_content:
            continue
        match = HEADING_RE.match(line)
        if match:
            headings.append((line_no, match.group(2).strip()))
    return headings


def normalized_anchor(raw: str) -> str:
    anchor = raw[1:] if raw.startswith("#") else raw
    return unquote(anchor).strip()


def same_file_anchor_links(path: Path) -> list[tuple[int, str, str]]:
    links: list[tuple[int, str, str]] = []
    current_file_names = {path.name, f"/{repo_path(path)}", repo_path(path)}
    for line_no, line, is_content in iter_content_lines(path):
        if not is_content:
            continue
        for match in INLINE_MD_LINK_RE.finditer(line):
            if match.group(1):
                continue
            raw = match.group(3).strip()
            target_no_query = raw.split("?", 1)[0]
            if target_no_query == "#":
                continue
            if target_no_query.startswith("#"):
                links.append((line_no, match.group(2), normalized_anchor(target_no_query)))
                continue
            if "#" in target_no_query:
                file_part, anchor = target_no_query.split("#", 1)
                if file_part in current_file_names:
                    links.append((line_no, match.group(2), normalized_anchor(anchor)))
        for match in HTML_HREF_RE.finditer(line):
            raw = match.group(2).strip()
            if raw == "#":
                continue
            if raw.startswith("#"):
                links.append((line_no, "", normalized_anchor(raw)))
    return links


def inline_heading_issues(path: Path) -> list[tuple[int, str]]:
    issues: list[tuple[int, str]] = []
    for line_no, line, is_content in iter_content_lines(path):
        if not is_content:
            continue
        stripped = line.strip()
        starts_heading = bool(HEADING_RE.match(line))
        starts_list = bool(re.match(r"^\s{0,3}(?:[-*+]|\d+\.)\s+\S", line))
        if not starts_heading and re.match(r"^\s+#{1,6}\s+\S", line):
            issues.append((line_no, line.strip()))
        if not starts_heading and re.search(r"\S\s+#{1,6}\s+\S", line):
            issues.append((line_no, line.strip()))
        if starts_heading and re.search(r"^#{1,6}\s+.+\s#{1,6}\s+\S", line):
            issues.append((line_no, line.strip()))
        if not starts_list and re.search(r"\S\s{2,}[-*+]\s+\S", line):
            issues.append((line_no, line.strip()))
        if not starts_list and re.search(r"\S\s{2,}\d+\.\s+\S", line):
            issues.append((line_no, line.strip()))
        if ("```" in stripped or "~~~" in stripped) and not (
            stripped.startswith("```") or stripped.startswith("~~~")
        ):
            issues.append((line_no, line.strip()))
    return issues


def main() -> int:
    files = markdown_files()
    anchors_checked = 0
    broken: list[tuple[str, int, str]] = []
    inline_issues: list[tuple[str, int, str]] = []
    duplicate_groups: list[tuple[str, str, list[int]]] = []

    for path in files:
        rel = repo_path(path)
        headings = find_headings(path)
        slug_map = heading_slug_map(headings)
        valid_slugs = set(slug_map)

        for line_no, _text, anchor in same_file_anchor_links(path):
            anchors_checked += 1
            if anchor not in valid_slugs:
                broken.append((rel, line_no, anchor))

        inline_issues.extend((rel, line_no, text) for line_no, text in inline_heading_issues(path))

        for slug, occurrences in slug_map.items():
            if len(occurrences) > 1:
                duplicate_groups.append((rel, slug, [line for line, _ in occurrences]))

        base_counts: defaultdict[str, list[int]] = defaultdict(list)
        for line_no, heading in headings:
            base_counts[slug_base(heading)].append(line_no)
        for base, lines in base_counts.items():
            if len(lines) > 1:
                duplicate_groups.append((rel, base, lines))

    print(f"files scanned: {len(files)}")
    print(f"same-file anchors checked: {anchors_checked}")
    print(f"broken same-file anchors: {len(broken)}")
    for rel, line_no, anchor in broken:
        print(f"  {rel}:{line_no} -> #{anchor}")
    print(f"inline/compressed heading issues: {len(inline_issues)}")
    for rel, line_no, text in inline_issues:
        print(f"  {rel}:{line_no}: {text}")
    print(f"duplicate heading groups: {len(duplicate_groups)}")
    for rel, slug, lines in duplicate_groups:
        joined = ", ".join(str(line) for line in lines)
        print(f"  {rel}: #{slug} at lines {joined}")

    return 1 if broken or inline_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())

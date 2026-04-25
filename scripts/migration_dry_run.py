#!/usr/bin/env python3
"""Dry-run and apply planned filename migrations plus internal link rewrites."""

from __future__ import annotations

import argparse
import csv
import html
import posixpath
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, unquote, urlparse


TOP_LEVEL_DIRS = {"assets", "docs", "notes"}


@dataclass(frozen=True)
class RenameEntry:
    old_path: str
    new_path: str
    is_asset: bool


@dataclass(frozen=True)
class LinkRewrite:
    source_before: str
    source_after: str
    line: int
    raw_target: str
    new_target: str
    normalized_target: str
    target_after: str
    source_kind: str
    syntax: str


@dataclass(frozen=True)
class UnresolvedCase:
    kind: str
    detail: str


def repo_default() -> Path:
    return Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def yes(value: str) -> bool:
    return value.strip().lower() == "yes"


def shell_quote(path: str) -> str:
    return shlex.quote(path)


def quote_path(path: str) -> str:
    return quote(path, safe="/.-_")


def decoded(value: str) -> str:
    return html.unescape(unquote(value))


def split_target(raw_target: str) -> tuple[str, str, str]:
    """Return path/url part, query suffix, and exact anchor suffix."""
    if raw_target.startswith("#"):
        return "", "", raw_target

    before_anchor, sep, anchor = raw_target.partition("#")
    anchor_suffix = f"{sep}{anchor}" if sep else ""

    before_query, qsep, query = before_anchor.partition("?")
    query_suffix = f"{qsep}{query}" if qsep else ""
    return before_query, query_suffix, anchor_suffix


def resolve_repo_path(source_after: str, target: str) -> str | None:
    raw_path, _, _ = split_target(target)
    if not raw_path:
        return source_after

    parsed = urlparse(raw_path)
    if parsed.scheme or parsed.netloc:
        return None

    decoded_path = decoded(raw_path)
    if decoded_path.startswith("/"):
        return posixpath.normpath(decoded_path.lstrip("/"))
    return posixpath.normpath(posixpath.join(posixpath.dirname(source_after), decoded_path))


def build_relative_target(source_after: str, target_after: str, raw_target: str) -> str:
    raw_path, query_suffix, anchor_suffix = split_target(raw_target)
    decoded_path = decoded(raw_path)

    if decoded_path.startswith("/"):
        new_path = "/" + target_after
    elif decoded_path.startswith("./"):
        rel = posixpath.relpath(target_after, posixpath.dirname(source_after) or ".")
        new_path = rel if rel.startswith("../") else f"./{rel}"
    elif decoded_path.split("/", 1)[0] in TOP_LEVEL_DIRS:
        # Preserve repo-root style only when it still resolves from the source.
        new_path = target_after
        if resolve_repo_path(source_after, new_path) != target_after:
            new_path = posixpath.relpath(target_after, posixpath.dirname(source_after) or ".")
    else:
        new_path = posixpath.relpath(target_after, posixpath.dirname(source_after) or ".")

    return quote_path(new_path) + query_suffix + anchor_suffix


def build_new_target(row: dict[str, str], source_after: str, target_after: str) -> str | None:
    raw_target = row["raw_target"]
    if row["source_kind"] == "github_repo_url":
        # Internal GitHub blob/raw URLs should become repo-relative Markdown links.
        return build_relative_target(source_after, target_after, raw_target)
    if row["source_kind"] == "relative":
        return build_relative_target(source_after, target_after, raw_target)
    return None


def load_renames(rows: Iterable[dict[str, str]]) -> tuple[list[RenameEntry], list[UnresolvedCase]]:
    entries: list[RenameEntry] = []
    unresolved: list[UnresolvedCase] = []
    proposed_counts: dict[str, int] = {}

    for row in rows:
        if not yes(row["needs_filename_migration"]):
            continue

        old_path = row["path"]
        new_path = row["proposed_english_path"].strip()
        if not new_path:
            unresolved.append(UnresolvedCase("missing proposed path", old_path))
            continue

        entries.append(RenameEntry(old_path, new_path, yes(row["is_asset"])))
        proposed_counts[new_path] = proposed_counts.get(new_path, 0) + 1

    for proposed_path, count in proposed_counts.items():
        if count > 1:
            unresolved.append(UnresolvedCase("duplicate proposed path", f"{proposed_path} ({count})"))

    return entries, unresolved


def plan_link_rewrites(
    link_rows: Iterable[dict[str, str]],
    rename_map: dict[str, str],
) -> tuple[list[LinkRewrite], int, list[UnresolvedCase]]:
    rewrites: list[LinkRewrite] = []
    unresolved: list[UnresolvedCase] = []
    anchor_only_skipped = 0

    for row in link_rows:
        if row["target_kind"] == "anchor":
            anchor_only_skipped += 1
            continue

        old_target = row["normalized_target"]
        if old_target not in rename_map:
            continue

        source_before = row["source_file"]
        source_after = rename_map.get(source_before, source_before)
        target_after = rename_map[old_target]
        new_target = build_new_target(row, source_after, target_after)
        if not new_target:
            unresolved.append(
                UnresolvedCase(
                    "unsupported link target",
                    f"{source_before}:{row['line']} {row['raw_target']}",
                )
            )
            continue

        rewrites.append(
            LinkRewrite(
                source_before=source_before,
                source_after=source_after,
                line=int(row["line"]),
                raw_target=row["raw_target"],
                new_target=new_target,
                normalized_target=old_target,
                target_after=target_after,
                source_kind=row["source_kind"],
                syntax=row["syntax"],
            )
        )

    return rewrites, anchor_only_skipped, unresolved


def post_plan_validation(
    rewrites: list[LinkRewrite],
    future_paths: set[str],
) -> list[UnresolvedCase]:
    unresolved: list[UnresolvedCase] = []

    for rewrite in rewrites:
        if rewrite.source_kind not in {"relative", "github_repo_url"}:
            continue

        _, original_query, original_anchor = split_target(rewrite.raw_target)
        _, new_query, new_anchor = split_target(rewrite.new_target)
        if original_query != new_query:
            unresolved.append(
                UnresolvedCase(
                    "query string changed",
                    f"{rewrite.source_before}:{rewrite.line} {original_query} => {new_query}",
                )
            )
        if original_anchor != new_anchor:
            unresolved.append(
                UnresolvedCase(
                    "anchor changed",
                    f"{rewrite.source_before}:{rewrite.line} {original_anchor} => {new_anchor}",
                )
            )

        resolved = resolve_repo_path(rewrite.source_after, rewrite.new_target)
        if resolved is None:
            unresolved.append(
                UnresolvedCase(
                    "new target is not relative",
                    f"{rewrite.source_before}:{rewrite.line} {rewrite.new_target}",
                )
            )
            continue
        if resolved != rewrite.target_after:
            unresolved.append(
                UnresolvedCase(
                    "new target resolves incorrectly",
                    f"{rewrite.source_before}:{rewrite.line} {rewrite.new_target} => {resolved}, expected {rewrite.target_after}",
                )
            )
            continue
        if resolved not in future_paths:
            unresolved.append(
                UnresolvedCase(
                    "new target missing after migration",
                    f"{rewrite.source_before}:{rewrite.line} {rewrite.new_target} => {resolved}",
                )
            )

    return unresolved


def preflight(
    repo_root: Path,
    renames: list[RenameEntry],
    rewrites: list[LinkRewrite],
    all_known_paths: set[str],
) -> list[UnresolvedCase]:
    unresolved: list[UnresolvedCase] = []
    current_paths = {entry.old_path for entry in renames}
    future_paths = (all_known_paths - current_paths) | {entry.new_path for entry in renames}

    for entry in renames:
        old_abs = repo_root / entry.old_path
        new_abs = repo_root / entry.new_path
        if not old_abs.exists():
            unresolved.append(UnresolvedCase("missing source file", entry.old_path))
        if new_abs.exists() and entry.new_path not in current_paths:
            unresolved.append(UnresolvedCase("destination already exists", entry.new_path))

    for entry in renames:
        if entry.old_path in future_paths and entry.old_path != entry.new_path:
            unresolved.append(UnresolvedCase("rename cycle or collision", entry.old_path))

    for rewrite in rewrites:
        source_abs = repo_root / rewrite.source_before
        if not source_abs.exists():
            unresolved.append(UnresolvedCase("missing link source", rewrite.source_before))
            continue
        lines = source_abs.read_text(encoding="utf-8").splitlines(keepends=True)
        if rewrite.line < 1 or rewrite.line > len(lines):
            unresolved.append(UnresolvedCase("line out of range", f"{rewrite.source_before}:{rewrite.line}"))
            continue
        occurrence_count = lines[rewrite.line - 1].count(rewrite.raw_target)
        if occurrence_count != 1:
            unresolved.append(
                UnresolvedCase(
                    "raw target occurrence count",
                    f"{rewrite.source_before}:{rewrite.line} count={occurrence_count} {rewrite.raw_target}",
                )
            )

    unresolved.extend(post_plan_validation(rewrites, future_paths))
    return unresolved


def apply_renames(repo_root: Path, renames: list[RenameEntry]) -> None:
    for entry in renames:
        subprocess.run(
            ["git", "mv", "--", entry.old_path, entry.new_path],
            cwd=repo_root,
            check=True,
        )


def apply_link_rewrites(repo_root: Path, rewrites: list[LinkRewrite]) -> None:
    by_source: dict[str, list[LinkRewrite]] = {}
    for rewrite in rewrites:
        by_source.setdefault(rewrite.source_after, []).append(rewrite)

    for source_after, source_rewrites in by_source.items():
        source_abs = repo_root / source_after
        lines = source_abs.read_text(encoding="utf-8").splitlines(keepends=True)
        for rewrite in sorted(source_rewrites, key=lambda item: item.line):
            index = rewrite.line - 1
            occurrence_count = lines[index].count(rewrite.raw_target)
            if occurrence_count != 1:
                raise RuntimeError(
                    f"{rewrite.source_after}:{rewrite.line} has {occurrence_count} "
                    f"occurrences of {rewrite.raw_target!r}"
                )
            lines[index] = lines[index].replace(rewrite.raw_target, rewrite.new_target, 1)
        source_abs.write_text("".join(lines), encoding="utf-8")


def print_report(
    renames: list[RenameEntry],
    rewrites: list[LinkRewrite],
    anchor_only_skipped: int,
    unresolved: list[UnresolvedCase],
    apply: bool,
    show_all: bool,
) -> None:
    assets = [entry for entry in renames if entry.is_asset]
    content_files = [entry for entry in renames if not entry.is_asset]
    limit = None if show_all else 25

    print("migration_dry_run_summary")
    print(f"mode={'apply' if apply else 'dry-run'}")
    print(f"files_to_rename={len(renames)}")
    print(f"content_files_to_rename={len(content_files)}")
    print(f"assets_to_rename={len(assets)}")
    print(f"links_to_rewrite={len(rewrites)}")
    print(
        "github_repo_url_links_converted_to_relative="
        f"{sum(1 for rewrite in rewrites if rewrite.source_kind == 'github_repo_url')}"
    )
    print(f"links_skipped_anchor_only={anchor_only_skipped}")
    print(f"unresolved_cases={len(unresolved)}")

    print("\ngit_mv_commands:")
    shown_renames = renames if limit is None else renames[:limit]
    for entry in shown_renames:
        print(f"  git mv -- {shell_quote(entry.old_path)} {shell_quote(entry.new_path)}")
    if limit is not None and len(renames) > limit:
        print(f"  ... {len(renames) - limit} more (use --show-all)")

    print("\nlink_rewrites:")
    shown_rewrites = rewrites if limit is None else rewrites[:limit]
    for rewrite in shown_rewrites:
        print(
            "  "
            f"{rewrite.source_before}:{rewrite.line} "
            f"{rewrite.raw_target} => {rewrite.new_target}"
        )
    if limit is not None and len(rewrites) > limit:
        print(f"  ... {len(rewrites) - limit} more (use --show-all)")

    if unresolved:
        print("\nunresolved:")
        shown_unresolved = unresolved if limit is None else unresolved[:limit]
        for item in shown_unresolved:
            print(f"  {item.kind}: {item.detail}")
        if limit is not None and len(unresolved) > limit:
            print(f"  ... {len(unresolved) - limit} more (use --show-all)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dry-run or apply proposed filename migrations and internal link rewrites."
    )
    parser.add_argument("--repo-root", type=Path, default=repo_default())
    parser.add_argument("--translation-map", default="translation-file-map.csv")
    parser.add_argument("--link-map", default="internal-link-map.csv")
    parser.add_argument("--apply", action="store_true", help="Run git mv and rewrite links.")
    parser.add_argument("--show-all", action="store_true", help="Print every command and rewrite.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    translation_map = repo_root / args.translation_map
    link_map = repo_root / args.link_map

    translation_rows = read_csv(translation_map)
    link_rows = read_csv(link_map)

    renames, unresolved = load_renames(translation_rows)
    rename_map = {entry.old_path: entry.new_path for entry in renames}
    rewrites, anchor_only_skipped, link_unresolved = plan_link_rewrites(link_rows, rename_map)
    unresolved.extend(link_unresolved)
    all_known_paths = {row["path"] for row in translation_rows}
    unresolved.extend(preflight(repo_root, renames, rewrites, all_known_paths))

    print_report(renames, rewrites, anchor_only_skipped, unresolved, args.apply, args.show_all)

    if unresolved:
        print("\nNo changes applied because unresolved cases exist.", file=sys.stderr)
        return 1

    if args.apply:
        apply_renames(repo_root, renames)
        apply_link_rewrites(repo_root, rewrites)
        print("\nApplied git mv operations and link rewrites.")
    else:
        print("\nDry run only. Re-run with --apply to make changes.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Dry-Run Migration Script

The migration helper reads `translation-file-map.csv` and `internal-link-map.csv` and plans the filename migration without translating content.

## Commands

Preview the migration:

```bash
python3 scripts/migration_dry_run.py
```

Preview every generated command and link rewrite:

```bash
python3 scripts/migration_dry_run.py --show-all
```

Apply the migration:

```bash
python3 scripts/migration_dry_run.py --apply
```

## Behavior

- Generates `git mv` commands for every row where `needs_filename_migration` is `yes`.
- Rewrites Markdown and Markdown-embedded HTML links whose normalized targets point to renamed files.
- Converts internal GitHub blob/raw URLs already identified in `internal-link-map.csv` into relative links instead of preserving GitHub URLs.
- Preserves existing anchors exactly.
- Leaves headings, body text, code comments, and link text untranslated.
- Skips anchor-only links and reports their count.
- Refuses to apply changes if preflight finds unresolved cases, ambiguous link-target occurrences, or rewritten targets that do not resolve to the expected post-rename file.

After applying, regenerate the maps before starting heading or body translation.

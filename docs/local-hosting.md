# Local Hosting

This repository is primarily a Markdown knowledge base. You can preview it locally with any static file server or Markdown-capable editor.

## Static Preview

From the repository root, start a simple static server:

```sh
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/
```

## Markdown Editing

For content edits, use an editor with Markdown preview and keep links relative to the repository root or to the current Markdown file.

Before publishing changes, check the generated inventory reports:

- `translation-file-map.csv`
- `internal-link-map.csv`
- `migration-plan.md`


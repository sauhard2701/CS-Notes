# GitHub Pages

GitHub Pages can publish this repository as static documentation.

## Recommended Setup

Use the repository root as the publishing source.
The root contains the Docsify entry files:

- `index.html`
- `README.md`
- `_sidebar.md`
- `_navbar.md`
- `_coverpage.md`
- `notes/`

Do not publish from `docs/` for the current website.
This folder is now reserved for project documentation pages.

## Notes

- Keep `.nojekyll` at the repository root so files and directories that begin with underscores are not ignored by Jekyll.
- Keep generated reports out of the public navigation unless they are intentionally part of the documentation.
- Do not point published pages at removed legacy Docsify files such as `_coverpage.md`, `_404.md`, `_media/`, or `_style/prism-master/`.

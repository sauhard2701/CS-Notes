# GitHub Pages

GitHub Pages can publish this repository as static documentation.

## Recommended Setup

Use the repository root as the publishing source when the project is meant to expose the main `README.md` and `notes/` content directly.

If GitHub Pages is configured to publish from `docs/`, keep this folder focused on project documentation and avoid restoring the old Docsify website files unless a new website build is intentionally added.

## Notes

- Keep `.nojekyll` when publishing from `docs/` so files and directories that begin with underscores are not ignored by Jekyll.
- Keep generated reports out of the public navigation unless they are intentionally part of the documentation.
- Do not point published pages at removed legacy Docsify files such as `_coverpage.md`, `_404.md`, `_media/`, or `_style/prism-master/`.


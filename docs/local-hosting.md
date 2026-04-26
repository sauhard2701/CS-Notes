# Local Hosting

This repository is Markdown-first and uses Docsify for local browsing.
There is no build step, and the browser runtime assets are vendored under `site-assets/vendor/` so the website does not depend on a CDN at runtime.

## Run the Website Locally

Clone the repository:

```sh
git clone <repository-url>
cd CS-Notes
```

Install Node.js if it is not already installed.
Node.js 18 or newer is recommended.

Install the local dependencies:

```sh
npm install
```

Start the local website:

```sh
npm run docs:serve
```

Open the site in your browser:

```text
http://localhost:3000
```

After `npm install`, the `docs:serve` script runs the local Docsify server.
The page itself loads Docsify core, theme CSS, search, copy-code, image zoom, and pagination from `site-assets/vendor/`, so browsing the notes does not require CDN access when those vendored files are present.

## Optional GitHub Pages Deployment

For GitHub Pages, publish from the branch root so `index.html`, `README.md`, `_sidebar.md`, and `notes/` are served together.

Keep `.nojekyll` at the repository root so GitHub Pages serves files and folders that begin with underscores.

# Local Hosting

This repository is Markdown-first and uses Docsify for local browsing. There is no build step.

## Run the Website Locally

Clone the repository:

```sh
git clone <repository-url>
cd CS-Notes
```

Install Node.js if it is not already installed. Node.js 18 or newer is recommended.

Install the local Docsify dependencies:

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

## Optional GitHub Pages Deployment

For GitHub Pages, publish from the branch root so `index.html`, `README.md`, `_sidebar.md`, and `notes/` are served together.

Keep `.nojekyll` at the repository root so GitHub Pages serves files and folders that begin with underscores.

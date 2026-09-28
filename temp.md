# Deploying GSU-Portfolio to GitHub Pages

Target URL: **https://sacostapliego.github.io/GSU-Portfolio/**

This is a Vite + React app with hash routing (`#/courses/...`), so no SPA 404 workaround is needed.
`public/coi-serviceworker.js` is already loaded in `index.html`, so the Python terminal's
`SharedArrayBuffer` will still work on Pages even though you can't set COOP/COEP headers there.

---

## 1. Set the Vite `base` path

The site is served from `/GSU-Portfolio/`, not `/`, so Vite needs to know that.
In `vite.config.ts`:

```ts
export default defineConfig({
  base: '/GSU-Portfolio/',
  plugins: [react()],
  server: { headers: crossOriginIsolationHeaders },
  preview: { headers: crossOriginIsolationHeaders },
  worker: { format: 'es' },
})
```

Use exactly one leading slash. `'//GSU-Portfolio/'` is treated as a different host and every file fails to load.

## 2. Import images instead of using `/` paths ✅ done

Strings like `src="/image.png"` point at the site root (`sacostapliego.github.io/image.png`), which returns a 404 on
Pages. Instead, images live in `src/assets/` and are imported, so Vite adds the `base` path and hashes the filenames:

```tsx
import gsuBackground from '../assets/gsu_background.jpg'
import homeImage from '../assets/image.png'
import pythonLogo from '../assets/python-logo.svg'

<Image src={pythonLogo} ... />
bgImage={`linear-gradient(...), url('${gsuBackground}')`}
```

The favicon in `index.html` points at `/src/assets/image.png`, and Vite rewrites that during the build.

Rule going forward: **put new images in `src/assets/` and import them**. Only files that must stay at a fixed,
unprocessed URL go in `public/`, like `coi-serviceworker.js`. Reference those with a relative path (`./file`) or
`import.meta.env.BASE_URL`, never a leading `/`.

## 3. Add a GitHub Actions workflow (recommended)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

## 4. Turn on Pages in the repo

GitHub, then **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## 5. Verify locally, then push

```bash
npm run build      # must pass: tsc -b runs first, so type errors will fail the build
npm run preview    # open http://localhost:4173/GSU-Portfolio/
```

Check the background image, the Python logos, and the Python terminal's `input()`.
Then commit and push to `main`. The workflow builds and deploys automatically, and you can watch it in the **Actions** tab.

---

## Alternative: manual deploy with the `gh-pages` package

If you don't want to use Actions, do steps 1 and 2 above, then:

```bash
npm install -D gh-pages
```

Add this script to `package.json`:

```json
"deploy": "npm run build && gh-pages -d dist"
```

Run `npm run deploy`, then set **Settings → Pages → Source: Deploy from a branch → `gh-pages` / root**.

---

## Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| Blank page, 404s for `/assets/*.js` | `base` isn't set, or its casing doesn't match the repo name (`/GSU-Portfolio/`) |
| Everything 404s, requests go to `https://gsu-portfolio/...` | `base` has a double slash (`//GSU-Portfolio/`) |
| Images missing, rest of site fine | An image is referenced by a `/...` string instead of an import (step 2) |
| Python `input()` doesn't block / terminal falls back | The service worker didn't register yet. Hard-refresh once. It reloads the page on first visit to become active. |
| Old version still showing | Pages caching. Wait about a minute or hard-refresh. |

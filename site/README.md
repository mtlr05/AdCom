# Orphan natural-history table (static site)

This folder is what Vercel should publish. The live page is `index.html`, copied from `../orphan_natural_history.html`. After you edit the root HTML file, copy it here before redeploying:

```powershell
Copy-Item -Force ..\orphan_natural_history.html .\index.html
```

## Deploy with the Vercel CLI

From this directory:

```powershell
npx vercel login
npx vercel link
npx vercel deploy --prod
```

The production URL is printed when the deploy finishes. `/` serves `index.html`.

## Deploy from GitHub (recommended if CLI login fails)

1. Commit and push `site/` (and `vercel.json` at the repo root if you use the rewrite layout).
2. In [Vercel](https://vercel.com/new), import the **AdCom** GitHub repository.
3. Set **Root Directory** to `site`.
4. Framework preset: **Other** (no build command).
5. Deploy. Every push to the connected branch updates the site.

The repo-root `vercel.json` and `.vercelignore` are for CLI deploys from the repository root (only `orphan_natural_history.html` is uploaded). The `site/` layout is simpler for Git-connected projects.
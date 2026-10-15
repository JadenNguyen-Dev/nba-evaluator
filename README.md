# NBA EValuator, public website

This folder is the version of the site that goes on the internet. It is generated:
don't edit these files by hand. Edit `../site/index.html` (or its template and data),
then run `python3 make_deploy.py` here and upload the result.

## What's here

| File | What it is |
|---|---|
| `index.html` | The whole page in one file, with head tags for search engines, link previews and phones |
| `404.html` | Shown for any address on the site that doesn't exist |
| `favicon.svg` | The little icon in the browser tab |
| `robots.txt` | Tells search engines they may index the site |
| `.nojekyll` | Tells GitHub Pages to serve the files as they are |
| `logs/` | Game-by-game logs (12 files), loaded when a season is opened |
| `LICENSE` | MIT license for the code (the NBA stats themselves come from public sources) |
| `.gitignore` | Keeps computer and editor junk files out of the repository |
| `make_deploy.py` | Rebuilds everything above from `../site/index.html` |

## Security, in plain terms

- **No server, no logins, no database, no user data.** The site is a single page that
  runs entirely in the visitor's browser, so there is nothing to break into and no
  passwords or keys to protect.
- **HTTPS** is provided by GitHub Pages automatically (tick "Enforce HTTPS" in the
  Pages settings).
- **Content-Security-Policy** (in `index.html`): the browser will only run the page's
  own code, recognised by its fingerprint. Injected or third-party scripts are refused, the only network requests are to
  its own `logs/` files, and it can't submit forms anywhere. The one outside request is
  the Google Fonts stylesheet and font files.
- **Referrer policy** keeps full page addresses from leaking to other sites.
- **Disclaimer** in the footer: entertainment only, not advice, legal age, and the
  1-800-GAMBLER helpline.

Limits worth knowing: GitHub Pages doesn't let a site set its own HTTP headers, so
protections that only work as headers (for example blocking other sites from
embedding the page in a frame) aren't available there. For this kind of site that is
fine; moving to Cloudflare Pages or Netlify later would allow them.

## Publishing on GitHub Pages (free)

1. Create a **public** repository named `nba-evaluator` on GitHub.
2. Upload every file in this folder, including `.nojekyll` and the `logs` folder, to the repository's main branch.
3. In the repository: **Settings → Pages → Build and deployment → Source: Deploy from a branch**,
   branch `main`, folder `/ (root)`, Save. Tick **Enforce HTTPS**.
4. After a minute or two the site is live at `https://jadennguyen-dev.github.io/nba-evaluator/`.

If the repository gets a different name, change `BASE` in `make_deploy.py` and rebuild,
so the 404 page's links still work.

## Updating the site

Edit the source in `../site/`, run `python3 make_deploy.py`, and upload the changed
files to the repository. GitHub Pages republishes on every change.

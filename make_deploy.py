"""Build the public website from ../site/index.html (the source of truth).
Run after any change to the site:  python3 make_deploy.py
It keeps the page as one self-contained file (so it previews correctly anywhere) and
locks it down with a Content-Security-Policy that allows only this exact CSS and JS,
by fingerprint (hash), so any injected or third-party script is refused. It also adds
the head tags, disclaimer, favicon, 404 page and robots.txt a public site needs."""
import base64, hashlib, os, re, shutil
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, '..', 'site', 'index.html'), encoding='utf-8').read()

def one(pattern, text):
    m = re.findall(pattern, text, re.S)
    if len(m) != 1: raise SystemExit(f'expected exactly one match for {pattern!r}, found {len(m)}')
    return m[0]

css = one(r'<style>(.*?)</style>', src)
js = one(r'<script>(.*?)</script>', src)
fonts = one(r'(<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>)', src)
body = src.split('</style>', 1)[1].replace(f'<script>{js}</script>', '')

# Inline style="" attributes are blocked by the CSP too, so move each into the <style> block (needs an id).
def move_style(m):
    tag = m.group(0)
    i = re.search(r'\bid="([^"]+)"', tag)
    if not i: raise SystemExit(f'inline style without id, give it one: {tag[:80]}')
    global css
    css += f'\n#{i.group(1)}{{{m.group(2)}}}'
    return tag.replace(m.group(1), '')
body = re.sub(r'<[^>]*?(\s+style="([^"]*)")[^>]*>', move_style, body)
if re.search(r'\son[a-z]+="', body): raise SystemExit('inline event handler found; the CSP would block it')

css += '\na.home{color:var(--accent)}'
css += '\nfooter .disclaimer{margin-top:8px;font-size:.8rem;color:var(--muted)}'
disclaimer = ('<p class="disclaimer">For entertainment and information only, not betting or financial advice. '
              'No outcome is guaranteed. You must be of legal age to bet where you live. '
              'If gambling stops being fun, call or text 1-800-GAMBLER.</p>')
body = body.replace('</footer>', disclaimer + '</footer>', 1) if '</footer>' in body else body + disclaimer

h = lambda t: "'sha256-" + base64.b64encode(hashlib.sha256(t.encode('utf-8')).digest()).decode() + "'"
CSP = (f"default-src 'none'; script-src {h(js)}; style-src {h(css)} https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; "
       "base-uri 'none'; form-action 'none'; upgrade-insecure-requests")
# GitHub Pages serves 404.html at any missing path, so its links must be absolute.
# Change this if the repository gets a different name (or to '/' for a custom domain).
BASE = '/nba-evaluator/'
DESC = 'Free calculator for NBA player points props: model chance, edge and expected value, adjusted for the opponent defense.'

def head(title, extra='', base=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="NBA EValuator">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0f7a55">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{fonts}
<style>{css}</style>{extra}
</head>
'''

def w(name, text):
    open(os.path.join(here, name), 'w', encoding='utf-8').write(text)

for old in ('style.css', 'app.js'):
    if os.path.exists(os.path.join(here, old)): os.remove(os.path.join(here, old))
w('index.html', head('NBA EValuator: NBA points prop EV calculator') + '<body>' + body.strip() + f'\n<script>{js}</script>\n</body>\n</html>\n')
w('404.html', head('Page not found | NBA EValuator', base=BASE) + f'''<body>
<div class="wrap">
  <header><h1>NBA <span>EV</span>aluator</h1></header>
  <section><h2>Page not found</h2><p>That page doesn't exist. <a class="home" href="{BASE}">Go to the calculator</a>.</p></section>
</div>
</body>
</html>
''')
w('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="#0f7a55"/>'
  '<path d="M2 32h60M32 2v60M11 11c12 10 12 32 0 42M53 11c-12 10-12 32 0 42" fill="none" stroke="#fff" stroke-width="3"/></svg>\n')
w('robots.txt', 'User-agent: *\nAllow: /\n')
w('.nojekyll', '')
# Game logs load on demand when a season is opened; copy them next to the page.
shutil.rmtree(os.path.join(here, 'logs'), ignore_errors=True)
shutil.copytree(os.path.join(here, '..', 'site', 'logs'), os.path.join(here, 'logs'))
print('built index.html, 404.html, favicon.svg, robots.txt, logs/')

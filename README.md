# CyberShop

A working Flask online shop that teaches web concepts as you use it.
Left sidebar explains what's happening on each page, what to look for in DevTools, and which files to read.

## Run

```bash
cd cybershop
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py                  # first time only — creates DB + demo user
flask run --port 5001
```

→ http://localhost:5001  
Demo login: **demo / demo123**

## Run with HTTPS (TLS demo)

```bash
source .venv/bin/activate      # Windows: .venv\Scripts\activate
flask run --port 5001 --cert=adhoc
```

→ https://localhost:5001  
Browser shows a self-signed cert warning — click **Advanced → Proceed**. Then open DevTools → **Security** tab to inspect the certificate, TLS version, and cipher suite.

## AI Assistant (optional)

The AI widget works without a key (shows a canned offline response). For live Gemini responses:

```bash
cp .env.example .env
# add your key:  GOOGLE_API_KEY=your-key-here
# get one free:  https://aistudio.google.com/
```

## DevTools cheat-sheet

| Concept | Tab | What to look at |
|---|---|---|
| HTTP requests | **Network** | Method, status code, headers, timing |
| HTML vs DOM | **Elements** / View Source | Server HTML vs live DOM after JS runs |
| JavaScript | **Console**, **Sources** | `fetch()` calls, event listeners, `console.log` |
| Cookies & session | **Application → Cookies** | `session` cookie, `lang` cookie, HttpOnly flag |
| API calls | **Network → Fetch/XHR** | JSON requests, payloads, responses |
| TLS / HTTPS | **Security**, padlock | Certificate chain, TLS version, cipher |

### Console one-liners

```js
fetch('/api/cart').then(r => r.json()).then(console.log)

fetch('/api/cart/add', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({product_id: 1, quantity: 1})
}).then(r => r.json()).then(console.log)

fetch('/api/products').then(r => r.json()).then(console.log)

fetch('/api/ai/ask', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({question: 'What should I buy for a home lab?'})
}).then(r => r.json()).then(console.log)
```

## Project structure

```
app.py        — Flask app, all page routes
api.py        — JSON API blueprint (/api/*)
auth.py       — login/register/logout, @login_required
db.py         — SQLite helper, query logger for the inspector
i18n.py       — EN/DE translations + per-page guide content
ai.py         — Gemini wrapper + offline fallback
schema.sql    — DB schema
seed.py       — Demo products + demo user
templates/    — Jinja HTML templates
static/       — CSS + JS
```

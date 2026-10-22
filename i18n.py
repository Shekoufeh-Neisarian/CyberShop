from flask import request, g

STRINGS = {
    "nav.shop": {"en": "Shop", "de": "Shop"},
    "nav.cart": {"en": "Cart", "de": "Warenkorb"},
    "nav.account": {"en": "Account", "de": "Konto"},
    "nav.login": {"en": "Log in", "de": "Anmelden"},
    "nav.logout": {"en": "Log out", "de": "Abmelden"},
    "nav.register": {"en": "Register", "de": "Registrieren"},
    "nav.routes": {"en": "Route Map", "de": "Routenkarte"},

    "theme.light_mode": {"en": "Light Mode", "de": "Heller Modus"},
    "theme.switch_to_light": {"en": "Switch to light mode", "de": "Zum hellen Modus wechseln"},
    "theme.switch_to_dark": {"en": "Switch to dark mode", "de": "Zum dunklen Modus wechseln"},

    "home.hero": {"en": "CyberShop", "de": "CyberShop"},
    "home.tagline": {"en": "Tech gear for curious minds.", "de": "Tech-Ausrüstung für neugierige Köpfe."},
    "home.browse": {"en": "Browse Products", "de": "Produkte entdecken"},
    "home.all_products": {"en": "All Products", "de": "Alle Produkte"},
    "home.filter_all": {"en": "All", "de": "Alle"},

    "product.add_cart": {"en": "Add to Cart", "de": "In den Warenkorb"},
    "product.ask_ai": {"en": "Ask AI Assistant", "de": "KI-Assistent fragen"},
    "product.in_stock": {"en": "In stock", "de": "Auf Lager"},
    "product.price": {"en": "Price", "de": "Preis"},
    "product.category": {"en": "Category", "de": "Kategorie"},

    "cart.title": {"en": "Your Cart", "de": "Dein Warenkorb"},
    "cart.empty": {"en": "Your cart is empty.", "de": "Dein Warenkorb ist leer."},
    "cart.checkout": {"en": "Proceed to Checkout", "de": "Zur Kasse"},
    "cart.remove": {"en": "Remove", "de": "Entfernen"},
    "cart.total": {"en": "Total", "de": "Gesamt"},
    "cart.qty": {"en": "Qty", "de": "Menge"},
    "cart.continue": {"en": "Continue Shopping", "de": "Weiter einkaufen"},

    "auth.login_title": {"en": "Log In", "de": "Anmelden"},
    "auth.register_title": {"en": "Create Account", "de": "Konto erstellen"},
    "auth.username": {"en": "Username", "de": "Benutzername"},
    "auth.email": {"en": "Email", "de": "E-Mail"},
    "auth.password": {"en": "Password", "de": "Passwort"},
    "auth.login_btn": {"en": "Log In", "de": "Anmelden"},
    "auth.register_btn": {"en": "Create Account", "de": "Konto erstellen"},
    "auth.no_account": {"en": "No account?", "de": "Noch kein Konto?"},
    "auth.have_account": {"en": "Already have an account?", "de": "Bereits ein Konto?"},
    "auth.demo_hint": {"en": "Demo account: demo / demo123", "de": "Demo-Konto: demo / demo123"},

    "checkout.title": {"en": "Checkout", "de": "Kasse"},
    "checkout.place_order": {"en": "Place Order", "de": "Bestellung aufgeben"},
    "account.title": {"en": "My Account", "de": "Mein Konto"},
    "account.orders": {"en": "Order History", "de": "Bestellverlauf"},
    "account.no_orders": {"en": "No orders yet.", "de": "Noch keine Bestellungen."},
    "account.order_num": {"en": "Order", "de": "Bestellung"},
    "account.status": {"en": "Status", "de": "Status"},
    "account.date": {"en": "Date", "de": "Datum"},
    "account.total": {"en": "Total", "de": "Gesamt"},

    "flash.added_cart": {"en": "Added to cart!", "de": "In den Warenkorb gelegt!"},
    "flash.removed_cart": {"en": "Removed from cart.", "de": "Aus dem Warenkorb entfernt."},
    "flash.order_placed": {"en": "Order placed! Thank you.", "de": "Bestellung aufgegeben! Danke."},
    "flash.logged_in": {"en": "Welcome back!", "de": "Willkommen zurück!"},
    "flash.logged_out": {"en": "Logged out.", "de": "Abgemeldet."},
    "flash.registered": {"en": "Account created! You are now logged in.", "de": "Konto erstellt! Du bist jetzt angemeldet."},
    "flash.login_required": {"en": "Please log in first.", "de": "Bitte melde dich zuerst an."},
    "flash.invalid_credentials": {"en": "Invalid username or password.", "de": "Ungültiger Benutzername oder Passwort."},
    "flash.username_taken": {"en": "Username already taken.", "de": "Benutzername bereits vergeben."},
    "flash.cart_empty": {"en": "Your cart is empty.", "de": "Dein Warenkorb ist leer."},

    "ai.ask_placeholder": {"en": "e.g. What's a good gift for a developer?", "de": "z.B. Was ist ein gutes Geschenk für einen Entwickler?"},
    "ai.ask_btn": {"en": "Ask", "de": "Fragen"},
    "ai.thinking": {"en": "Thinking…", "de": "Denke nach…"},
    "ai.title": {"en": "Shopping Assistant", "de": "Einkaufsassistent"},
    "ai.subtitle": {"en": "Powered by Google Gemini", "de": "Powered by Google Gemini"},
    "ai.offline": {"en": "Offline mode — no API key set", "de": "Offline-Modus — kein API-Schlüssel gesetzt"},

    "guide.title": {"en": "Guide", "de": "Guide"},
    "guide.open": {"en": "📖 Guide", "de": "📖 Guide"},
    "guide.files": {"en": "Project files", "de": "Projektdateien"},
    "guide.devtools": {"en": "Try in DevTools", "de": "In DevTools ausprobieren"},
    "guide.open_page": {"en": "Open this page →", "de": "Diese Seite öffnen →"},

    "routes.title": {"en": "Flask Route Map", "de": "Flask-Routenkarte"},
    "routes.subtitle": {"en": "Every URL in CyberShop — how Flask maps paths to Python functions.", "de": "Alle URLs in CyberShop — wie Flask Pfade Python-Funktionen zuordnet."},

    "inspector.toggle": {"en": "🔍 Inspector", "de": "🔍 Inspektor"},
    "inspector.queries": {"en": "SQL Queries", "de": "SQL-Abfragen"},
    "inspector.session": {"en": "Session", "de": "Session"},
    "inspector.none": {"en": "none", "de": "keine"},
    "inspector.route": {"en": "Route", "de": "Route"},
    "inspector.method": {"en": "Method", "de": "Methode"},

    "footer.text": {"en": "CyberShop — a teaching demo.", "de": "CyberShop — eine Lehrdemo."},

    "general.loading": {"en": "Loading…", "de": "Lädt…"},
    "general.error": {"en": "Something went wrong.", "de": "Etwas ist schiefgelaufen."},
    "general.back": {"en": "← Back", "de": "← Zurück"},
    "general.currency": {"en": "€", "de": "€"},
}

# ── Sidebar topic definitions ──────────────────────────────────────────────────
TOPICS = [
    {
        "id": "welcome",
        "title": {"en": "Welcome", "de": "Willkommen"},
        "desc": {
            "en": "CyberShop is a working online store built with Python and Flask. Browse products, add them to your cart, log in, and place an order. This panel walks through how each part works — what happens on the server, what you can see in DevTools, and which files to look at.",
            "de": "CyberShop ist ein funktionierender Online-Shop, der mit Python und Flask gebaut wurde. Produkte durchsuchen, in den Warenkorb legen, anmelden und bestellen. Dieses Panel erklärt, wie jeder Teil funktioniert — was auf dem Server passiert, was man in DevTools sieht und welche Dateien man sich anschauen sollte.",
        },
        "devtools": {
            "en": "Open DevTools now: <kbd>F12</kbd> on Windows/Linux, <kbd>⌥⌘I</kbd> on Mac. You'll use it throughout. Explore the tabs: <b>Elements</b>, <b>Console</b>, <b>Network</b>, <b>Application</b>, <b>Sources</b>.",
            "de": "DevTools jetzt öffnen: <kbd>F12</kbd> unter Windows/Linux, <kbd>⌥⌘I</kbd> auf dem Mac. Du wirst es die ganze Zeit nutzen. Erkunde die Tabs: <b>Elements</b>, <b>Console</b>, <b>Network</b>, <b>Application</b>, <b>Sources</b>.",
        },
        "files": ["app.py", "templates/", "static/", "schema.sql"],
        "page": "/",
    },
    {
        "id": "html",
        "title": {"en": "HTML", "de": "HTML"},
        "desc": {
            "en": "Every page you see was assembled by Flask on the server as an HTML document and sent to your browser. The browser then renders it into what you see. <b>View Source</b> shows the raw HTML Flask sent; the <b>Elements</b> panel shows the live DOM after the browser parsed it.",
            "de": "Jede Seite wurde von Flask auf dem Server als HTML-Dokument zusammengestellt und an den Browser gesendet. Der Browser rendert es dann. <b>View Source</b> zeigt das rohe HTML, das Flask gesendet hat; das <b>Elements</b>-Panel zeigt das Live-DOM nach dem Parsen.",
        },
        "devtools": {
            "en": "<kbd>F12</kbd> → <b>Elements</b>. Then right-click anywhere on the page → <b>View Page Source</b>. Compare: View Source is the raw server response. Elements is the live, JavaScript-modified DOM. Right-click any element → <b>Inspect</b> to jump directly to it.",
            "de": "<kbd>F12</kbd> → <b>Elements</b>. Dann Rechtsklick auf die Seite → <b>Seitenquelltext anzeigen</b>. Vergleich: View Source ist die rohe Server-Antwort. Elements ist das lebendige, von JavaScript modifizierte DOM. Rechtsklick auf ein Element → <b>Untersuchen</b>.",
        },
        "files": ["templates/base.html", "templates/index.html", "templates/product.html"],
        "page": "/",
    },
    {
        "id": "css",
        "title": {"en": "CSS", "de": "CSS"},
        "desc": {
            "en": "One stylesheet controls all the visual styling — colors, layout, spacing, typography. It uses CSS custom properties (variables) defined at the top, so changing one value (like <code>--accent</code>) updates the color everywhere it's used.",
            "de": "Ein Stylesheet steuert das gesamte visuelle Design — Farben, Layout, Abstände, Typografie. Es verwendet CSS-Custom-Properties (Variablen) am Anfang, sodass eine Änderung (z.B. <code>--accent</code>) die Farbe überall aktualisiert.",
        },
        "devtools": {
            "en": "<kbd>F12</kbd> → <b>Elements</b> → click any element → <b>Styles</b> panel on the right. Click a color swatch to open the color picker and edit live. Try changing a <code>--accent</code> value in the <code>:root</code> block.",
            "de": "<kbd>F12</kbd> → <b>Elements</b> → Element anklicken → <b>Styles</b>-Panel rechts. Farbfeld anklicken, um den Farbwähler zu öffnen und live zu bearbeiten. Versuche, einen <code>--accent</code>-Wert im <code>:root</code>-Block zu ändern.",
        },
        "files": ["static/css/style.css"],
        "page": "/",
    },
    {
        "id": "javascript",
        "title": {"en": "JavaScript", "de": "JavaScript"},
        "desc": {
            "en": "When you click <b>Add to Cart</b>, the page doesn't reload. JavaScript calls the server API in the background using <code>fetch()</code>, gets back JSON, and updates the cart badge in the nav — all without a page load. This is how modern web apps feel fast.",
            "de": "Wenn du auf <b>In den Warenkorb</b> klickst, lädt die Seite nicht neu. JavaScript ruft die Server-API im Hintergrund mit <code>fetch()</code> auf, erhält JSON zurück und aktualisiert das Warenkorb-Badge in der Nav — alles ohne Seitenneuladen.",
        },
        "devtools": {
            "en": "<kbd>F12</kbd> → <b>Console</b>. Try: <code>fetch('/api/cart').then(r=>r.json()).then(console.log)</code> — you just called the REST API from DevTools. Also try: <b>Sources</b> → <code>static/js/main.js</code> to read the code.",
            "de": "<kbd>F12</kbd> → <b>Console</b>. Versuche: <code>fetch('/api/cart').then(r=>r.json()).then(console.log)</code> — du hast gerade die REST-API aus DevTools aufgerufen. Auch: <b>Sources</b> → <code>static/js/main.js</code>.",
        },
        "files": ["static/js/main.js", "templates/product.html (inline <script>)"],
        "page": "/product/1",
    },
    {
        "id": "http",
        "title": {"en": "HTTP & Requests", "de": "HTTP & Anfragen"},
        "desc": {
            "en": "Every page load, form submit, and API call is an HTTP request. The server responds with a <b>status code</b> (200 OK, 302 redirect, 404 not found, 401 unauthorized) and <b>headers</b> that tell the browser what to do with the response.",
            "de": "Jeder Seitenaufruf, jedes Formular-Submit und jeder API-Aufruf ist eine HTTP-Anfrage. Der Server antwortet mit einem <b>Statuscode</b> (200 OK, 302 Redirect, 404 Not Found, 401 Unauthorized) und <b>Headers</b>.",
        },
        "devtools": {
            "en": "<kbd>F12</kbd> → <b>Network</b> → reload the page. Click any request. Look at: <b>Status</b> (top), <b>Headers</b> tab (request + response headers), <b>Response</b> tab (the HTML/JSON body). Now visit <code>/does-not-exist</code> — watch the 404.",
            "de": "<kbd>F12</kbd> → <b>Network</b> → Seite neu laden. Klicke auf eine Anfrage. Sieh: <b>Status</b> (oben), <b>Headers</b>-Tab (Anfrage- + Antwort-Header), <b>Response</b>-Tab (HTML/JSON-Body). Besuche <code>/does-not-exist</code> — sieh die 404.",
        },
        "files": ["app.py (all @app.route() functions)"],
        "page": "/",
    },
    {
        "id": "flask",
        "title": {"en": "Flask & Routing", "de": "Flask & Routing"},
        "desc": {
            "en": "Flask maps URLs to Python functions using <code>@app.route('/path')</code>. When a request arrives, Flask matches the path, calls the function, and returns whatever it gives back — usually HTML rendered from a Jinja template, or JSON for API endpoints.",
            "de": "Flask ordnet URLs Python-Funktionen mit <code>@app.route('/path')</code> zu. Wenn eine Anfrage eintrifft, matcht Flask den Pfad, ruft die Funktion auf und gibt zurück, was sie liefert — normalerweise HTML aus einem Jinja-Template oder JSON für API-Endpunkte.",
        },
        "devtools": {
            "en": "Visit <a href='/routes' style='color:var(--accent)'>/routes</a> to see every URL CyberShop handles. In Network tab, click a request and look at the <b>General</b> section — the URL maps directly to a Python function name.",
            "de": "Besuche <a href='/routes' style='color:var(--accent)'>/routes</a>, um alle URLs von CyberShop zu sehen. Im Network-Tab, klicke eine Anfrage an und sieh den <b>General</b>-Bereich — die URL entspricht direkt einem Python-Funktionsnamen.",
        },
        "files": ["app.py", "api.py", "auth.py", "templates/"],
        "page": "/routes",
    },
    {
        "id": "sql",
        "title": {"en": "Databases & SQL", "de": "Datenbanken & SQL"},
        "desc": {
            "en": "Products, users, and orders are stored in SQLite. Every page that displays data runs a SQL query behind the scenes. The <b>Inspector</b> bar at the bottom of this page shows the exact SQL that was run to generate what you're currently looking at.",
            "de": "Produkte, Nutzer und Bestellungen sind in SQLite gespeichert. Jede Seite, die Daten anzeigt, führt im Hintergrund eine SQL-Abfrage aus. Die <b>Inspektor</b>-Leiste unten zeigt das genaue SQL, das für die aktuelle Seite ausgeführt wurde.",
        },
        "devtools": {
            "en": "Click the <b>🔍 Inspector</b> bar at the bottom to expand it — you'll see the SQL queries run for this page. Navigate to different pages and watch the queries change. Also open <code>schema.sql</code> to see the table structure.",
            "de": "Klicke auf die <b>🔍 Inspektor</b>-Leiste unten, um sie aufzuklappen — du siehst die SQL-Abfragen für diese Seite. Navigiere zu verschiedenen Seiten und beobachte die Änderungen. Öffne auch <code>schema.sql</code> für die Tabellenstruktur.",
        },
        "files": ["schema.sql", "db.py", "seed.py"],
        "page": "/account",
    },
    {
        "id": "cookies",
        "title": {"en": "Cookies & Sessions", "de": "Cookies & Sessions"},
        "desc": {
            "en": "Your cart is stored in a Flask <b>session</b> — a dictionary that lives on the server, tied to a cookie in your browser. The browser sends the session cookie with every request so Flask knows who you are. The language preference is stored as a plain cookie.",
            "de": "Dein Warenkorb ist in einer Flask-<b>Session</b> gespeichert — einem Dictionary auf dem Server, das mit einem Cookie im Browser verknüpft ist. Der Browser sendet das Session-Cookie mit jeder Anfrage. Die Spracheinstellung wird als einfaches Cookie gespeichert.",
        },
        "devtools": {
            "en": "<kbd>F12</kbd> → <b>Application</b> → <b>Cookies</b> → localhost. You'll see the <code>session</code> cookie (HttpOnly — JavaScript can't read it) and the <code>lang</code> cookie (plain text). Switch EN/DE and watch <code>lang</code> change.",
            "de": "<kbd>F12</kbd> → <b>Application</b> → <b>Cookies</b> → localhost. Du siehst das <code>session</code>-Cookie (HttpOnly — JavaScript kann es nicht lesen) und das <code>lang</code>-Cookie (Klartext). Wechsle EN/DE und beobachte die Änderung.",
        },
        "files": ["api.py (session['cart'])", "app.py (/set-lang route)"],
        "page": "/cart",
    },
    {
        "id": "auth",
        "title": {"en": "Authentication", "de": "Authentifizierung"},
        "desc": {
            "en": "Passwords are never stored in plain text — Flask hashes them using <code>werkzeug</code> (a bcrypt-style algorithm). On login, the hash is compared. If correct, the user's ID is stored in the session. Protected routes check the session before serving the page.",
            "de": "Passwörter werden nie im Klartext gespeichert — Flask hasht sie mit <code>werkzeug</code> (einem bcrypt-ähnlichen Algorithmus). Beim Login wird der Hash verglichen. Wenn korrekt, wird die User-ID in der Session gespeichert. Geschützte Routen prüfen die Session.",
        },
        "devtools": {
            "en": "Log out, then try visiting <code>/checkout</code> directly — you get redirected. Log back in → Network → find the POST to <code>/login</code> → <b>Payload</b>: the password is visible in plain text here. This is why HTTPS matters.",
            "de": "Abmelden, dann <code>/checkout</code> direkt aufrufen — du wirst weitergeleitet. Wieder anmelden → Network → POST zu <code>/login</code> → <b>Payload</b>: Das Passwort ist hier im Klartext sichtbar. Deshalb ist HTTPS wichtig.",
        },
        "files": ["auth.py"],
        "page": "/login",
    },
    {
        "id": "api",
        "title": {"en": "REST APIs", "de": "REST APIs"},
        "desc": {
            "en": "CyberShop has a JSON API alongside its HTML pages. The same product data is available at <code>/api/products</code> as JSON. JavaScript uses the API to update the cart badge without reloading. You can call the API directly from DevTools or a terminal.",
            "de": "CyberShop hat eine JSON-API neben seinen HTML-Seiten. Dieselben Produktdaten sind unter <code>/api/products</code> als JSON verfügbar. JavaScript nutzt die API für Warenkorb-Updates. Die API kann direkt aus DevTools oder dem Terminal aufgerufen werden.",
        },
        "devtools": {
            "en": "Open <a href='/api/products' target='_blank' style='color:var(--accent)'>/api/products</a> in a new tab — raw JSON. In the Network tab, filter by <b>Fetch/XHR</b> to see only API calls. Add something to the cart and watch the request.",
            "de": "Öffne <a href='/api/products' target='_blank' style='color:var(--accent)'>/api/products</a> in einem neuen Tab — rohes JSON. Im Network-Tab, filtere nach <b>Fetch/XHR</b>, um nur API-Aufrufe zu sehen. Artikel in den Warenkorb legen und Anfrage beobachten.",
        },
        "files": ["api.py"],
        "page": "/routes",
    },
    {
        "id": "ai",
        "title": {"en": "AI Integration", "de": "KI-Integration"},
        "desc": {
            "en": "The shopping assistant calls Google Gemini <b>on the server</b>. Your browser sends a question to Flask, Flask calls the Gemini API using an API key, and sends the answer back. The key never reaches the browser. If no key is set, you get a sensible offline fallback.",
            "de": "Der Einkaufsassistent ruft Google Gemini <b>auf dem Server</b> auf. Der Browser sendet eine Frage an Flask, Flask ruft die Gemini-API mit einem API-Schlüssel auf und sendet die Antwort zurück. Der Schlüssel erreicht den Browser nie. Ohne Schlüssel gibt es einen Offline-Fallback.",
        },
        "devtools": {
            "en": "Click the <b>💬</b> button (bottom right) → ask a question → Network → find the POST to <code>/api/ai/ask</code> → check Payload (your question) and Response (the AI answer). Notice the latency.",
            "de": "Klicke den <b>💬</b>-Button (unten rechts) → Frage stellen → Network → POST zu <code>/api/ai/ask</code> → Payload (deine Frage) und Response (KI-Antwort). Beachte die Latenz.",
        },
        "files": ["ai.py", "api.py (ai_ask route)"],
        "page": None,
    },
    {
        "id": "tls",
        "title": {"en": "TLS & HTTPS", "de": "TLS & HTTPS"},
        "desc": {
            "en": "TLS encrypts traffic between browser and server. Without it, passwords sent in login forms are readable on the network. Run Flask with <code>flask run --cert=adhoc</code> to enable HTTPS with a self-signed certificate — you'll get a browser warning because it's not signed by a trusted CA.",
            "de": "TLS verschlüsselt den Datenverkehr zwischen Browser und Server. Ohne TLS sind Passwörter im Login-Formular im Netzwerk lesbar. Starte Flask mit <code>flask run --cert=adhoc</code> für HTTPS mit einem selbst signierten Zertifikat — der Browser warnt, da es nicht von einer vertrauenswürdigen CA signiert ist.",
        },
        "devtools": {
            "en": "With HTTPS running: click the <b>padlock</b> in the address bar → <b>Certificate is valid</b> to inspect it. In Network → select a request → <b>Security</b> panel to see TLS version and cipher suite.",
            "de": "Mit HTTPS: Klicke das <b>Schloss</b> in der Adressleiste → <b>Zertifikat ist gültig</b>. Im Network-Tab → Anfrage auswählen → <b>Security</b>-Panel für TLS-Version und Cipher Suite.",
        },
        "files": ["run: flask run --cert=adhoc"],
        "page": None,
    },
]


def get_lang():
    return request.cookies.get('lang', 'en')


def t(key):
    lang = get_lang()
    entry = STRINGS.get(key)
    if entry is None:
        return key
    return entry.get(lang, entry.get('en', key))


def get_topics():
    lang = get_lang()
    result = []
    for topic in TOPICS:
        result.append({
            "id": topic["id"],
            "title": topic["title"].get(lang, topic["title"]["en"]),
            "desc": topic["desc"].get(lang, topic["desc"]["en"]),
            "devtools": topic["devtools"].get(lang, topic["devtools"]["en"]),
            "files": topic.get("files", []),
            "page": topic.get("page"),
        })
    return result

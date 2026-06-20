import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from db import init_db, query, execute
from auth import auth_bp, login_required, load_user
from api import api_bp
from i18n import t, get_topics, get_lang


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cybershop-dev-secret-change-me')
    app.config['DATABASE'] = os.path.join(app.instance_path, 'cybershop.db')

    os.makedirs(app.instance_path, exist_ok=True)

    init_db(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    @app.before_request
    def _before():
        load_user()
        g.lang = get_lang()
        if not hasattr(g, 'query_log'):
            g.query_log = []

    @app.context_processor
    def _inject():
        cart_count = sum(session.get('cart', {}).values())
        return {
            't': t,
            'lang': g.lang,
            'current_user': getattr(g, 'user', None),
            'cart_count': cart_count,
            'query_log': getattr(g, 'query_log', []),
            'request': request,
            'topics': get_topics(),
        }

    # ── Page routes ──────────────────────────────────────────────────────────

    @app.route('/')
    def index():
        category = request.args.get('cat', '')
        if category:
            products = query('SELECT * FROM products WHERE category = ? ORDER BY name', (category,))
        else:
            products = query('SELECT * FROM products ORDER BY category, name')
        categories = query('SELECT DISTINCT category FROM products ORDER BY category')
        return render_template('index.html', products=products, categories=categories,
                               active_cat=category, active_topic='html')

    @app.route('/product/<int:pid>')
    def product(pid):
        p = query('SELECT * FROM products WHERE id = ?', (pid,), one=True)
        if not p:
            return render_template('404.html'), 404
        return render_template('product.html', product=p, active_topic='javascript')

    @app.route('/cart')
    def cart():
        cart_data = session.get('cart', {})
        items = []
        total = 0.0
        for pid_str, qty in cart_data.items():
            p = query('SELECT * FROM products WHERE id = ?', (int(pid_str),), one=True)
            if p:
                subtotal = p['price'] * qty
                total += subtotal
                items.append({**dict(p), 'quantity': qty, 'subtotal': subtotal})
        return render_template('cart.html', items=items, total=round(total, 2),
                               active_topic='cookies')

    @app.route('/checkout', methods=['GET', 'POST'])
    @login_required
    def checkout():
        cart_data = session.get('cart', {})
        if not cart_data:
            flash(t('flash.cart_empty'), 'warning')
            return redirect(url_for('cart'))

        items = []
        total = 0.0
        for pid_str, qty in cart_data.items():
            p = query('SELECT * FROM products WHERE id = ?', (int(pid_str),), one=True)
            if p:
                subtotal = p['price'] * qty
                total += subtotal
                items.append({**dict(p), 'quantity': qty, 'subtotal': subtotal})

        if request.method == 'POST':
            order_id = execute(
                'INSERT INTO orders (user_id, total) VALUES (?, ?)',
                (g.user['id'], round(total, 2))
            )
            for item in items:
                execute(
                    'INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (?, ?, ?, ?)',
                    (order_id, item['id'], item['quantity'], item['price'])
                )
            session.pop('cart', None)
            flash(t('flash.order_placed'), 'success')
            return redirect(url_for('account'))

        return render_template('checkout.html', items=items, total=round(total, 2),
                               active_topic='auth')

    @app.route('/account')
    @login_required
    def account():
        orders = query(
            '''SELECT o.id, o.total, o.status, o.created_at,
                      GROUP_CONCAT(p.name || " x" || oi.quantity, ", ") as items_summary
               FROM orders o
               JOIN order_items oi ON oi.order_id = o.id
               JOIN products p ON p.id = oi.product_id
               WHERE o.user_id = ?
               GROUP BY o.id
               ORDER BY o.created_at DESC''',
            (g.user['id'],)
        )
        return render_template('account.html', orders=orders, active_topic='sql')

    @app.route('/routes')
    def route_map():
        routes = []
        for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
            methods = ', '.join(sorted(m for m in rule.methods if m not in ('HEAD', 'OPTIONS')))
            routes.append({'rule': rule.rule, 'endpoint': rule.endpoint, 'methods': methods})
        return render_template('routes.html', routes=routes, active_topic='flask')

    @app.route('/set-lang/<lang>')
    def set_lang(lang):
        if lang not in ('en', 'de'):
            lang = 'en'
        resp = redirect(request.referrer or url_for('index'))
        resp.set_cookie('lang', lang, max_age=60*60*24*365, samesite='Lax')
        return resp

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html', active_topic='http'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

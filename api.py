from flask import Blueprint, jsonify, request, session
from db import query, execute
from i18n import t, get_lang
from ai import ask_assistant

api_bp = Blueprint('api', __name__, url_prefix='/api')


# ── Products ──────────────────────────────────────────────────────────────────

@api_bp.route('/products')
def products():
    rows = query('SELECT * FROM products ORDER BY category, name')
    return jsonify([dict(r) for r in rows])


@api_bp.route('/products/<int:pid>')
def product(pid):
    row = query('SELECT * FROM products WHERE id = ?', (pid,), one=True)
    if not row:
        return jsonify({'error': 'not found'}), 404
    return jsonify(dict(row))


# ── Cart ──────────────────────────────────────────────────────────────────────

def _cart():
    return session.get('cart', {})


def _save_cart(cart):
    session['cart'] = cart
    session.modified = True


@api_bp.route('/cart')
def get_cart():
    cart = _cart()
    items = []
    total = 0.0
    for pid_str, qty in cart.items():
        product = query('SELECT * FROM products WHERE id = ?', (int(pid_str),), one=True)
        if product:
            subtotal = product['price'] * qty
            total += subtotal
            items.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': qty,
                'subtotal': subtotal,
                'image_url': product['image_url'],
            })
    return jsonify({'items': items, 'total': round(total, 2), 'count': sum(cart.values())})


@api_bp.route('/cart/add', methods=['POST'])
def cart_add():
    data = request.get_json(force=True)
    pid = str(data.get('product_id', ''))
    qty = int(data.get('quantity', 1))
    if not pid:
        return jsonify({'error': 'missing product_id'}), 400
    cart = _cart()
    cart[pid] = cart.get(pid, 0) + qty
    _save_cart(cart)
    return jsonify({'count': sum(cart.values()), 'message': t('flash.added_cart')})


@api_bp.route('/cart/remove', methods=['POST'])
def cart_remove():
    data = request.get_json(force=True)
    pid = str(data.get('product_id', ''))
    cart = _cart()
    cart.pop(pid, None)
    _save_cart(cart)
    return jsonify({'count': sum(cart.values()), 'message': t('flash.removed_cart')})


@api_bp.route('/cart/update', methods=['POST'])
def cart_update():
    data = request.get_json(force=True)
    pid = str(data.get('product_id', ''))
    qty = int(data.get('quantity', 1))
    cart = _cart()
    if qty <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = qty
    _save_cart(cart)
    return jsonify({'count': sum(cart.values())})


@api_bp.route('/cart/clear', methods=['POST'])
def cart_clear():
    _save_cart({})
    return jsonify({'count': 0})


# ── AI ────────────────────────────────────────────────────────────────────────

@api_bp.route('/ai/ask', methods=['POST'])
def ai_ask():
    data = request.get_json(force=True)
    question = data.get('question', '').strip()
    if not question:
        return jsonify({'error': 'missing question'}), 400
    lang = get_lang()
    products = [dict(r) for r in query('SELECT * FROM products ORDER BY name')]
    answer, is_live = ask_assistant(question, products, lang)
    return jsonify({'answer': answer, 'live': is_live})

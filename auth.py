from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from db import query, execute
from i18n import t

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash(t('flash.login_required'), 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def load_user():
    user_id = session.get('user_id')
    if user_id:
        g.user = query('SELECT * FROM users WHERE id = ?', (user_id,), one=True)
    else:
        g.user = None


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = query('SELECT * FROM users WHERE username = ?', (username,), one=True)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash(t('flash.logged_in'), 'success')
            return redirect(url_for('index'))
        flash(t('flash.invalid_credentials'), 'error')
    return render_template('login.html', page='login')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        existing = query('SELECT id FROM users WHERE username = ?', (username,), one=True)
        if existing:
            flash(t('flash.username_taken'), 'error')
        else:
            execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, generate_password_hash(password))
            )
            user = query('SELECT * FROM users WHERE username = ?', (username,), one=True)
            session['user_id'] = user['id']
            flash(t('flash.registered'), 'success')
            return redirect(url_for('index'))
    return render_template('register.html', page='register')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash(t('flash.logged_out'), 'info')
    return redirect(url_for('index'))

import sqlite3
from flask import g, current_app

_query_log = []  # per-request SQL log for the inspector


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.query_log = []
    return g.db


def query(sql, args=(), one=False):
    db = get_db()
    if not hasattr(g, 'query_log'):
        g.query_log = []
    g.query_log.append(sql.strip())
    cur = db.execute(sql, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def execute(sql, args=()):
    db = get_db()
    if not hasattr(g, 'query_log'):
        g.query_log = []
    g.query_log.append(sql.strip())
    db.execute(sql, args)
    db.commit()
    return db.execute('SELECT last_insert_rowid()').fetchone()[0]


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    import os
    with app.app_context():
        db = get_db()
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path) as f:
            db.executescript(f.read())
        db.commit()
    app.teardown_appcontext(close_db)

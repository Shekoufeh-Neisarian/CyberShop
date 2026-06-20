"""Run once to populate the database with demo data."""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from db import get_db, execute, query
from werkzeug.security import generate_password_hash

PRODUCTS = [
    ("USB Security Key", "Hardware 2FA token — FIDO2/WebAuthn compatible. Plug in, tap, authenticated.", 29.99, "Security", "🔑"),
    ("Raspberry Pi 5", "4GB RAM single-board computer. Perfect for home lab projects, network monitoring, and learning.", 79.99, "Hardware", "🖥️"),
    ("Network Packet Sniffer", "Portable USB WiFi adapter in monitor mode. Capture and analyse traffic with Wireshark.", 24.99, "Hardware", "📡"),
    ("Python Crash Course (Book)", "Best-selling Python intro book, 3rd edition. From basics to projects in one volume.", 34.99, "Books", "📚"),
    ("SSL/TLS Certificate Guide (Book)", "Deep dive into PKI, certificate chains, and modern TLS configuration.", 29.99, "Books", "📖"),
    ("Ergonomic Mechanical Keyboard", "TKL layout, Cherry MX switches. Wrists will thank you during long coding sessions.", 119.99, "Hardware", "⌨️"),
    ("Privacy Screen Filter", "Micro-louver film blocks side-angle viewing. Fits 15\" laptops. Essential for coffee-shop coding.", 19.99, "Security", "🛡️"),
    ("CyberDeck Sticker Pack", "Terminal prompts, lock icons, and binary art. 20 vinyl stickers, weatherproof.", 9.99, "Merch", "🎨"),
    ("32GB Encrypted USB Drive", "Hardware-encrypted flash drive with PIN pad. Data stays safe even if lost.", 49.99, "Security", "💾"),
    ("Smart Home Hub", "Control lights, sensors, and locks from one dashboard. MQTT + REST API included.", 59.99, "Hardware", "🏠"),
    ("Pro Git (Book)", "Comprehensive Git reference by Scott Chacon. Free online, available in print.", 24.99, "Books", "📗"),
    ("Laptop Lock Cable", "Kensington-style security cable, 1.8m. Secure your laptop at the library or café.", 14.99, "Security", "🔒"),
]

def seed():
    app = create_app()
    with app.app_context():
        db = get_db()

        existing = db.execute('SELECT COUNT(*) FROM products').fetchone()[0]
        if existing > 0:
            print(f"DB already has {existing} products — skipping seed.")
            return

        for name, desc, price, category, emoji in PRODUCTS:
            db.execute(
                'INSERT INTO products (name, description, price, category, image_url) VALUES (?, ?, ?, ?, ?)',
                (name, desc, price, category, emoji)
            )

        # demo user: demo / demo123
        db.execute(
            'INSERT OR IGNORE INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            ('demo', 'demo@cybershop.local', generate_password_hash('demo123'))
        )
        db.commit()
        print(f"Seeded {len(PRODUCTS)} products + demo user (demo / demo123)")

if __name__ == '__main__':
    seed()

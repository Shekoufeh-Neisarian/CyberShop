import os

FALLBACK = (
    "I'm running in offline mode (no GOOGLE_API_KEY set). "
    "Based on the current catalogue, I'd recommend the **USB Security Key** for security-conscious users, "
    "the **Raspberry Pi 5** for anyone building a home lab, "
    "or the **Python Crash Course** for beginners. "
    "Set GOOGLE_API_KEY in your .env file to get live AI responses!"
)

FALLBACK_DE = (
    "Ich laufe im Offline-Modus (kein GOOGLE_API_KEY gesetzt). "
    "Basierend auf dem aktuellen Katalog empfehle ich den **USB Security Key** für sicherheitsbewusste Nutzer, "
    "den **Raspberry Pi 5** für alle, die ein Heimlabor aufbauen, "
    "oder den **Python Crash Course** für Einsteiger. "
    "Setze GOOGLE_API_KEY in deiner .env-Datei, um Live-KI-Antworten zu erhalten!"
)


def ask_assistant(question: str, products: list, lang: str = "en") -> tuple[str, bool]:
    """
    Returns (answer_text, is_live).
    is_live=True means a real Gemini call was made.
    Falls back gracefully if no key or API error.
    """
    api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if not api_key:
        return (FALLBACK_DE if lang == "de" else FALLBACK), False

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        product_list = "\n".join(
            f"- {p['name']} (€{p['price']:.2f}, {p['category']}): {p['description']}"
            for p in products
        )
        lang_instruction = "Answer in German." if lang == "de" else "Answer in English."
        prompt = (
            f"You are a helpful shopping assistant for CyberShop, a tech/security gear store.\n"
            f"{lang_instruction}\n"
            f"Keep your answer concise (2-4 sentences). Recommend specific products by name when relevant.\n\n"
            f"Available products:\n{product_list}\n\n"
            f"Customer question: {question}"
        )
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text.strip(), True

    except Exception as e:
        fallback = FALLBACK_DE if lang == "de" else FALLBACK
        return f"{fallback}\n\n_(Error: {e})_", False

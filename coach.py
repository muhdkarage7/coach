from flask import Flask, request
import requests
from translatepy import Translator
import json

app = Flask(__name__)

# === CONFIGURATION ===
GROQ_API_KEY = "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"  # GROQ AI key
GUPSHUP_API_KEY = "3gie2jrpmj6zb8n9gz4sulh5fcd98xsh"  # Gupshup API key
SANDBOX_PHONE = "+14155238886"  # Gupshup sandbox number
APP_NAME = "ABIACOACH"  # Name of your chatbot app on Gupshup
translator = Translator()

# === SYSTEM PROMPT FOR AI COACH ===
system_message = """
You are our personal life coach, team strategist, and startup co-founder.

🎯 TEAM BACKGROUND:
We are 4 brothers with different skills (engineering, crypto, hustle, and vision) working to build the next billion-dollar tech company.

Your job:
- Guide us like a top-tier startup mentor
- Suggest clear weekly goals
- Break down ideas into technical and business action plans
- Motivate us when we’re tired
- Suggest how to use each brother’s strength
- Help us stay focused on becoming billionaires, one smart move at a time

If we ask in Hausa, reply in Hausa.
"""

# === AI GENERATION FUNCTION ===
def generate_reply(user_input, lang="en"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        reply = result["choices"][0]["message"]["content"]

        if lang == "ha":
            translated = translator.translate(reply, "Hausa")
            return translated.result
        return reply

    except Exception as e:
        return f"Error: {str(e)}"

# === WHATSAPP WEBHOOK ROUTE ===
@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    data = request.json
    user_message = data.get("text", "")
    phone = data.get("sender", "")

    lang = "ha" if "yaya" in user_message.lower() or "ina" in user_message.lower() else "en"
    reply = generate_reply(user_message, lang=lang)

    send_whatsapp_message(phone, reply)
    return "ok", 200

# === SEND REPLY TO WHATSAPP USER ===
def send_whatsapp_message(phone, message):
    GUPSHUP_API_URL = "https://api.gupshup.io/sm/api/v1/msg"
    headers = {
        "apikey": GUPSHUP_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "channel": "whatsapp",
        "source": SANDBOX_PHONE,
        "destination": phone,
        "message": json.dumps({
            "type": "text",
            "text": message
        }),
        "src.name": APP_NAME
    }

    try:
        response = requests.post(GUPSHUP_API_URL, headers=headers, data=payload)
        print("✅ Message sent:", response.text)
    except Exception as e:
        print("❌ Send error:", e)

# === START THE SERVER ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

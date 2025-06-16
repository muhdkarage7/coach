# ===== Setup Flask App =====
from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
from groq import Groq
import threading
import requests
import time

# Create Flask app
app = Flask(__name__)
run_with_ngrok(app)

# Setup Groq client
client = Groq(api_key="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")

# Route
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "What should we focus on this week?")
    print("➡️ Incoming Question:", question)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": (
                    "You're a disciplined, aggressive startup coach. You're a guardian motivator. "
                    "You speak with confidence, urgency, and direction. Your tone is masculine, tough-love, no fluff. "
                    "You coach 4 African brothers building a multi-million dollar comms + crypto SaaS empire. "
                    "Every answer must drive action, focus, and monetization. Never philosophize. Never sugarcoat."
                )
            },
            {"role": "user", "content": question}
        ]
    )

    reply = response.choices[0].message.content.strip()
    print("✅ Coach says:", reply)
    return jsonify({"coach_says": reply})


# Function to test after a few seconds
def test_request():
    time.sleep(5)  # Wait for server to start
    url = "http://127.0.0.1:5000/ask"
    payload = {"question": "What's our most important revenue move this week?"}
    try:
        res = requests.post(url, json=payload)
        print("📦 Response from /ask route:\n", res.json())
    except Exception as e:
        print("❌ Request failed:", e)

# Start tester in background
threading.Thread(target=test_request).start()

# Run Flask
app.run()

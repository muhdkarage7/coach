from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Setup Groq client
client = Groq(api_key="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")

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

# Required by Render to bind correctly
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

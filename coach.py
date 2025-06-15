import requests

# === CONFIG ===
GROQ_API_KEY = "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"  # Use gsk_live_xxxxx from https://console.groq.com/keys
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

# === SYSTEM PROMPT ===
system_message = """
You are our personal life coach, team strategist, and startup co-founder.
🎯 TEAM BACKGROUND: We are 4 brothers with different skills (engineering, crypto, hustle, and vision) working to build the next billion-dollar tech company.
Your job: Guide us like a top-tier startup mentor. Suggest weekly goals. Break down ideas into technical and business steps.
"""

# === FUNCTION ===
def ask_coach(user_input):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"

# === TEST ===
response = ask_coach("Coach, what's one thing we should focus on this week?")
print("🤖 Coach says:", response)

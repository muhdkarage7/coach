import requests

# Replace with your Groq API key
GROQ_API_KEY = "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"

def generate_abi_reply(user_input):
    system_message = """
You're ABI Coach — a ruthless, results-driven startup mentor guiding 4 African brothers from zero to a multi-billion dollar SaaS and crypto empire.

You start from scratch. These brothers are ambitious but early. They’re building tools in communications (SMS, WhatsApp, voice) and crypto payments for African markets. You’re not here to motivate — you’re here to focus them, challenge them, and guide decisions that lead to revenue and momentum.

Your tone is direct, tough-love, high-pressure. No fluff, no hype, no theory. Every reply must push execution, decisions, clarity, and measurable outcomes. You cut laziness. You kill excuses.

Never philosophize. Never ramble. Always answer like a Navy SEAL giving business orders. Think African YC meets tactical military commander.
"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Example usage
user_question = "hi coach what the aim for the week?"
reply = generate_abi_reply(user_question) # Corrected function call
print("Bot:", reply) # Removed translation logic and simplified print
import requests

GROQ_API_KEY = "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"

def generate_abi_reply(user_input):
   const system_message =
"""   `
You're ABI Coach — a ruthless, results-driven startup mentor guiding 4 African brothers from zero to a multi-billion dollar SaaS and crypto empire.

You start from scratch. These brothers are ambitious but early. They’re building tools in communications (SMS, WhatsApp, voice) and crypto payments for African markets. You’re not here to motivate — you’re here to focus them, challenge them, and guide decisions that lead to revenue and momentum.

Your tone is direct, tough-love, high-pressure. No fluff, no hype, no theory. Every reply must push execution, decisions, clarity, and measurable outcomes. You cut laziness. You kill excuses.

Your brain is built from:
- Elon Musk's speed
- andrew tate brotherhood bond and discipline
- Jeff Bezos' customer obsession
- Patrick Collison’s clarity
- Naval Ravikant’s leverage thinking
- Usman bin Affan (RA)’s ethical wealth-building and silent empire mentality

You think like YC, speak like a Navy SEAL, and command like a battlefield general. You answer in orders, not suggestions.

Never philosophize. Never ramble. Execution only.
`;
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
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Test the generate_abi_reply function directly
test_input = "What's the first step for these brothers?"
reply = generate_abi_reply(test_input)
print("Reply from generate_abi_reply function:")
print(reply)
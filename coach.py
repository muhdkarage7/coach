# No longer need !pip install commands for Render, as dependencies are handled by requirements.txt
from flask import Flask, request, jsonify
import requests
# No longer need flask_ngrok for Render deployment
# from flask_ngrok import run_with_ngrok
import os # Import os to access environment variables

app = Flask(__name__)

# Fetch API key from environment variables for production
# This is crucial for security and best practice on platforms like Render
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    # This check is important for local development if not using environment variables,
    # but Render will ensure it's set if configured correctly.
    print("WARNING: GROQ_API_KEY environment variable not set. API calls may fail.")


def generate_abi_reply(user_input):
    """
    Generates a reply from the ABI Coach using the Groq API.

    Args:
        user_input (str): The user's message to the coach.

    Returns:
        str: The coach's reply or an error message.
    """
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY is not configured."

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
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0 and "message" in result["choices"][0]:
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"Error: Unexpected response structure from Groq API: {result}"
    except requests.exceptions.RequestException as e:
        # Catch network-related errors or bad HTTP responses
        return f"Error connecting to Groq API: {e}"
    except Exception as e:
        # Catch any other unexpected errors
        return f"An unexpected error occurred: {str(e)}"

@app.route("/coach", methods=["POST"])
def coach_endpoint():
    """
    Flask endpoint to receive user messages and return ABI Coach replies.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request must be JSON"}), 400

    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"error": "No 'message' field provided in JSON payload"}), 400

    # In a production environment like Render, logs are typically streamed to the platform's logging system.
    # print statements will show up in Render's logs.
    print(f"Received user input: {user_input}")
    reply = generate_abi_reply(user_input)
    print(f"Generated reply: {reply}")

    return jsonify({"reply": reply})

# The following block is typically removed or modified for production deployment
# as a WSGI server (like Gunicorn) will manage starting the app.
# If you run this file directly in a local development environment (not Render),
# it will still work as a standard Flask app.
if __name__ == "__main__":
    # For local development:
    # app.run(debug=True, port=os.getenv("PORT", 5000))
    # For Render, a WSGI server like Gunicorn will be used,
    # so this __main__ block is not strictly necessary for deployment
    # but good for local testing.
    print("Flask app ready. Use gunicorn to run in production (e.g., Render).")

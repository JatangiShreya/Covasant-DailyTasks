from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")

PORTKEY_API_URL = "https://api.portkey.ai/v1/chat/completions"

@app.route("/llm", methods=["POST"])
def llm_gateway():
    data = request.get_json()
    provider = data.get("provider")
    prompt = data.get("prompt")
    if not provider or not prompt:
        return jsonify({"error": "missing provider or prompt"}), 400
    
    payload = {
        "provider": provider,
        "prompt": prompt,
        "max_tokens": 100
    }
    headers = {
        "Authorization": f"Bearer {PORTKEY_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(PORTKEY_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return jsonify({"response": data.get("response", "No response received.")})

if __name__ == "__main__":
    app.run(debug=True)

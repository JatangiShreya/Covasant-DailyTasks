from flask import Flask, request, jsonify
import openai
import anthropic
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


openai.api_key = OPENAI_API_KEY
anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

@app.route("/llm", methods=["POST"])
def llm_gateway_func():
    data = request.get_json()
    provider = data.get("provider")
    prompt = data.get("prompt")
    
    if not provider or not prompt:
        return jsonify({"error": "missing provider or prompt"}), 400
        
    if provider == "openai":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"response": response.choices[0].message["content"]})
        
    elif provider == "anthropic":
        response = anthropic_client.completions.create(
            model="claude-3-opus-20240229",
            prompt=prompt,
            max_tokens_to_sample=100,
        )
        return jsonify({"response": response['completion'].strip()})

if __name__ == "__main__":
    app.run(debug=True)

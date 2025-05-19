import requests
import json
from dotenv import load_dotenv
load_dotenv()
url = "https://api.portkey.ai/v1/chat/completions"
PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
headers = {
    "Authorization": f"Bearer {PORTKEY_API_KEY}",
    "Content-Type": "application/json",
    "x-portkey-provider": "google",
    "x-portkey-google-api-key": GEMINI_API_KEY 
}
payload = {
    "prompt": "Tell me a joke",
    "max_tokens": 100
}
response = requests.post(url, headers=headers, json=payload)
if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Error:", response.status_code, response.text)

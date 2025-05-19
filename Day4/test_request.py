import requests

url="http://localhost:5000/llmm"
payload={
"provider":"openai",
"prompt":"Tell me a joke",
"max_tokens": 50
}
response=requests.post(url,json=payload)
print("Status:",response.status_code)
print("Raw Response Text:", response.text) 
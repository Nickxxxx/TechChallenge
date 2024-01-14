import requests
import os
from dotenv import load_dotenv
load_dotenv()


def prompt_gpt(text, openai_api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    payload = {
        "model": "gpt-4",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": text
              }
            ]
          }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()

openai_api_key = os.getenv('OPENAI_API_KEY')

text = "please rewrite the following text into email format: Good thing Mr. Smith We will meet tomorrow at 5, greetings Nick "

summary = prompt_gpt(text, openai_api_key)
output = summary["choices"][0]["message"]["content"]
print(output)
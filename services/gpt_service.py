import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_chatgpt_reply(message_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or use "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful HR assistant from HumanHire recruitment team."},
            {"role": "user", "content": message_text}
        ],
        max_tokens=150,
        temperature=0.7,
    )

    reply = response.choices[0].message.content.strip()
    return reply

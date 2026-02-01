from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = [
    {
        "role": "system",
        "content": (
            "Answer in detail. "
            "At the very end, add a concise 2–3 bullet point summary "
            "prefixed with 'SUMMARY:'."
        )
    }
]

def ask_ai(user_input):
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    full_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": full_reply})

    return full_reply   # 🔥 FULL TEXT ALWAYS

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv(".env")

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def career_advice(user_input):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Mochi AI, a career advisor."},
                {"role": "user", "content": user_input}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Groq error:", e)
        return "Mochi is loading rn... try again in a sec."
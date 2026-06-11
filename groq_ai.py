import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv(".env")

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def career_advice(user_input):
    print("USER INPUT:", user_input)
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
    {
        "role": "system",
        "content": """
You are Mochi AI, the talent discovery and employability assistant of BridgedIt.

Your goals:

1. Help students discover hidden talents.
2. Recommend career paths.
3. Suggest skills they should learn.
4. Recommend opportunities related to their interests.
5. Suggest role models and successful professionals.
6. Ask follow-up questions when information is limited.
7. Give practical and motivating advice.

If a student says:
'I like gaming'

Recommend:
- Game Developer
- Game Designer
- Esports Analyst
- Streamer
- UI/UX Designer
- 3D Artist

Explain why each career matches.

If a student says:
'I don't know my talents'

Start a short talent discovery quiz.

Always answer the user's actual question.
Do not introduce yourself repeatedly.
"""
    },
    {
        "role": "user",
        "content": user_input
    }
]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Groq error:", e)
        return f"ERROR: {e}"
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_questions(text: str, num_questions: int = 10) -> list[dict]:
    prompt = f"""
Generate {num_questions} multiple choice questions with 4 options and the correct answer based on the text below:

Text:
{text}

Return a JSON list of objects with 'question', 'options', and 'answer' keys.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a quiz generator AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return eval(response.choices[0].message.content)
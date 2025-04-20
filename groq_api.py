import os
from groq import Groq
from dotenv import load_dotenv
import re

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_text(text):
    prompt = f"Summarize the following content in bullet points:\n\n{text}"
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

def generate_mcq(text, num_questions=5):
    prompt = f"""
From the following content, generate {num_questions} multiple-choice questions with 4 options each.
Use the following format:

Q1: Question here
a) Option A
b) Option B
c) Option C
d) Option D
Answer: c

Content:
{text}
"""
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

def parse_mcq_text(raw_quiz_text):
    questions = []
    parts = re.split(r"\nQ\d+:", "\n" + raw_quiz_text)
    for part in parts[1:]:
        lines = part.strip().split("\n")
        question = lines[0].strip()
        options = {line[0]: line[3:].strip() for line in lines[1:5] if re.match(r"[abcd]\)", line)}
        answer_line = next((line for line in lines if line.startswith("Answer:")), None)
        correct = answer_line.split(":")[1].strip().lower() if answer_line else None
        questions.append({"question": question, "options": options, "answer": correct})
    return questions

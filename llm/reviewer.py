from llm.cache import load_cache, save_cache, generate_key
from groq import Groq
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def basic_review(analysis):
    return "Basic review: Code analyzed using rule-based system. Consider improving structure and readability."


def call_llm_api(prompt):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1,
            stream=False   # IMPORTANT: no streaming in Flask
        )

        return completion.choices[0].message.content

    except Exception as e:
        print("Groq API Error:", e)
        raise e


def generate_prompt(code, analysis):
    return f"""
You are a senior software engineer.

Review the following Python code.

STRICT RULES:
- Keep response under 150 words
- DO NOT include code snippets
- DO NOT rewrite the code
- Use bullet points only
- Be concise and actionable

Format EXACTLY like this:

Readability:
- ...

Performance:
- ...

Best Practices:
- ...

Code:
{code}

Analysis:
{analysis}
"""


def get_llm_review(code, analysis):
    cache = load_cache()
    key = generate_key(code, analysis)

    if key in cache:
        return cache[key]

    prompt = generate_prompt(code, analysis)

    response = None   

    try:
        response = call_llm_api(prompt)
    except Exception as e:
        print("LLM failed:", e)
        return basic_review(analysis)

    #Only process if response exists
    if not response:
        return basic_review(analysis)

    response = clean_response(response)

    cache[key] = response
    save_cache(cache)

    return response
    
def clean_response(text):
    return text.strip().replace("**", "")
    
def format_review(text):
    sections = {"Readability": [], "Performance": [], "Best Practices": []}
    
    current = None
    for line in text.split("\n"):
        line = line.strip()
        if "Readability" in line:
            current = "Readability"
        elif "Performance" in line:
            current = "Performance"
        elif "Best Practices" in line:
            current = "Best Practices"
        elif line.startswith("-") and current:
            sections[current].append(line[1:].strip())
    
    return sections
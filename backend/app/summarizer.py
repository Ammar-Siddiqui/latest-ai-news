import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_post(title, url):
    prompt = f"""
You are an AI assistant for a college student learning AI.

Summarize the following post.
Then explain why it's important, in a simple way that a college computer science student would understand.

Title: "{title}"
Link: {url}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return response.choices[0].message["content"]

    except Exception as e:
        print(f" GPT summarization failed for {title}: {e}")
        return "Summary not available."

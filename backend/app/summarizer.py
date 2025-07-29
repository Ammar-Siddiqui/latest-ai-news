import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_post(title, url):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize the article at the given URL in simple language for a college CS student. Include why it matters."},
                {"role": "user", "content": f"Title: {title}\nURL: {url}"}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"GPT summarization failed for {title}: {e}")
        return None



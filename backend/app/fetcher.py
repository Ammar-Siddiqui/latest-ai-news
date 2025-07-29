import requests
import feedparser
from datetime import datetime
import praw
import os
from dotenv import load_dotenv
from app.summarizer import summarize_post


load_dotenv()

def get_reddit_ai_posts():
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    print("Logged in as:", reddit.user.me())

    subs = ["MachineLearning", "artificial", "Futurology"]
    posts = []

    for sub in subs:
        print(f"Fetching from r/{sub}...")
        try:
            subreddit = reddit.subreddit(sub)
            for post in subreddit.top(time_filter="week", limit=3):
                if post.score < 50 or post.stickied:
                    continue

                posts.append({
                    "source": f"Reddit - r/{sub}",
                    "title": post.title,
                    "url": post.url,
                    "date": datetime.utcfromtimestamp(post.created_utc).isoformat(),
                    "points": post.score,
                    "summary": summarize_post(post.title, post.url)
                })
        except Exception as e:
            print(f"⚠️ Error while fetching r/{sub}: {e}")

    return posts



KEYWORDS = ["AI", "ML", "AGI", "robot", "OpenAI", "Google" , "Meta" , "Startup" , "future", "transform"]

def get_hackernews_ai():
    url = "https://hn.algolia.com/api/v1/search?tags=story&hitsPerPage=50"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    hits = response.json().get("hits", [])
    news_items = []

    for hit in hits:
        title = hit.get("title", "")
        url = hit.get("url")
        created = hit.get("created_at")
        points = hit.get("points", 0)

        if not url or not title:
            continue

        if any(keyword.lower() in title.lower() for keyword in KEYWORDS) and points >= 20:
            news_items.append({
                "source": "Hacker News",
                "title": title,
                "url": url,
                "date": created,
                "points": points,
                "summary": summarize_post(title, url)
            })

    return news_items


def get_arxiv_ml():
    feed_url = "https://export.arxiv.org/rss/cs.LG"  # Machine Learning RSS
    feed = feedparser.parse(feed_url)
    news = []

    for entry in feed.entries[:5]:
        news.append({
            "source": "arXiv ML",
            "title": entry.title,
            "url": entry.link,
            "date": entry.published,
            "summary": summarize_post(entry.title, entry.link)
        })

    return news


def get_openai_blog():
    feed_url = "https://openai.com/blog/rss.xml"
    feed = feedparser.parse(feed_url)
    news = []

    for entry in feed.entries[:5]:
        news.append({
            "source": "OpenAI Blog",
            "title": entry.title,
            "url": entry.link,
            "date": entry.published,
            "summary": summarize_post(entry.title, entry.link)
        })

    return news


def get_google_ai_blog():
    feed_url = "https://ai.googleblog.com/feeds/posts/default?alt=rss"
    feed = feedparser.parse(feed_url)
    news = []

    for entry in feed.entries[:5]:
        news.append({
            "source": "Google AI Blog",
            "title": entry.title,
            "url": entry.link,
            "date": entry.published,
            "summary": summarize_post(entry.title, entry.link)
        })

    return news


def get_huggingface_blog():
    feed_url = "https://huggingface.co/blog/rss.xml"
    feed = feedparser.parse(feed_url)
    news = []

    for entry in feed.entries[:5]:
        news.append({
            "source": "Hugging Face Blog",
            "title": entry.title,
            "url": entry.link,
            "date": entry.published,
            "summary": summarize_post(entry.title, entry.link)
        })

    return news


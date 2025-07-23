from fastapi import APIRouter
from app.fetcher import (
    get_reddit_ai_posts,
    get_hackernews_ai,
    get_arxiv_ml,
    get_openai_blog,
    get_google_ai_blog,
    get_huggingface_blog, )


router = APIRouter()

@router.get("/news")
def get_all_news():
    all_news = []
    all_news.extend(get_reddit_ai_posts())
    all_news.extend(get_hackernews_ai())
    all_news.extend(get_arxiv_ml())
    all_news.extend(get_openai_blog())
    all_news.extend(get_google_ai_blog())
    all_news.extend(get_huggingface_blog())
    sorted_news = sorted(all_news, key=lambda x: x['date'], reverse=True)
    return {"news": sorted_news}


@router.get("/")
def root():
    return {"message": "AI News Curator Backend is running!"}



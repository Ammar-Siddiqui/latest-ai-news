
import streamlit as st
import requests

st.set_page_config(page_title="AI News Curator", layout="centered")

st.title("🧠 Latest AI/ML News")
st.markdown("Summarized from Reddit, arXiv, OpenAI, and more. Updated weekly.")

with st.spinner("Fetching the latest news..."):
    try:
        res = requests.get("http://localhost:8000/news")
        res.raise_for_status()
        news = res.json().get("news", [])
    except Exception as e:
        st.error(f"Failed to load news. Error: {e}")
        news = []

if news:
    for item in news:
        st.subheader(item["title"])
        st.caption(f"{item['source']} • {item.get('date', '')}")
        st.write(item.get("summary", "No summary available."))
        st.markdown(f"[🔗 Read more]({item['url']})")
        st.markdown("---")
else:
    st.info("No news found.")

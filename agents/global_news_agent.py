# agents/global_news_agent.py
import os
import requests
from typing import List

from datetime import datetime, timedelta

def fetch_news_for_topics(topics: List[str], max_per_topic: int = 3) -> dict:
    news_data = {}
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    for topic in topics:
        try:
            url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&pageSize={max_per_topic}"
            response = requests.get(url)
            articles = response.json().get("articles", [])[:max_per_topic]
            news_data[topic] = [
                {"title": article["title"], "url": article["url"]}
                for article in articles
            ]
        except Exception as e:
            news_data[topic] = [{"error": str(e)}]
    return news_data



def fetch_news_last_24_hours(topics: List[str], max_per_topic: int = 3) -> dict:
    news_data = {}
    from_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    to_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

    for topic in topics:
        try:
            url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&pageSize={max_per_topic}"
            response = requests.get(url)
            articles = response.json().get("articles", [])[:max_per_topic]
            print(articles)
            print(topic)
            news_data[topic] = [
                {
                    "title": article["title"],
                    "url": article["url"],
                    "description": article.get("description", ""),
                    "publishedAt": article["publishedAt"]
                }
                for article in articles
            ]
        except Exception as e:
            news_data[topic] = [{"error": str(e)}]
    return news_data

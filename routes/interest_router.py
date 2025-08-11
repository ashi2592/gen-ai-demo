# routes/interest_route.py

from fastapi import APIRouter
from schema import InterestRequestSchema
from services.interest_service import extract_interests_from_input, store_user_interests, get_user_interests
from utils.constants import PREDEFINED_INTERESTS
from agents.global_news_agent import fetch_news_for_topics, fetch_news_last_24_hours
from utils.llm_model import generate_fact

router = APIRouter(prefix="/interest", tags=["Interest"])

@router.post("/update")
async def update_user_interests(request: InterestRequestSchema):
    user_input = request.user_input
    user_id =request.user_id

    if not user_input:
        return {"error": "Missing input"}

    extracted = extract_interests_from_input(user_input, PREDEFINED_INTERESTS)
    store_user_interests(user_id, extracted)

    return {"message": "Interests updated", "extracted": extracted}

@router.get("/list")
async def list_user_interests(user_id: int = 1):
    interests = get_user_interests(user_id)
    return {"user_id": user_id, "interests": interests}


@router.get("/news", summary="Personalized News", tags=["AgentAPI"])
async def get_personalized_news(user_id: int = 1):
    interests = get_user_interests(user_id)
    if not interests:
        return {"message": "No interests found. Update them first via /interest/update."}

    raw_news = fetch_news_for_topics(interests)
    print(raw_news)
    summarized_news = {}

    for topic, articles in raw_news.items():
        topic_news = []
        for article in articles:
            description = article.get("description", "")
            if description:
                summary = await generate_fact(description)
            else:
                summary = "No summary available."
            topic_news.append({
                "title": article["title"],
                "url": article["url"],
                "summary": summary
            })
        summarized_news[topic] = topic_news

    return {
        "user_id": user_id,
        "interests": interests,
        "personalized_news": summarized_news
    }


@router.get("/news/daily-summary", summary="Summarized News for Last 24 Hours", tags=["AgentAPI"])
async def get_daily_news_summary(user_id: int = 1):
    interests = get_user_interests(user_id)
    if not interests:
        return {"message": "No interests found for this user. Please update via /interest/update."}

    news = fetch_news_last_24_hours(interests)
    summarized = {}

    for topic, articles in news.items():
        topic_news = []
        for article in articles:
            desc = article.get("description", "")
            if desc:
                summary = await generate_fact(desc)
            else:
                summary = "No summary available."
            topic_news.append({
                "title": article["title"],
                "url": article["url"],
                "summary": summary,
                "publishedAt": article["publishedAt"]
            })
        summarized[topic] = topic_news

    return {
        "user_id": user_id,
        "interests": interests,
        "daily_news": summarized
    }

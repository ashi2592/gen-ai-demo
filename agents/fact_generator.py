import json
from sentence_transformers import SentenceTransformer, util
from services.user_facts_service import insert_user_fact, store_fact_chroma
from services.users_service import get_user
from services.items_service import read_items
from services.interaction_service import get_user_interactions
from utils.llm_model import llm
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import re

import re

def extract_clean_facts(text: str) -> list[str]:
    # Split on numbered bullet points
    raw_facts = re.findall(r'\d+\.\s+(.*?)(?:\n|$)', text.strip())
    cleaned_facts = []

    for fact in raw_facts:
        # Further split long sentences into smaller chunks
        parts = re.split(r'[.,;:]\s*', fact)
        for part in parts:
            stripped = part.strip()
            if len(stripped) > 4:
                cleaned_facts.append(stripped)
    
    return cleaned_facts


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def recommend_items(user_id: int, top_k: int = 5):
    # Step 1: Get user profile
    user = get_user({"id": user_id})
    if isinstance(user, str):
        return user

    preferences = user.get("preferences", [])
    if not preferences:
        return "No preferences found for user."

    # Step 2: Embed user preferences
    user_embedding = embedding_model.encode(" ".join(preferences), convert_to_tensor=True)

    # Step 3: Fetch all items
    all_items = read_items()
    if not all_items:
        return "No items available."

    # Step 4: Get user's past interactions
    interactions = get_user_interactions({"user_id": user_id})
    interacted_item_ids = set([i["item_id"] for i in interactions])

    # Step 5: Score and filter items
    scored_items = []
    for item in all_items:
        item_id = item[0]
        if item_id in interacted_item_ids:
            continue  # Skip already interacted items

        item_tags = json.loads(item[4]) if item[4] else []
        item_embedding = embedding_model.encode(" ".join(item_tags), convert_to_tensor=True)
        score = util.cos_sim(user_embedding, item_embedding).item()
        scored_items.append((item, score))

    # Step 6: Sort and pick top-K
    top_items = sorted(scored_items, key=lambda x: x[1], reverse=True)[:top_k]

    # Step 7: Use LLM for explanation
    item_descriptions = [f"{i[0][1]} ({i[0][2]})" for i in top_items]
    prompt = f"""
    You are a recommendation engine that generates personalized facts based on a user's interests and recommended items.

    User Info:
    - Name: {user['name']}
    - ID: {user['id']}
    - Preferences: {', '.join(preferences)}

    Recommended Items:
    {chr(10).join(f"{i+1}. {desc}" for i, desc in enumerate(item_descriptions))}

    Generate 3 short, personalized facts based on the user's preferences and the recommended items.
    Each fact should be concise and in natural language.

    Format:
    1. ...
    2. ...
    3. ...
    """

    llm_response = llm.invoke(prompt)

    facts = extract_clean_facts(llm_response.content)
    for fact in facts:
        insert_user_fact(user_id, fact=fact, source="LLM")
        store_fact_chroma(user_id, fact)

    # Step 8: Return results
    return {
        "recommended_items": [
            {
                "id": i[0][0],
                "name": i[0][1],
                "category": i[0][2],
                "tags": json.loads(i[0][4]),
                "score": round(i[1], 3)
            }
            for i in top_items
        ],
        "llm_explanation": llm_response.content
    }

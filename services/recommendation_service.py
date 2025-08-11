import json
from sentence_transformers import SentenceTransformer, util
from services.users_service import get_user
from services.items_service import read_items
from services.interaction_service import get_user_interactions
from utils.llm_model import llm

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
    prompt = f"Suggest these items to a user interested in {', '.join(preferences)}: {', '.join(item_descriptions)}. Explain why each item is a good match."

    llm_response = llm.invoke(prompt)

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

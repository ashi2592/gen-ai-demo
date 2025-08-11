from utils.db_utils import execute_query_with_fetch_all, execute_query_with_fetch_one,execute_query_with_lastrowid,execute_query_without_no_value
from typing import List
from sentence_transformers import SentenceTransformer, util
from datetime import datetime, timedelta, timezone

model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_interests_from_input(user_input: str, predefined_interests: List[str]) -> List[str]:
    input_embedding = model.encode(user_input, convert_to_tensor=True)
    interest_embeddings = model.encode(predefined_interests, convert_to_tensor=True)
    
    scores = util.cos_sim(input_embedding, interest_embeddings)[0]
    top_indices = scores.argsort(descending=True)[:3]  # top 3 related interests
    
    return [predefined_interests[i] for i in top_indices if scores[i] > 0.4]  # threshold


def store_user_interests(user_id: int, interests: List[str]):
    update_interest(user_id, interests)

def get_user_interests(user_id: int) -> List[str]:
    rows = execute_query_with_fetch_all("SELECT interest FROM user_interests WHERE user_id = ?", (user_id,))
    results = [row[0] for row in rows]
    return results


def classify_interest_category(user_id: int, topic: str):

    # Hot if count >= 3 in last 7 days
    recent_threshold = datetime.utcnow() - timedelta(days=7)
    row =  execute_query_with_fetch_one("""
        SELECT count, last_used FROM user_interests
        WHERE user_id=? AND interest=?
    """, (user_id, topic))
    if row:
        count, last_used = row
        last_used = datetime.fromisoformat(last_used)
        category = "hot" if count >= 3 and last_used >= recent_threshold else "cold"
        execute_query_without_no_value("UPDATE user_interests SET category=? WHERE user_id=? AND interest=?",
                    (category, user_id, topic))


def update_interest(user_id: int, topic: str):
    # Check if interest exists
    row = execute_query_with_fetch_one("SELECT count FROM user_interests WHERE user_id=? AND interest=?", (user_id, topic))
    
    now = datetime.now(timezone.utc)

    if row:
        new_count = row[0] + 1
        execute_query_without_no_value("""
            UPDATE user_interests
            SET count = ?, last_used = ?
            WHERE user_id = ? AND interest = ?
        """, (new_count, now, user_id, topic))
    else:
        execute_query_without_no_value("""
            INSERT INTO user_interests (user_id, interest, count, last_used)
            VALUES (?, ?, ?, ?)
        """, (user_id, topic, 1, now))
        
    classify_interest_category(user_id, topic)

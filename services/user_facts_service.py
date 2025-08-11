from utils.db_utils import execute_query_with_fetch_one,execute_query_with_lastrowid,execute_query_without_no_value
from utils.chroma_db import store_data_chroma
collection = store_data_chroma("user_facts")

def get_user_fact(user_id: int):
        result = execute_query_with_fetch_one("SELECT fact FROM user_facts WHERE user_id = ?", (user_id,))
        return result[0] if result else None

def insert_user_fact(user_id: int, fact: str, source: str = "manual"):
    last_row_id = execute_query_with_lastrowid("INSERT INTO user_facts (user_id, fact, source) VALUES (?, ?, ?)", (user_id, fact, source))
    return last_row_id

def update_user_fact(user_id: int, fact: str):
        execute_query_without_no_value("UPDATE user_facts SET fact = ? WHERE user_id = ?", (fact, user_id))


def store_fact_chroma(user_id: int, fact: str):
    collection.add(
        documents=[fact],
        metadatas=[{"user_id": user_id}],
        ids=[f"user_{user_id}_fact_{hash(fact)}"]
    )

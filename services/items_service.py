

# --- Database Initialization ---

from utils.db_utils import execute_query_without_no_value, execute_query_with_fetch_all, execute_query_with_fetch_one, execute_query_with_lastrowid
import json


def add_item(payload: dict) -> str:
    name = payload.get("name")
    category = payload.get("category")
    description = payload.get("description")
    tags = payload.get("tags",[])
   
    # Serialize the list to JSON string
    tag_json = json.dumps(tags)
   
    inserted_id = execute_query_with_lastrowid("""
        INSERT INTO items (name, category, description, tags)
        VALUES (?, ?, ?, ?)
    """, (name, category, description, tag_json))

    return "items created with id " + str(inserted_id)


def read_items(limit: int=100) -> str:
    rows = execute_query_with_fetch_all("""
        SELECT id, name, category, description, tags, timestamp
        FROM items
        ORDER BY timestamp DESC
        LIMIT 100
    """,(limit,))
    return rows

def get_item(payload: dict) -> str:
    user_id = payload.get("id")
    row = execute_query_with_fetch_one(""" SELECT id, name, category, description, tags, timestamp
        FROM items
        WHERE id = ?
    """, (user_id,))
    if row:
        return {
            "id": row[0] if row[0] is not None else "",
            "name": row[1] if row[1] is not None else "",
            "category": row[2] if row[2] is not None else "",
            "description": row[3] if row[3] is not None else "",
            "tags": row[4] if row[4] is not None else "",
            "timestamp": row[5] if row[5] is not None else "",
        }
    else:
        return "items not found." 


def update_item(payload: dict) -> str:

    name = payload.get("name")
    category = payload.get("category")
    description = payload.get("description")
    tags = payload.get("preferences")
    # Serialize the list to JSON string
    tag_json = json.dumps(tags, [])

    execute_query_without_no_value("""
        UPDATE items SET name=?, category=?, description=?, tags=?
        WHERE id=?
    """, (name, category, description, tag_json, payload.get("id")))

    return "items updated."

def delete_item(payload: dict) -> str:
    execute_query_without_no_value("DELETE FROM items WHERE id = ?", (payload.get("id"),))
    return "items deleted."  

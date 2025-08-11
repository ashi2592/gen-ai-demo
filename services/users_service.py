
from utils.db_utils import execute_query_without_no_value, execute_query_with_fetch_all, execute_query_with_fetch_one, execute_query_with_lastrowid


def get_user_prefernce_list(new_preferences: list[str], existing_pref_string: str=""):
    # Get and split existing comma-separated preferences
    existing_preferences = [p.strip() for p in existing_pref_string.split(",") if p.strip()]
    # Merge and deduplicate
    updated_preferences = list(set(existing_preferences + new_preferences))
    # Convert back to comma-separated string
    updated_pref_string = ",".join(updated_preferences)
    return  updated_pref_string
    

def add_user(payload: dict) -> str:
    name, age, occupation, preferences = payload
    preferences = get_user_prefernce_list(payload.get("preferences",[]))
    inserted_id = execute_query_with_lastrowid("""
        INSERT INTO users (name, age, occupation, preferences)
        VALUES (?, ?, ?, ?)
    """, (name, age, occupation, preferences))
    return "User created with id " + str(inserted_id)


def read_users(limit: int=100) -> str:
    rows = execute_query_with_fetch_all("""
        SELECT id, name, age, occupation, preferences, timestamp
        FROM users
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    return rows

def get_user(payload: dict) -> str:
    user_id = payload.get("id")
    row = execute_query_with_fetch_one(""" SELECT id, name, age, occupation, preferences, timestamp
        FROM users
        WHERE id = ?
    """, (user_id,))

    if row:
        return {
            "id": row[0] if row[0] is not None else "",
            "name": row[1] if row[1] is not None else "",
            "age": row[2] if row[2] is not None else "",
            "occupation": row[3] if row[3] is not None else "",
            "preferences": row[4] if row[4] is not None else "",
            "timestamp": row[5] if row[5] is not None else "",
        }
    else:
        return "User not found." 


def update_user(payload: dict) -> str:
    name, age, occupation, user_id, preferences = payload
    preferences = get_user_prefernce_list(payload.get("preferences",[]))
    execute_query_without_no_value("""
        UPDATE users SET name=?, age=?, occupation=?, preferences=?
        WHERE id=?
    """, (name, age, occupation, preferences, user_id))
    return "User updated."

def update_user_preferences(payload: dict) -> str:
    user_id, new_preferences = payload
    user = get_user({"id": user_id})
    if not user:
        return "User not found."
    preferences = get_user_prefernce_list(new_preferences, user.get("preferences"))
    execute_query_without_no_value("""
            UPDATE users SET preferences = ? WHERE id = ?
        """, (preferences, user_id))

    return "User updated."


def delete_user(payload: dict) -> str:
    execute_query_without_no_value("DELETE FROM users WHERE id = ?", (payload.get("user_id"),))
    return "User deleted."  

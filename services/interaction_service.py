from utils.db_utils import execute_query_with_fetch_all, execute_query_with_fetch_one,execute_query_with_lastrowid,execute_query_without_no_value


def add_user_item_interaction(payload: dict) -> str:
    inserted_id = execute_query_with_lastrowid("""
        INSERT INTO user_item_interactions (user_id, item_id, interaction_type, interaction_value)
        VALUES (?, ?, ?, ?)
    """, (
        payload.get("user_id"),
        payload.get("item_id"),
        payload.get("interaction_type"),
        payload.get("interaction_value")
    ))
    return f"Interaction created with id {inserted_id}"


def get_interaction(interaction_id: int):
    row =  execute_query_with_fetch_one("""
        SELECT id, user_id, item_id, interaction_type, interaction_value, timestamp
        FROM user_item_interactions
        WHERE id = ?
    """, (interaction_id,))
    if row:
        return {
            "id": row[0],
            "user_id": row[1],
            "item_id": row[2],
            "interaction_type": row[3],
            "interaction_value": row[4],
            "timestamp": row[5],
        }
    return "Interaction not found."


def list_interactions(limit: int = 100):
    rows = execute_query_with_fetch_all("""
        SELECT id, user_id, item_id, interaction_type, interaction_value, timestamp
        FROM user_item_interactions
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    return [
        {
            "id": row[0],
            "user_id": row[1],
            "item_id": row[2],
            "interaction_type": row[3],
            "interaction_value": row[4],
            "timestamp": row[5],
        }
        for row in rows
    ]


def update_interaction(interaction_id: int, payload: dict) -> str:
    execute_query_without_no_value("""
        UPDATE user_item_interactions
        SET user_id=?, item_id=?, interaction_type=?, interaction_value=?
        WHERE id=?
    """, (
        payload.get("user_id"),
        payload.get("item_id"),
        payload.get("interaction_type"),
        payload.get("interaction_value"),
        interaction_id
    ))
    return "Interaction updated."


def delete_interaction(interaction_id: int) -> str:
    execute_query_without_no_value("DELETE FROM user_item_interactions WHERE id = ?", (interaction_id,))
    return "Interaction deleted."


def get_user_interactions(payload: dict):
    try:
        user_id = payload.get("user_id")
        interactions = execute_query_with_fetch_all("""
            SELECT * FROM user_item_interactions WHERE user_id = ?
        """, (user_id,))

        if not interactions:
            return []

        # Format response
        result = []
        for interaction in interactions:
            result.append({
                "interaction_id": interaction[0],
                "user_id": interaction[1],
                "item_id": interaction[2],
                "interaction_type": interaction[3],
                "timestamp": interaction[4]
            })

        return result

    except Exception as e:
        return str(e)
    


from utils.chroma_db import store_data_chroma
from utils.db_utils import execute_query_without_no_value, execute_query_with_fetch_all, execute_query_with_fetch_one, execute_query_with_lastrowid
collection = store_data_chroma("transactions")

# --- CRUD Functions ---

def create_transaction(payload: dict) -> str:
    user_id = payload.get("user_id")
    description= payload.get("description")
    amount = payload.get("amount")
    category = payload.get("category")
    txn_type = payload.get("type")
    inserted_id = execute_query_with_lastrowid(
        "INSERT INTO transactions (user_id, description, amount,category,type) VALUES (?, ?, ?,?,?)",
        (user_id, description, amount,category, txn_type)
    )
    # Add to Chroma vector store
    metadata = {"user_id":user_id, "amount":  amount}
    collection.add(
        documents=[description],
        metadatas=[metadata],
        ids=[f"{user_id}_{inserted_id}"]
    )
    return "Transaction created."


def read_transactions(payload: dict) -> str:
    user_id = payload.get("user_id")
    rows = execute_query_with_fetch_all("""
        SELECT id, description, amount, category, timestamp,type
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 100
    """, (user_id,))
    transactions = [
        {
            "id": row[0] if row[0] is not None else "",
            "description": row[1] if row[1] is not None else "",
            "amount": row[2] if row[2] is not None else 0.0,
            "category": row[3] if row[3] is not None else "",
            "timestamp": row[4] if row[4] is not None else "",
            "type": row[5] if row[5] is not None else "",
        }
        for row in rows
    ]
    return transactions



def update_transaction(payload: dict) -> str:
    execute_query_without_no_value(
        "UPDATE transactions SET description=?, amount=? WHERE id=?",
        (payload.get("description"), payload.get("amount"), payload.get("id"))
    )
    return "Transaction updated."


def delete_transaction(payload: dict) -> str:
    execute_query_without_no_value("DELETE FROM transactions WHERE id = ?", (payload.get("id"),))
    return "Transaction deleted."


def get_total_amount(payload: dict):
    user_id = payload.get("user_id")
    txn_type = payload.get("type")  # "income" or "expense"
    date = payload.get("date")      # format: "YYYY-MM-DD"
    month = payload.get("month")    # format: "YYYY-MM" or just "MM"

    query = "SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = ?"
    params = [user_id, txn_type]

    if date:
        query += " AND DATE(timestamp) = ?"
        params.append(date)

    elif month:
        query += " AND strftime('%Y-%m', timestamp) = ?"
        params.append(month)

    result =execute_query_with_fetch_one(query, tuple(params))
    return result[0] if result and result[0] is not None else 0.0


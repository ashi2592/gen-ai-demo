from utils.db_utils import execute_query_without_no_value, execute_query_with_fetch_all, execute_query_with_lastrowid
from utils.llm_model import llm


def add_item(payload: dict):
    user_id, item, due_date, category, tags_str = (
        payload.get("user_id"),
        payload.get("item"),
        payload.get("due_date"),
        payload.get("category"),
        payload.get("tags")
    )   
    tags_str = ",".join(tags_str or [])
    execute_query_with_lastrowid("""
        INSERT INTO todos (user_id, item, status, due_at, category, tags)
        VALUES (?, ?, 'pending', ?, ?, ?)
    """, (user_id, item, due_date, category, tags_str))
    return f"[TodoAgent] Added task for user {user_id}: {item}"


def remove_item(user_id: int, id: int) -> str:
    execute_query_without_no_value("DELETE FROM todos WHERE user_id = ? AND id = ?", (user_id, id))
    return f"[TodoAgent] Removed task: {id}"

def mark_completed(user_id: int, id: int) -> str:
    execute_query_without_no_value("UPDATE todos SET status = 'done' WHERE user_id = ? AND id = ?", (user_id, id))
    return f"[TodoAgent] Marked as completed"

def mark_pending(user_id: int, item: str) -> str:
    execute_query_without_no_value("""
        UPDATE todos SET status = 'pending'
        WHERE user_id = ? AND item = ?
    """, (user_id, item))
    return f"[TodoAgent] Marked task as pending: {item}"

def add_reminder(user_id: int, item: str, due_at: str) -> str:

    execute_query_without_no_value("""
        UPDATE todos SET due_at = ?, remind = 1
        WHERE user_id = ? AND item = ?
    """, (due_at, user_id, item))
    return f"[TodoAgent] Reminder set for task: {item} at {due_at}"

def list_items(user_id: int, filter_by: str = "all") -> str:
    query = "SELECT id, item, due_at, category, tags, status FROM todos WHERE user_id = ?"
    if filter_by == "pending":
        query += " AND status = 'pending'"

    elif filter_by == "done":
        query += "AND status = 'done'"

    rows = execute_query_with_fetch_all(query, (user_id,))

    if not rows:
        return f"[TodoAgent] No tasks found for filter: {filter_by}"

    items = [
        {
            "id": row[0] if row[0] is not None else "",
            "item": row[1] if row[1] is not None else "",
            "due_at": row[2] if row[2] is not None else 0.0,
            "category": row[3] if row[3] is not None else "",
            "status": row[5] if row[5] is not None else "",
        }
        for row in rows
    ]
    return items


def summarize_tasks(user_id: int) -> str:
    tasks = execute_query_with_fetch_all("SELECT item, status, due_at, category, tags FROM todos WHERE user_id = ?", (user_id,))
    
    if not tasks:
        return "[TodoAgent] No tasks available for summarization."

    raw_summary_input = "\n".join([
        f"- {item} [{status}] | Due: {due_at or 'N/A'} | Category: {category or 'None'} | Tags: {tags or 'None'}"
        for item, status, due_at, category, tags in tasks
    ])

    prompt = (
        f"Summarize the following tasks:\n{raw_summary_input}\n\n"
        "Give:\n1. Number of pending and done tasks.\n"
        "2. Group tasks by category.\n"
        "3. Identify important tags.\n"
        "4. Highlight overdue tasks.\n"
    )
    response = llm.invoke(prompt)
    return f"[TodoAgent] Summary:\n{response.content}"



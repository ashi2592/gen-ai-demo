# agents/user_input_history_agent.py

from typing import Dict, List
from datetime import datetime

# In-memory user input store
user_input_history: Dict[int, List[Dict]] = {}

# Configurable max entries per user
MAX_HISTORY_LENGTH = 100

def store_user_input(user_id: int, task: str, input_text: str) -> Dict[str, str]:
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "task": task,
        "input": input_text.strip()
    }

    # Initialize user history
    if user_id not in user_input_history:
        user_input_history[user_id] = []

    # Deduplication check (skip if identical input already exists)
    if any(e["input"] == entry["input"] and e["task"] == entry["task"] for e in user_input_history[user_id]):
        return {"status": "duplicate_skipped", "entries": len(user_input_history[user_id])}

    # Append new entry
    user_input_history[user_id].append(entry)

    # Enforce max-length
    if len(user_input_history[user_id]) > MAX_HISTORY_LENGTH:
        user_input_history[user_id] = user_input_history[user_id][-MAX_HISTORY_LENGTH:]

    return {"status": "stored", "entries": len(user_input_history[user_id])}

def get_user_history(user_id: int) -> List[Dict]:
    return user_input_history.get(user_id, [])

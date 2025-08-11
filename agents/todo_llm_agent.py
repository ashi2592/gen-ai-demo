# File: agents/todo_llm_agent.py

import json
import re
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage
from utils.llm_model import llm
from services.todo_service import (
    add_item, remove_item, list_items,
    mark_completed, mark_pending,
    add_reminder, summarize_tasks
)

todo_prompt= """
You are an assistant that helps manage a user's to-do list. Extract the action, item description, due date, tags, and category from the message.

some example:
I want to finish work today 
finish work -> item
today -> due date
personal or office-> category

I have to drink water thrice in a day
drink water -> item
thrice in a day -> due date split into 3 parts
health-> category


Respond in JSON format like this:
{{
  "action": "add" | "remove" | "list" | "complete"  | "remind" | "summarize",
  "item": "<task description>",
  "due_date": "YYYY-MM-DD HH:MM" (optional),
  "tags": ["tag1", "tag2"] (optional),
  "category": "<category>" (optional)
  "status": "pending" (optional)
}}

User input:
"{user_input}"
User ID:
"{user_id}"
"""

def extract_json_block(text: str) -> str:
    match = re.search(r"\{[\s\S]*\}", text)
    return match.group(0) if match else None

def llm_todo_handler(input_data: dict) -> dict:
    user_input = input_data.get("input", "")
    user_id = input_data.get("user_id", "default")

    prompt = todo_prompt.format(user_input=user_input, user_id=user_id)
    response = llm.invoke([HumanMessage(content=prompt)])
    raw_output = response.content.strip()
    json_block = extract_json_block(raw_output)

    if not json_block:
        return {"user_id": user_id, "response": "[LLMTodoAgent] No valid JSON found in response."}

    try:
        parsed = json.loads(json_block)
        action = parsed.get("action").lower()
        item = parsed.get("item")
        due_date = parsed.get("due_date")
        tags = parsed.get("tags", [])
        category = parsed.get("category")
        status = parsed.get("status")

        print(action, item, due_date, tags, category, status)

        if action == "add" and item:
            return {"user_id": user_id, "response": add_item({"item":item, "user_id":user_id, "tags":tags, "category":category, "due_date":due_date})}
        elif action == "remove" and item:
            return {"user_id": user_id, "response": remove_item(item, user_id)}
        elif action == "complete" and item:
            return {"user_id": user_id, "response": mark_completed(item, user_id)}
        elif action == "summarize":
            return {"user_id": user_id, "response": summarize_tasks(user_id)}
        elif action == "list":
            return {"user_id": user_id, "response": list_items(user_id, status)}
        else:
            return {"user_id": user_id, "response": "[LLMTodoAgent] Unknown action or missing item."}

    except Exception as e:
        return {"user_id": user_id, "response": f"[LLMTodoAgent] Failed to parse input: {str(e)}"}

LLMTodoAgent = RunnableLambda(llm_todo_handler)

# File: agents/calendar_agent.py

from langchain_core.runnables import RunnableLambda
from datetime import datetime

# Placeholder function for calendar integration
calendar_storage = []  # In-memory for demo

def calendar_handler(input_data: dict) -> dict:
    title = input_data.get("title")
    date = input_data.get("date")  # expected format YYYY-MM-DD
    time = input_data.get("time", "00:00")  # optional time

    if not title or not date:
        return {"response": "[CalendarAgent] Title and date required."}

    try:
        datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return {"response": "[CalendarAgent] Invalid date or time format."}

    calendar_storage.append({"title": title, "date": date, "time": time})
    return {"response": f"[CalendarAgent] Event '{title}' set for {date} at {time}."}


CalendarAgent = RunnableLambda(calendar_handler)
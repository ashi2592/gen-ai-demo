# File: cli/main.py
import sys
import os
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.fact_generator import recommend_items
from utils.user_facts_utils import get_user_fact

# flow = generate_or_update_fact()

# def run_cli():
#     flow = build_langgraph_flow()
#     while True:
#         user_input = input("Enter task (chat, crud, youtube, prompt, calendar, ms_teams, todo): ")
#         if user_input.strip().lower() in ["exit", "quit"]:
#             break
#         result = asyncio.run(flow.ainvoke({"task": user_input, "input": user_input, "user_id": 1}))
#         print("Result:", result)


# if __name__ == "__main__":
#     run_cli()



def run_cli():
    result = recommend_items(user_id=4)
    #  result = get_user_fact(user_id=4)
    print(result)
       

        



if __name__ == "__main__":
    run_cli()

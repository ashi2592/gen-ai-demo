from dotenv import load_dotenv
from agents.intent_agent import SUPPORTED_TASKS
from schema import GraphStateSchema
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.llm_model import llm, generate_fact
from services.user_input_history_service import store_user_input

from agents import (
    chat_agent,
    transaction_llm_agent,
    youtube_agent,
    calendar_agent,
    todo_llm_agent,
)

load_dotenv() 


# Load agent based on task
def get_agent(task_name: str):
    agent_map = {
        "chat": chat_agent.chat_agent,
        "transaction": transaction_llm_agent.LLMTransactionAgent,
        "youtube": youtube_agent.YouTubeAgent,
        "calendar": calendar_agent.CalendarAgent,
        "todo": todo_llm_agent.LLMTodoAgent,
    }
    return agent_map.get(task_name)


TASK_ROUTER_PROMPT = ChatPromptTemplate.from_template("""
You are a task router for a multi-agent system. Given the user's input, determine the appropriate task.

Supported tasks: {supported_tasks}

Only respond with one of the task names.

User input: {user_input}
Some examples:
"I'm spending too much on food this week" => transaction
"Add dentist appointment to my calendar" => calendar
"Summarize this YouTube video" => youtube
"Add task to my to-do list" => todo
"Hey, how's the weather?" => chat
"I want to purchase a laptop please add in my list" => todo
                                                
""")

router_chain = TASK_ROUTER_PROMPT | llm | StrOutputParser()


# LangGraph router function
async def langgraph_router(payload):
    user_id = payload.get("user_id")
    user_input = payload.get("user_input")
    print(user_input,user_id)

    # Route the user input to the right task
    task = await router_chain.ainvoke({
        "user_input": user_input,
        "supported_tasks": ", ".join(SUPPORTED_TASKS)
    })
    
    task = task.strip().lower()
    agent = get_agent(task)

    # Store input before processing
    store_user_input(user_id=user_id, task=task, input_text=user_input)
    facts  =generate_fact(user_input)
    print(facts)

    if agent:
        print(f"Selected task: {task}")
        result = await agent.ainvoke({
            "input": user_input,  # original user input
            "task": task,
            "user_id": user_id
        })
        return {
            "response": result,
            "context": {"task": task},
            "next": END
        }
    else:
        return {
            "response": f"No agent found for task: {task}",
            "context": {"task": task},
            "next": END
        }


# Build the LangGraph flow
def build_langgraph_flow():
    graph = StateGraph(GraphStateSchema)
    graph.add_node("router", RunnableLambda(langgraph_router))
    graph.set_entry_point("router")
    graph.set_finish_point("router")  # Correct: "router" is the finish node
    return graph.compile()


if __name__ == "__main__":
    flow = build_langgraph_flow()
    result = flow.invoke({"user_input": "i want to add some task into my to-do list"})
    print("Flow Result:", result)

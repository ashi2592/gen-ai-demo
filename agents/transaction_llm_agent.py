import json
from utils.llm_model import llm
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage
from services.transaction_service import (
    create_transaction,
    read_transactions,
    update_transaction,
    delete_transaction,
    get_total_amount,
)

transcation_prompt = """
You are an assistant that helps manage a user's finance management. Extract the action and data from the message.

Respond ONLY in JSON format like this:
{{
  "action": "create" | "read" | "update" | "delete" | "summary",
  "payload": {{
    "user_id": "{user_id}",
    "description": "<description>",  // required for create/update
    "amount": 123.45,               // required for create/update
    "id": 1                         // required for update/delete
    "category": "<category>",       // optional for create/update
    "type": "expense" | "income"    // optional for create/update
  }}
}}

User message:
"{user_input}"
"""



def read_transaction_processing(rows, user_input):
    if not rows:
        return "No transactions found."

    # Build context for RAG
    context = "\n".join([
        f"{txn.get('id', '')} | {txn.get('description') or 'No description'} | ₹{txn.get('amount') or 0.0} | "
        f"{txn.get('category') or 'Uncategorized'} | {txn.get('timestamp') or 'No timestamp'} | {txn.get('type') or 'Unknown'}"
        for txn in rows
    ])


    print(context)

   

    rag_prompt = f"""
    You are a financial assistant. Based on the following transaction history, answer the user's query intelligently.

    Transaction History:
    {context}

    User Query:
    {user_input}

    Some example:
    total expense: 100000
    total income : 500000
    monthly expense: 200000
    monthly income: 300000
    area of improvement: you should avoid unnecessary expense
    your achivement:  car , house


    Guidelines for your response:
    - Consolidate expenses and provide total sums.
    - Summarize total income.
    - Categorize sources of income and expenses.
    - Highlight monthly and weekly patterns.
    - Comment on the behavior or trends in the user's spending and earning.

    Your response:
    """


    response = llm.invoke([HumanMessage(content=rag_prompt)])
    return response.content.strip()

def llm_transaction_handler(input_data: dict) -> dict:
    user_input = input_data.get("input", "")
    user_id = input_data.get("user_id", "default")

    # Format prompt
    prompt = transcation_prompt.format(user_input=user_input, user_id=user_id)

    # Call LLM
    response = llm.invoke([HumanMessage(content=prompt)])

    try:
        parsed = json.loads(response.content.strip())
        action = parsed.get("action", "").lower()
        payload = parsed.get("payload", {})

        # Inject user_id if missing
        payload["user_id"] = payload.get("user_id", user_id)

        print(action, payload)

        # Dispatch to appropriate function
        if action == "create":
            return {"user_id": user_id, "response": create_transaction(payload)}
        elif action == "read":
            return {"user_id": user_id, "response": read_transaction_processing(read_transactions(payload),user_input)}
        elif action == "update":
            return {"user_id": user_id, "response": update_transaction(payload)}
        elif action == "delete":
            return {"user_id": user_id, "response": delete_transaction(payload)}
        elif action == "summary":
            return {"user_id": user_id, "response": get_total_amount(payload)}
        else:
            return {"user_id": user_id, "response": f"[LLMTransactionAgent] Unknown action: {action}"}

    except Exception as e:
        return {
            "user_id": user_id,
            "response": f"[LLMTransactionAgent] Failed to parse or route action. Error: {str(e)}"
        }

# Wrap in LangChain Runnable
LLMTransactionAgent = RunnableLambda(llm_transaction_handler)

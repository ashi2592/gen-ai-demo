from fastapi import APIRouter, HTTPException
from services.langgraph_flow import build_langgraph_flow
from schema import AgentRequestSchema
from services.user_input_history_service import get_user_history


router = APIRouter(prefix="/agent", tags=["Agentic AI"])

# Load LangGraph flow once
flow = build_langgraph_flow()

@router.get("/", tags=["Health"])
def home():
    """Check if API is live."""
    return {"message": "FastAPI is working ✅"}

@router.post("/chat", summary="Agent Task Handler", tags=["AgentAPI"])
async def chat(request_data: AgentRequestSchema):
    """
    Handle multi-agent tasks like chat, calendar, todo, transactions, etc.
    """
    if not request_data.user_input:
        raise HTTPException(status_code=400, detail="Missing 'user_input' in request.")

    # LangGraph execution
    result = await flow.ainvoke({
        "user_input": request_data.user_input,
        "user_id": request_data.user_id
    })
 
    return {"response": result}

@router.get("/history/{user_id}", tags=["AgentAPI"], summary="Get User Input History")
async def get_history(user_id: int):
    """
    Retrieve input history for a given user.
    """
    history = get_user_history(user_id)
    return {"user_id": user_id, "history": history}



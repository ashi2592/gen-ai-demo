from typing import TypedDict, Optional, List
from pydantic import BaseModel


# Request model
class AgentRequestSchema(BaseModel):
    user_input: str
    user_id: int = 1


# Define your schema
class GraphStateSchema(TypedDict):
    user_input: str
    response: Optional[str]
    context: Optional[dict]
    task: str
    user_id: str
    intent: dict

class InterestRequestSchema(BaseModel):
    user_input: str
    user_id: int = 1

class ItemSchema(BaseModel):
    name: str 
    category: Optional[str] = None
    description: Optional[str] = None 
    id: Optional[int] = None 
    tags: Optional[list[str]] = None 

class TodoInputSchema(BaseModel):
    item: str
    tags: Optional[List[str]] = []
    category: Optional[str] = None
    due_date: Optional[str] = None  # Format: "YYYY-MM-DD HH:MM"
    reminder: Optional[bool] = False
    user_id: int

class TransactionInputSchema(BaseModel):
    description: str
    amount: float
    type: str  # "income" or "expense"
    category: Optional[str] = None
    date: Optional[str] = None  # Format: "YYYY-MM-DD"
    user_id: int

class TransactionReadInputSchema(BaseModel):
    user_id: str

class TransactionDeleteInputSchema(BaseModel):
    id: int
    user_id: str


class InteractionSchema(BaseModel):
    name: str 
    user_id: int
    item_id: int
    interaction_type: str
    interaction_value: str

class UserSchema(BaseModel):
    name: str 
    age: Optional[str] = None
    occupation: Optional[str] = None 
    id: Optional[int] = None 
    preferences: Optional[list[str]] = None 



class preferenceSchema(BaseModel):
    user_id: int = None
    preferences: Optional[list[str]] = []
    id: Optional[int] = None 

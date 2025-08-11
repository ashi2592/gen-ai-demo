from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import init_db
from routes import interest_router
from routes import users_router
from routes import items_router
from routes import user_interaction_router
from routes import chat_router

from routes import todo_router, transaction_router

app = FastAPI(
    title="Multi-Agent LLM API",
    description="Handles tasks like chat, transactions, and more using LangGraph agents.",
    version="1.0.0",
)

init_db()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interest_router.router)
app.include_router(todo_router.router)
app.include_router(transaction_router.router)
app.include_router(users_router.router)
app.include_router(items_router.router)
app.include_router(user_interaction_router.router)
app.include_router(chat_router.router)


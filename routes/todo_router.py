from fastapi import APIRouter
from schema import TodoInputSchema
from services.todo_service import (
    add_item, list_items, mark_completed, mark_pending,
    remove_item, summarize_tasks, add_reminder
)

router = APIRouter(prefix="/todo", tags=["Todo"])

@router.post("/add")
def add_todo(data: TodoInputSchema):
    print("Received data:", data)
    return add_item(data.dict())

@router.get("/list/{user_id}")
def list_todos(user_id: int):
    return list_items(user_id)

@router.post("/done")
def mark_done(data: TodoInputSchema):
    return mark_completed(data.item, data.user_id)

@router.post("/pending")
def mark_pending_status(data: TodoInputSchema):
    return mark_pending(data.item, data.user_id)

@router.post("/remove")
def remove_todo(data: TodoInputSchema):
    return remove_item(data.item, data.user_id)

@router.get("/summarize/{user_id}")
def summarize(user_id: int):
    return summarize_tasks(user_id)

@router.post("/remind")
def remind(data: TodoInputSchema):
    return add_reminder(data.item, data.user_id)

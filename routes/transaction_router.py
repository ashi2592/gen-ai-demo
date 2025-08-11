# routers/transaction_router.py

from fastapi import APIRouter
from schema import TransactionInputSchema
from services.transaction_service import (
    create_transaction, read_transactions, get_total_amount,
    delete_transaction
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/add")
def add_txn(data: TransactionInputSchema):
    return create_transaction(data.dict())

@router.get("/list/{user_id}")
def list_txns(user_id: int):
    return read_transactions({"user_id": user_id})  # ✅ Passed as dict

@router.get("/summarize/{user_id}")
def summarize_txns(user_id: int):
    return get_total_amount({"user_id": user_id})

@router.post("/remove/{id}")
def remove_txn(id:int):
    return delete_transaction({"id": id})

from fastapi import APIRouter
from schema import InteractionSchema
from services.interaction_service import add_user_item_interaction, get_interaction, update_interaction, delete_interaction, list_interactions


router = APIRouter(prefix="/user-interaction", tags=["User Interaction"])

@router.post("/")
def add_interaction(data: InteractionSchema):
    return add_user_item_interaction(data.dict())


@router.get("/")
def all_users():
    return list_interactions()

@router.get("/{id}")
def read(id: int):
    return get_interaction({"id": id})


@router.delete("/{id}")
def delete(id: int):
    return delete_interaction(id)
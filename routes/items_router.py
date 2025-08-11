
# routers/users.py
from fastapi import APIRouter
from schema import ItemSchema
from services.items_service import add_item, get_item, update_item, delete_item, read_items


router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/")
def create_item(item: ItemSchema):
    return add_item({"name": item.name, "category": item.category, "description": item.description, "tags": item.tags})

@router.get("/")
def all_items():
    return read_items()

@router.get("/{id}")
def read_item(id: int):
    return get_item({"id": id})

@router.put("/{id}")
def update_item(item: ItemSchema):
    return update_item({"name": item.name, "category": item.category, "description": item.description, "tags": item.tags})

@router.delete("/{item_id}")
def delete_item(item_id: int):
    return delete_item(item_id)
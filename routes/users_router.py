from fastapi import APIRouter
from schema import UserSchema, preferenceSchema
from services.users_service import add_user, get_user, update_user, delete_user, read_users, update_user_preferences


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user(user: UserSchema):
    return add_user({"name": user.name, "age": user.age, "occupation": user.occupation, "preferences": user.preferences})

@router.get("/")
def all_users():
    return read_users()

@router.get("/{id}")
def read_user(id: int):
    return get_user({"id": id})

@router.put("/{id}")
def update_user_call(user: UserSchema):
    return update_user({"id": user.id, "name": user.name, "age": user.age, "occupation": user.occupation, "preferences": user.preferences})


@router.put("/preferences")
def update_user_preferences_call(data: preferenceSchema):
    return update_user_preferences(data.dict())

@router.delete("/{user_id}")
def delete_user(user_id: int):
    return delete_user(user_id)
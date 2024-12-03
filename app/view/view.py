from fastapi import APIRouter, HTTPException
from app.controller.form_controller import (
    create_user, get_all_users, get_user_by_id, update_user, delete_user
)

router = APIRouter()

@router.post("/users/")
def create_user_endpoint(data: dict):
    result = create_user(data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/users/")
def get_all_users_endpoint():
    return get_all_users()

@router.get("/users/{user_id}")
def get_user_by_id_endpoint(user_id: str):
    result = get_user_by_id(user_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.put("/users/{user_id}")
def update_user_endpoint(user_id: str, data: dict):
    result = update_user(user_id, data)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.delete("/users/{user_id}")
def delete_user_endpoint(user_id: str):
    result = delete_user(user_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

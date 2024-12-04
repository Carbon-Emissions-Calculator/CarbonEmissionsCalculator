# from app.model.transport_model import User
from app.model.transport_mock import MockUser as User
from app.calculator.calculator import operation1

def create_user(data: dict):
    try:
        user = User(**data)
        user.save()
        return {"message": "User created successfully",
                "id": str(user.id),
                "calculation_results": {"carbon_emissions": operation1(user.name),
                                        "transport_trips": 1,
                                        "residuos": "hot cocoa",
                                        "gasoline": 12}}
    except Exception as e:
        return {"error": str(e)}

def get_all_users():
    users = User.objects()
    return [{"id": str(user.id), "name": user.name, "email": user.email} for user in users]

def get_user_by_id(user_id: str):
    try:
        user = User.objects(id=user_id).first()
        if user:
            return {"id": str(user.id), "name": user.name, "email": user.email, "calculation": operation1(user.name)}
        return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}

def update_user(user_id: str, data: dict):
    try:
        user = User.objects(id=user_id).first()
        if user:
            user.update(**data)
            return {"message": "User updated successfully"}
        return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}

def delete_user(user_id: str):
    try:
        user = User.objects(id=user_id).first()
        if user:
            user.delete()
            return {"message": "User deleted successfully"}
        return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}

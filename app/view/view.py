from fastapi import APIRouter, HTTPException
from app.controller.report_controller import (
    create_report, get_all_reports, get_report_by_id
)

#, update_report, delete_report

router = APIRouter()

@router.post("/report/")
def create_report_endpoint(data: dict):
    result = create_report(data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/reports/")
def get_all_reports_endpoint():
    return get_all_reports()

@router.get("/report/{report_id}")
def get_report_by_id_endpoint(report_id: str):
    result = get_report_by_id(report_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# @router.put("/users/{user_id}")
# def update_user_endpoint(user_id: str, data: dict):
#     result = update_user(user_id, data)
#     if "error" in result:
#         raise HTTPException(status_code=404, detail=result["error"])
#     return result

# @router.delete("/users/{user_id}")
# def delete_user_endpoint(user_id: str):
#     result = delete_user(user_id)
#     if "error" in result:
#         raise HTTPException(status_code=404, detail=result["error"])
#     return result

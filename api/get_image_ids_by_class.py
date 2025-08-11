from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from service.get_image_ids_by_class_service import get_image_ids_by_class_api_service

get_image_ids_by_class_router = APIRouter()



@get_image_ids_by_class_router.get('/get_image_ids_by_class')
def get_image_ids_by_class_api(class_id: str = Query(..., description="Class ID cần truy vấn")):
    result = get_image_ids_by_class_api_service(class_id)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

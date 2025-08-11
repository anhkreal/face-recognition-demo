from fastapi import APIRouter
from fastapi.responses import JSONResponse
from service.vector_info_service import get_vector_info_service


vector_info_router = APIRouter()

@vector_info_router.get('/vector_info')
def get_vector_info():
    result = get_vector_info_service()
    status_code = result.get("status_code", 200)
    # Xóa status_code khỏi dict nếu có
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)
    

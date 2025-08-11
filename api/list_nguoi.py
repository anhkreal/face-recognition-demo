

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from service.nguoi_info_service import get_nguoi_info_service

list_nguoi_router = APIRouter()

@list_nguoi_router.get('/list_nguoi')
def list_nguoi(
    query: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100)
):
    try:
        nguoi_list = get_nguoi_info_service(query, page, page_size)
        return JSONResponse(content={"results": nguoi_list}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

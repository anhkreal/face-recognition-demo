from fastapi import APIRouter, Query
from db import nguoi_repository

nguoi_info_router = APIRouter()
nguoi_repository = nguoi_repository.NguoiRepository()

@nguoi_info_router.get('/nguoi_info')
def get_nguoi_info_service(
    query: str = Query(""),
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100)
):
    try:
        result = nguoi_repository.search_nguoi_paged(query, page, page_size)
        print(f"Found {result['total']} results for query: {query}, page: {page}")
        return {
            "nguoi_list": [n.to_dict() for n in result['nguoi_list']],
            "total": result['total']
        }
    except Exception as e:
        return {"error": str(e)}

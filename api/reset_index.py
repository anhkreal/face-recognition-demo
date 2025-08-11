from fastapi import APIRouter
from fastapi.responses import JSONResponse

from service.reset_index_service import reset_index_api_service as reset_index_service

reset_router = APIRouter()



@reset_router.post('/reset_index')
def reset_index_api():
    result = reset_index_service()
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

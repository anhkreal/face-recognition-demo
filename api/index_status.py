from fastapi import APIRouter
from fastapi.responses import JSONResponse

from service.index_status_service import index_status_service

status_router = APIRouter()



@status_router.get('/index_status')
def index_status():
    result = index_status_service()
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

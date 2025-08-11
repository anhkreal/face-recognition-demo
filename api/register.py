from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from service.register_service import register_service
from Depend.depend import RegisterRequest, RegisterResponse
register_router = APIRouter()

@register_router.post('/register')
def register(request: RegisterRequest):
    success, message = register_service(request.username, request.passwrd)
    status = 200 if success else 400
    # return JSONResponse(content=RegisterResponse.as_response(success, message), status_code=status)
    return JSONResponse(content=RegisterResponse.as_response(success, message).dict(), status_code=status)
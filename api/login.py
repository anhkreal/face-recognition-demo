from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from service.login_service import login_service
from Depend.depend import LoginRequest, LoginResponse

login_router = APIRouter()

@login_router.post('/login')
def login(request: LoginRequest):
    if login_service(request.username, request.passwrd):
        resp = LoginResponse.as_response(True, "Đăng nhập thành công")
        if hasattr(resp, 'dict'):
            resp = resp.dict()
        return JSONResponse(content=resp, status_code=200)
    else:
        return JSONResponse(content={"success": False, "message": "Sai tên đăng nhập hoặc mật khẩu"}, status_code=401)

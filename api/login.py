from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from service.login_service import login_service
from Depend.depend import LoginRequest, LoginResponse

login_router = APIRouter()

@login_router.post(
    '/login',
    summary="Đăng nhập vào hệ thống",
    description="""
    **Xác thực người dùng để truy cập hệ thống**
    
    API này cho phép:
    - Đăng nhập bằng tên người dùng và mật khẩu
    - Xác thực thông tin đăng nhập
    - Trả về trạng thái đăng nhập
    
    **Thông tin đăng nhập:**
    - username: Tên đăng nhập đã đăng ký
    - passwrd: Mật khẩu tương ứng
    
    **Kết quả:**
    - Thành công: Trả về token hoặc xác nhận đăng nhập
    - Thất bại: Thông báo lỗi sai thông tin
    
    **Lưu ý:**
    - Cần đăng ký tài khoản trước khi đăng nhập
    - Mật khẩu được mã hóa an toàn
    - Session sẽ được duy trì sau khi đăng nhập thành công
    """,
    response_description="Kết quả đăng nhập với trạng thái thành công/thất bại",
    responses={
        200: {"description": "Đăng nhập thành công"},
        401: {"description": "Sai tên đăng nhập hoặc mật khẩu"}
    },
    tags=["🔐 Xác Thực"]
)
def login(request: LoginRequest):
    if login_service(request.username, request.passwrd):
        resp = LoginResponse.as_response(True, "Đăng nhập thành công")
        if hasattr(resp, 'dict'):
            resp = resp.dict()
        return JSONResponse(content=resp, status_code=200)
    else:
        return JSONResponse(content={"success": False, "message": "Sai tên đăng nhập hoặc mật khẩu"}, status_code=401)

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from service.register_service import register_service
from Depend.depend import RegisterRequest, RegisterResponse
register_router = APIRouter()

@register_router.post(
    '/register',
    summary="Đăng ký tài khoản mới",
    description="""
    **Tạo tài khoản người dùng mới để truy cập hệ thống**
    
    API này cho phép:
    - Đăng ký tài khoản với tên người dùng và mật khẩu
    - Kiểm tra tính hợp lệ của thông tin đăng ký
    - Mã hóa mật khẩu an toàn
    - Lưu thông tin tài khoản vào hệ thống
    
    **Thông tin đăng ký:**
    - username: Tên đăng nhập (phải là duy nhất)
    - passwrd: Mật khẩu (nên đủ mạnh để bảo mật)
    
    **Quy tắc:**
    - Tên đăng nhập không được trùng với tài khoản đã có
    - Mật khẩu nên có độ dài phù hợp
    - Tất cả ký tự đặc biệt được hỗ trợ
    
    **Kết quả:**
    - Thành công: Tài khoản được tạo, có thể đăng nhập ngay
    - Thất bại: Thông báo lỗi cụ thể (tên đã tồn tại, v.v.)
    """,
    response_description="Kết quả đăng ký với trạng thái thành công/thất bại",
    responses={
        200: {"description": "Đăng ký thành công"},
        400: {"description": "Lỗi đăng ký (tên đã tồn tại hoặc thông tin không hợp lệ)"}
    },
    tags=["🔐 Xác Thực"]
)
def register(request: RegisterRequest):
    success, message = register_service(request.username, request.passwrd)
    status = 200 if success else 400
    # return JSONResponse(content=RegisterResponse.as_response(success, message), status_code=status)
    return JSONResponse(content=RegisterResponse.as_response(success, message).dict(), status_code=status)
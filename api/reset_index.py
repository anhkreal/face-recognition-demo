from fastapi import APIRouter
from fastapi.responses import JSONResponse

from service.reset_index_service import reset_index_api_service as reset_index_service

reset_router = APIRouter()



@reset_router.post(
    '/reset_index',
    summary="Khởi tạo lại chỉ mục tìm kiếm",
    description="""
    **Xóa toàn bộ dữ liệu và khởi tạo lại hệ thống từ đầu**
    
    API này sẽ:
    - Xóa toàn bộ chỉ mục tìm kiếm FAISS
    - Xóa tất cả dữ liệu embedding đã lưu
    - Xóa thông tin người trong cơ sở dữ liệu
    - Khởi tạo lại hệ thống về trạng thái ban đầu
    
    **Cảnh báo:**
    - Thao tác này sẽ XÓA TẤT CẢ dữ liệu
    - Không thể hoàn tác sau khi thực hiện
    - Hệ thống sẽ trở về trạng thái trống hoàn toàn
    - Chỉ sử dụng khi muốn bắt đầu lại từ đầu
    
    **Sử dụng khi nào:**
    - Khởi tạo hệ thống lần đầu
    - Reset toàn bộ để import dữ liệu mới
    - Khắc phục lỗi chỉ mục bị hỏng
    - Testing và development
    """,
    response_description="Kết quả khởi tạo lại hệ thống",
    tags=["🗑️ Xóa Dữ Liệu"]
)
def reset_index_api():
    result = reset_index_service()
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

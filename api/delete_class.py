from fastapi import APIRouter, Query, Form, Depends
from fastapi.responses import JSONResponse
import numpy as np

from service.delete_class_service import delete_class_service
from Depend.depend import DeleteClassInput

delete_class_router = APIRouter()



@delete_class_router.post(
    '/delete_class',
    summary="Xóa toàn bộ thông tin một người",
    description="""
    **Xóa tất cả ảnh và thông tin của một người khỏi hệ thống**
    
    API này sẽ:
    - Xóa tất cả ảnh khuôn mặt thuộc class_id đã chỉ định
    - Loại bỏ toàn bộ đặc trưng khuôn mặt khỏi chỉ mục tìm kiếm
    - Xóa thông tin cá nhân (tên, tuổi, giới tính, nơi ở)
    - Cập nhật cơ sở dữ liệu hoàn toàn
    
    **Cách sử dụng:**
    - Cung cấp class_id của người cần xóa
    - class_id phải tồn tại trong hệ thống
    
    **Lưu ý:**
    - Thao tác này không thể hoàn tác
    - Sẽ xóa TẤT CẢ ảnh và thông tin liên quan đến class_id
    - Khác với delete_image chỉ xóa 1 ảnh cụ thể
    - Hãy chắc chắn trước khi thực hiện
    """,
    response_description="Kết quả xóa toàn bộ thông tin người",
    tags=["🗑️ Xóa Dữ Liệu"]
)
def delete_class(
    input: DeleteClassInput = Depends(DeleteClassInput.as_form)
):
    result = delete_class_service(input)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)
    
from fastapi import APIRouter, Form, Depends
from fastapi.responses import JSONResponse

from service.delete_image_service import delete_image_service
from Depend.depend import DeleteImageInput

delete_image_router = APIRouter()



@delete_image_router.post(
    '/delete_image',
    summary="Xóa ảnh khuôn mặt khỏi hệ thống",
    description="""
    **Xóa một ảnh khuôn mặt cụ thể khỏi cơ sở dữ liệu**
    
    API này sẽ:
    - Xóa ảnh khuôn mặt theo image_id
    - Loại bỏ đặc trưng khuôn mặt khỏi chỉ mục tìm kiếm
    - Cập nhật cơ sở dữ liệu
    - Không ảnh hưởng đến các ảnh khác cùng class_id
    
    **Cách sử dụng:**
    - Cung cấp image_id cần xóa
    - image_id phải tồn tại trong hệ thống
    
    **Lưu ý:**
    - Thao tác này không thể hoàn tác
    - Chỉ xóa 1 ảnh cụ thể, không xóa toàn bộ class
    - Nếu muốn xóa tất cả ảnh của 1 người, sử dụng API delete_class
    """,
    response_description="Kết quả xóa ảnh khuôn mặt",
    tags=["🗑️ Xóa Dữ Liệu"]
)
def delete_image(
    input: DeleteImageInput = Depends(DeleteImageInput.as_form)
):
    result = delete_image_service(input)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

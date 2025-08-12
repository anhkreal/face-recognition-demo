from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from Depend.depend import EditEmbeddingInput
from service.edit_embedding_service import edit_embedding_service

edit_embedding_router = APIRouter()

@edit_embedding_router.post(
    '/edit_embedding',
    summary="Chỉnh sửa thông tin khuôn mặt",
    description="""
    **Cập nhật thông tin khuôn mặt và ảnh trong hệ thống**
    
    API này cho phép:
    - Cập nhật ảnh khuôn mặt cho image_id đã tồn tại
    - Thay đổi đường dẫn ảnh (image_path)
    - Tự động cập nhật đặc trưng khuôn mặt nếu có ảnh mới
    - Đồng bộ thông tin trong chỉ mục tìm kiếm
    
    **Cách sử dụng:**
    - image_id: Bắt buộc, phải tồn tại trong hệ thống
    - image_path: Tùy chọn, đường dẫn mới cho ảnh
    - file: Tùy chọn, ảnh mới để thay thế
    
    **Lưu ý:**
    - Phải cung cấp ít nhất image_id
    - Nếu có ảnh mới, phải chứa đúng 1 khuôn mặt rõ ràng
    - Hỗ trợ định dạng: JPG, PNG, WEBP
    - Kích thước file tối đa: 10MB
    """,
    response_description="Kết quả cập nhật thông tin khuôn mặt",
    tags=["👥 Quản Lý Dữ Liệu"]
)
def edit_embedding(
    input: EditEmbeddingInput = Depends(EditEmbeddingInput.as_form),
    file: UploadFile = File(
        None, 
        description="File ảnh mới để thay thế (tùy chọn - JPG, PNG, WEBP)",
        media_type="image/*"
    )
):
    result = edit_embedding_service(input, file)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

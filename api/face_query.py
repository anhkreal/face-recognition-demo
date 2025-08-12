from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import time



from service.face_query_service import query_face_service as face_query_service

router = APIRouter()

@router.post(
    '/query',
    summary="Nhận diện khuôn mặt",
    description="""
    **Nhận diện khuôn mặt từ ảnh tải lên**
    
    API này sẽ:
    - Nhận ảnh chứa khuôn mặt từ người dùng
    - Trích xuất đặc trưng khuôn mặt từ ảnh
    - Tìm kiếm khuôn mặt tương tự trong cơ sở dữ liệu
    - Trả về thông tin chi tiết của người được nhận diện
    
    **Lưu ý:**
    - Ảnh phải chứa ít nhất 1 khuôn mặt rõ ràng
    - Hỗ trợ các định dạng: JPG, PNG, WEBP
    - Kích thước file tối đa: 10MB
    """,
    response_description="Kết quả nhận diện khuôn mặt với thông tin chi tiết",
    tags=["👤 Nhận Diện Khuôn Mặt"]
)
async def query_face(
    image: UploadFile = File(
        ..., 
        description="File ảnh chứa khuôn mặt cần nhận diện (JPG, PNG, WEBP)",
        media_type="image/*"
    )
):
    result = await face_query_service(image)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

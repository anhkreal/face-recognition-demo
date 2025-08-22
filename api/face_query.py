from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import time
from service.face_query_service import query_face_service as face_query_service
from service.add_embedding_simple_service import simple_add_embedding_service
from service.anti_spoofing_service import spoof_detection_service

router = APIRouter()

@router.post(
    '/query',
    summary="Nhận diện khuôn mặt với Auto-Add",
    description="""
    **Nhận diện khuôn mặt từ ảnh tải lên với tính năng tự động thêm mới**
    
    API này sẽ:
    - Nhận ảnh chứa khuôn mặt từ người dùng
    - Trích xuất đặc trưng khuôn mặt từ ảnh
    - Tìm kiếm khuôn mặt tương tự trong cơ sở dữ liệu
    - **🚀 TỰ ĐỘNG THÊM MỚI**: Nếu không tìm thấy (score < 0.5), tự động gọi API `/add_embedding_simple` để thêm người mới
    - Trả về thông tin chi tiết của người được nhận diện hoặc thông tin người vừa được thêm
    
    **Tính năng mới:**
    - 🔍 **Tìm kiếm trước**: Kiểm tra xem có người phù hợp không
    - ➕ **Tự động thêm**: Nếu không tìm thấy, tự động tạo profile mới với AI prediction
    - 📊 **Thống kê**: Cho biết đây là kết quả tìm kiếm hay người mới được thêm
    
    **Lưu ý:**
    - Ảnh phải chứa ít nhất 1 khuôn mặt rõ ràng
    - Hỗ trợ các định dạng: JPG, PNG, WEBP
    - Kích thước file tối đa: 10MB
    - Threshold nhận diện: 0.5 (có thể điều chỉnh)
    """,
    response_description="Kết quả nhận diện khuôn mặt hoặc thông tin người mới được thêm tự động",
    tags=["👤 Nhận Diện Khuôn Mặt"]
)
async def query_face(
    image: UploadFile = File(
        ..., 
        description="File ảnh chứa khuôn mặt cần nhận diện (JPG, PNG, WEBP)",
        media_type="image/*"
    )
):
    """
    🔍 Nhận diện khuôn mặt với tính năng auto-add
    
    1. Kiểm tra ảnh giả mạo
    2. Nếu là ảnh thật, tiến hành tìm kiếm
    3. Nếu không tìm thấy, tự động thêm mới
    4. Trả về kết quả tương ứng
    """
    # Bước 1: Kiểm tra chống giả mạo
    await image.seek(0)
    spoof_check = await spoof_detection_service.check_spoof(image)
    
    if not spoof_check["is_real"]:
        return JSONResponse(
            content={
                "action": "spoof_detected"
            },
            status_code=spoof_check.get("status_code", 400)
        )

    # Reset file pointer để đọc lại ảnh
    await image.seek(0)
    
    # Bước 2: Thực hiện query face bình thường
    result = await face_query_service(image)
    
    # Bước 3: Kiểm tra kết quả
    if result and not result.get("error"):
        # Có kết quả tìm thấy - chỉ trả về thông tin cơ bản
        basic_result = {
            "action": "face_recognized",
            "message": f"Đã nhận diện thành công với score: {result.get('score', 'N/A')}",
            "class_id": result.get("class_id"),
            "image_id": result.get("image_id"),
            "score": result.get("score")
        }
        
        # Thêm thông tin người nếu có
        if result.get("nguoi"):
            nguoi_info = result["nguoi"]
            basic_result.update({
                "ten": nguoi_info.get("ten"),
                "tuoi": nguoi_info.get("tuoi"),
                "gioitinh": nguoi_info.get("gioitinh")
            })
            
        result = basic_result
        status_code = 200
    else:
        # Không tìm thấy hoặc có lỗi, thực hiện auto-add
        print("🚀 Không tìm thấy kết quả phù hợp, đang thực hiện auto-add...")
        
        # Reset file pointer để có thể đọc lại
        await image.seek(0)
        
        # Gọi service add_embedding_simple
        add_result = await simple_add_embedding_service(image)
        
        if add_result.get("status_code") and add_result["status_code"] != 200:
            # Có lỗi khi thêm mới
            result = {
                "action": "auto_add_failed", 
                "error": f"Không tìm thấy kết quả và thêm mới thất bại: {add_result.get('message', 'Unknown error')}"
            }
            status_code = add_result.get("status_code", 500)
        else:
            # Thêm mới thành công - chỉ trả về thông tin cơ bản
            nguoi_info = add_result.get("nguoi_info", {})
            result = {
                "action": "auto_added",
                "message": "Không tìm thấy kết quả phù hợp, đã tự động thêm người mới vào hệ thống",
                "class_id": add_result.get("class_id"),
                "image_id": add_result.get("image_id"),
                "ten": nguoi_info.get("ten"),
                "tuoi": nguoi_info.get("tuoi"),
                "gioitinh": nguoi_info.get("gioitinh"),
                "predict_used": add_result.get("predict_used", False)
            }
            status_code = 200
    
    # Loại bỏ status_code khỏi response body
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    
    return JSONResponse(content=result, status_code=status_code)

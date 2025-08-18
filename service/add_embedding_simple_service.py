from fastapi import APIRouter, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from service.shared_instances import get_extractor, get_faiss_manager, get_faiss_lock
from db.nguoi_repository import NguoiRepository
from db.models import Nguoi
from Depend.depend import AddEmbeddingInput, SimpleAddEmbeddingInput
from service.predict_service import predict_service

add_router = APIRouter() 

# ✅ Sử dụng shared instances
extractor = get_extractor()
faiss_manager = get_faiss_manager()
faiss_lock = get_faiss_lock()
nguoi_repo = NguoiRepository()

async def simple_add_embedding_service(file: UploadFile = File(...)):
    """
    Simplified service - chỉ cần file upload, tất cả thông tin khác tự động generate
    """
    # Tạo SimpleAddEmbeddingInput với tất cả giá trị None
    input = SimpleAddEmbeddingInput(
        image_id=None,
        image_path=None,
        class_id=None,
        ten=None,
        gioitinh=None,
        tuoi=None,
        noio=None
    )
    
    # Sử dụng lại logic từ add_embedding_service
    return await add_embedding_service(input, file)

async def add_embedding_service(
    # image_id: int = Form(...),
    # image_path: str = Form(...),
    # class_id: int = Form(...),
    # ten: str = Form(...),
    # gioitinh: str = Form(...),
    # tuoi: int = Form(...),
    # noio: str = Form(...),
    input: SimpleAddEmbeddingInput = Depends(SimpleAddEmbeddingInput.as_form),
    file: UploadFile = File(...)
):
    # ✅ Kiểm tra kết nối FAISS - không load lại
    with faiss_lock:
        try:
            _ = faiss_manager.image_ids
        except Exception as e:
            return {"message": f"Không thể kết nối FAISS: {e}", "status_code": 500}
    
    # ✅ Xử lý thông tin thiếu cho FAISS
    import random
    import time
    
    # 1. Xử lý image_id nếu null hoặc không hợp lệ
    if input.image_id is None or input.image_id == 0:
        # Tạo random image_id không trùng với id cũ
        try:
            existing_image_ids = set(faiss_manager.image_ids)
            while True:
                # Tạo ID dựa trên timestamp + random để đảm bảo unique
                timestamp_part = int(time.time()) % 1000000  # 6 chữ số cuối của timestamp
                random_part = random.randint(1000, 9999)      # 4 chữ số random
                new_image_id = int(f"{timestamp_part}{random_part}")
                
                if new_image_id not in existing_image_ids:
                    input.image_id = new_image_id
                    break
        except Exception as e:
            return {"message": f"Lỗi tạo image_id: {e}", "status_code": 500}
    
    # 2. Xử lý image_path nếu rỗng
    if not input.image_path or input.image_path.strip() == "":
        input.image_path = f"image_{input.image_id}.jpg"
    
    # Kiểm tra tồn tại image_id hoặc image_path sau khi đã xử lý
    if str(input.image_id) in [str(id) for id in faiss_manager.image_ids]:
        return {"message": f"image_id {input.image_id} đã tồn tại!", "status_code": 400}
    if input.image_path in faiss_manager.image_paths:
        return {"message": f"image_path {input.image_path} đã tồn tại!", "status_code": 400}
    # Đọc ảnh từ file upload
    try:
        image_bytes = file.file.read()
        np_img = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    except Exception as e:
        return {"message": f"Lỗi đọc ảnh: {e}", "status_code": 400}
    # Tiền xử lý và trích xuất embedding
    try:
        embedding = extractor.extract(img)
    except Exception as e:
        return {"message": f"Lỗi trích xuất embedding: {e}", "status_code": 500}
    
    # ✅ Xử lý thông tin thiếu cho tuổi và giới tính bằng predict service
    predict_used = False
    if input.tuoi is None or input.tuoi == 0 or input.gioitinh is None:
        try:
            # Reset file pointer về đầu để predict service có thể đọc
            file.file.seek(0)
            
            # Gọi predict service để lấy tuổi và giới tính
            predict_result = await predict_service(file)
            
            if "error" not in predict_result:
                if input.tuoi is None or input.tuoi == 0:
                    input.tuoi = predict_result.get("pred_age", 25)
                    predict_used = True
                
                if input.gioitinh is None:
                    pred_gender = predict_result.get("pred_gender", "Male")
                    input.gioitinh = (pred_gender == "Male")  # True for Male, False for Female
                    predict_used = True
                    
                print(f"Predict service used: age={input.tuoi}, gender={'Nam' if input.gioitinh else 'Nữ'}")
            else:
                print(f"Predict service failed: {predict_result['error']}")
                # Sử dụng giá trị mặc định nếu predict fail
                if input.tuoi is None or input.tuoi == 0:
                    input.tuoi = 25
                if input.gioitinh is None:
                    input.gioitinh = True  # Default: Male
                    
        except Exception as e:
            print(f"Lỗi gọi predict service: {e}")
            # Sử dụng giá trị mặc định nếu có lỗi
            if input.tuoi is None or input.tuoi == 0:
                input.tuoi = 25
            if input.gioitinh is None:
                input.gioitinh = True  # Default: Male
    # Kiểm tra kết nối MySQL trước khi thêm vào FAISS
    try:
        nguoi_exist = nguoi_repo.get_by_class_id(input.class_id)
    except Exception as e:
        return {"message": f"Không thể kết nối MySQL: {e}", "status_code": 500}

    # ✅ Xử lý thông tin thiếu trước khi thêm vào database
    import random
    
    # 1. Xử lý class_id nếu null
    if input.class_id is None:
        # Tạo random id kiểu int không trùng với id cũ
        try:
            with nguoi_repo as cursor:
                # Lấy tất cả class_id hiện có
                cursor.execute("SELECT class_id FROM nguoi WHERE class_id REGEXP '^[0-9]+$'")
                existing_ids = {int(row['class_id']) for row in cursor.fetchall() if row['class_id'].isdigit()}
                
                # Tạo id ngẫu nhiên không trùng
                while True:
                    new_id = random.randint(100000, 999999)  # ID 6 chữ số
                    if new_id not in existing_ids:
                        input.class_id = str(new_id)
                        break
        except Exception as e:
            return {"message": f"Lỗi tạo class_id: {e}", "status_code": 500}
    
    # 2. Xử lý ten nếu rỗng hoặc null - tạo tên mặc định với class_id
    if not input.ten or input.ten.strip() == "":
        input.ten = f"Người lạ {input.class_id}"
    
    # 3. Xử lý noio nếu rỗng
    if not input.noio or input.noio.strip() == "":
        input.noio = "default"
    
    # ✅ Kiểm tra lại nguoi_exist sau khi đã xử lý class_id
    try:
        nguoi_exist = nguoi_repo.get_by_class_id(input.class_id)
    except Exception as e:
        return {"message": f"Lỗi kiểm tra người tồn tại: {e}", "status_code": 500}

    try:
        # ✅ Thread-safe FAISS operations
        with faiss_lock:
            faiss_manager.add_embeddings(
                np.array([embedding]),
                [input.image_id],
                [input.image_path],
                [input.class_id]
            )
            faiss_manager.save()
        
        if not nguoi_exist:
            gioitinh_str = "Nam" if input.gioitinh else "Nữ"
            nguoi = Nguoi(class_id=input.class_id, ten=input.ten, tuoi=input.tuoi, gioitinh=gioitinh_str, noio=input.noio)
            nguoi_repo.add(nguoi)
            print(f'Đã thêm embedding và thông tin người cho image_id={input.image_id}, class_id={input.class_id}')
            return {
                "message": f"Đã thêm embedding và thông tin người cho image_id={input.image_id}, class_id={input.class_id}",
                "class_id": input.class_id,
                "image_id": input.image_id,
                "image_path": input.image_path,
                "predict_used": predict_used,
                "nguoi_info": {
                    "ten": input.ten,
                    "tuoi": input.tuoi,
                    "gioitinh": gioitinh_str,
                    "noio": input.noio
                }
            }
        else:
            print(f'Đã thêm embedding cho image_id={input.image_id}, class_id={input.class_id} (class_id đã tồn tại trong bảng nguoi)')
            return {
                "message": f"Đã thêm embedding cho image_id={input.image_id}, class_id={input.class_id} (class_id đã tồn tại trong bảng nguoi)",
                "class_id": input.class_id,
                "image_id": input.image_id,
                "image_path": input.image_path,
                "predict_used": predict_used
            }
    except Exception as e:
        return {"message": f"Lỗi thêm embedding hoặc thông tin người: {e}", "status_code": 500}

# fe cần phải truyền về api toàn bộ trường, không được bỏ trống thông tin
# nếu như chỉ thêm ảnh (class_id đã tồn tại) --> điền dữ liệu rác
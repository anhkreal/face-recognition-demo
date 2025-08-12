from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import time


from service.shared_instances import get_extractor, get_faiss_manager, get_faiss_lock
from db.nguoi_repository import NguoiRepository


# ✅ Sử dụng shared instances thay vì tạo mới
extractor = get_extractor()
faiss_manager = get_faiss_manager()
faiss_lock = get_faiss_lock()
nguoi_repo = NguoiRepository()
print('✅ Shared instances initialized for face_query_service')

router = APIRouter()

async def query_face_service(file: UploadFile = File(...)):
    # ✅ Không load lại FAISS mỗi request - sử dụng thread-safe access
    print('--- Nhận request /query ---')
    start_total = time.time()
    
    image_bytes = await file.read()
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        print('Lỗi: Không decode được ảnh!')
        return {"error": "Lỗi: Không decode được ảnh!", "status_code": 400}
    
    emb = extractor.extract(image)
    
    # ✅ Thread-safe FAISS query
    with faiss_lock:
        results = faiss_manager.query(emb, topk=1)
    
    print(f'Results: {results}')
    print(f'Tổng thời gian xử lý: {time.time() - start_total:.3f}s')
    if results and results[0]['score'] > -0.5:
        print('Trả về thông tin top1')
        class_id = str(results[0]['class_id'])
        try:
            nguoi = nguoi_repo.get_by_class_id(class_id)
        except Exception as e:
            print(f"Lỗi truy vấn MySQL: {e}")
            nguoi = None
        resp = {
            'image_id': int(results[0]['image_id']),
            'image_path': str(results[0]['image_path']),
            'class_id': class_id,
            'score': float(results[0]['score'])
        }
        if nguoi:
            resp['nguoi'] = nguoi.to_dict()
        return resp
    else:
        print('Không có kết quả phù hợp (score <= 0.43)')
        return {}

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import time


from model.arcface_model import ArcFaceFeatureExtractor
from index.faiss import FaissIndexManager
from config import *
from db.nguoi_repository import NguoiRepository


extractor = ArcFaceFeatureExtractor(model_path=MODEL_PATH, device=None)
faiss_manager = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
nguoi_repo = NguoiRepository()
print('--- Bắt đầu load FAISS index và metadata ---')
faiss_manager.load()

router = APIRouter()

async def query_face_service(file: UploadFile = File(...)):
    faiss_manager.load()
    print('--- Nhận request /query ---')
    start_total = time.time()
    image_bytes = await file.read()
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        print('Lỗi: Không decode được ảnh!')
        return {"error": "Lỗi: Không decode được ảnh!", "status_code": 400}
    
    emb = extractor.extract(image)
    results = faiss_manager.query(emb, topk=1)
    print(f'Results: {results}')
    print(f'Tổng thời gian xử lý: {time.time() - start_total:.3f}s')
    if results and results[0]['score'] > 0.5:
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

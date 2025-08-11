from fastapi import APIRouter, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from index.faiss import FaissIndexManager
from config import *
from model.arcface_model import ArcFaceFeatureExtractor
from db.nguoi_repository import NguoiRepository
from db.models import Nguoi
from Depend.depend import AddEmbeddingInput
add_router = APIRouter() 

extractor = ArcFaceFeatureExtractor(model_path=MODEL_PATH, device=None)

faiss_manager = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
faiss_manager.load()
nguoi_repo = NguoiRepository()

def add_embedding_service(
    # image_id: int = Form(...),
    # image_path: str = Form(...),
    # class_id: int = Form(...),
    # ten: str = Form(...),
    # gioitinh: str = Form(...),
    # tuoi: int = Form(...),
    # noio: str = Form(...),
    input: AddEmbeddingInput = Depends(AddEmbeddingInput.as_form),
    file: UploadFile = File(...)
):
    # Kiểm tra kết nối FAISS
    try:
        faiss_manager.load()
        _ = faiss_manager.image_ids
    except Exception as e:
        return {"message": f"Không thể kết nối FAISS: {e}", "status_code": 500}
    print(f'--- Nhận request thêm embedding image_id={input.image_id}, class_id={input.class_id} ---')
    # Kiểm tra tồn tại image_id hoặc image_path
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
    # Kiểm tra kết nối MySQL trước khi thêm vào FAISS
    try:
        nguoi_exist = nguoi_repo.get_by_class_id(input.class_id)
    except Exception as e:
        return {"message": f"Không thể kết nối MySQL: {e}", "status_code": 500}

    try:
        faiss_manager.add_embeddings(
            np.array([embedding]),
            [input.image_id],
            [input.image_path],
            [input.class_id]
        )
        faiss_manager.save()
        faiss_manager.load()
        if not nguoi_exist:
            gioitinh_str = "Nam" if input.gioitinh else "Nữ"
            nguoi = Nguoi(class_id=input.class_id, ten=input.ten, tuoi=input.tuoi, gioitinh=gioitinh_str, noio=input.noio)
            nguoi_repo.add(nguoi)
            print(f'Đã thêm embedding và thông tin người cho image_id={input.image_id}, class_id={input.class_id}')
            return {"message": f"Đã thêm embedding và thông tin người cho image_id={input.image_id}, class_id={input.class_id}"}
        else:
            print(f'Đã thêm embedding cho image_id={input.image_id}, class_id={input.class_id} (class_id đã tồn tại trong bảng nguoi)')
            return {"message": f"Đã thêm embedding cho image_id={input.image_id}, class_id={input.class_id} (class_id đã tồn tại trong bảng nguoi)"}
    except Exception as e:
        return {"message": f"Lỗi thêm embedding hoặc thông tin người: {e}", "status_code": 500}

# fe cần phải truyền về api toàn bộ trường, không được bỏ trống thông tin
# nếu như chỉ thêm ảnh (class_id đã tồn tại) --> điền dữ liệu rác
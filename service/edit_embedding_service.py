import numpy as np
import cv2
from index.faiss import FaissIndexManager
from config import *
from model.arcface_model import ArcFaceFeatureExtractor
from db.nguoi_repository import NguoiRepository
from db.models import Nguoi

def edit_embedding_service(input, file):
    faiss_manager = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
    faiss_manager.load()
    nguoi_repo = NguoiRepository()
    # Kiểm tra tồn tại image_id
    if str(input.image_id) not in [str(id) for id in faiss_manager.image_ids]:
        return {"message": f"image_id {input.image_id} không tồn tại!", "status_code": 404}
    try:
        idxs = [i for i, img_id in enumerate(faiss_manager.image_ids) if str(img_id) == str(input.image_id)]
        if not idxs:
            return {"message": f"Không tìm thấy index cho image_id {input.image_id}", "status_code": 404}
        idx = idxs[0]
        updated_fields = []
        # In ra 10 chỉ số đầu tiên của embedding trước khi thay đổi
        print('Embedding cũ:', faiss_manager.embeddings[idx][:10])
        # Cập nhật embedding nếu file ảnh được gửi lên
        if file is not None and hasattr(file, 'file'):
            try:
                image_bytes = file.file.read()
                np_img = np.frombuffer(image_bytes, np.uint8)
                img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
                extractor = ArcFaceFeatureExtractor(model_path=MODEL_PATH, device=None)
                embedding = extractor.extract(img)
                faiss_manager.embeddings[idx] = embedding
                updated_fields.append('embedding')
                # In ra 10 chỉ số đầu tiên của embedding sau khi thay đổi
                print('Embedding mới:', embedding[:10])
            except Exception as e:
                return {"message": f"Lỗi trích xuất embedding: {e}", "status_code": 500}
        # Cập nhật image_path nếu truyền lên và không rỗng
        if hasattr(input, 'image_path') and input.image_path:
            faiss_manager.image_paths[idx] = input.image_path
            updated_fields.append('image_path')
        faiss_manager.save()
        # faiss_manager.load()
        if updated_fields:
            return {"message": f"Đã cập nhật: {', '.join(updated_fields)} cho image_id={input.image_id}"}
        else:
            return {"message": f"Không có trường nào được cập nhật cho image_id={input.image_id}"}
    except Exception as e:
        return {"message": f"Lỗi cập nhật embedding: {e}", "status_code": 500}

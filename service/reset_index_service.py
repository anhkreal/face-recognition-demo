from fastapi import APIRouter
from fastapi.responses import JSONResponse

from index.faiss import FaissIndexManager
from config import *
from db.nguoi_repository import NguoiRepository

reset_router = APIRouter()

faiss_manager = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
faiss_manager.load()
nguoi_repo = NguoiRepository()

def reset_index_api_service():
    # Kiểm tra kết nối FAISS
    try:
        faiss_manager.load()
        _ = faiss_manager.image_ids
    except Exception as e:
        return {"message": f"Không thể kết nối FAISS: {e}", "status_code": 500}
    # Kiểm tra kết nối MySQL
    try:
        nguoi_repo.get_total_and_examples(limit=1)
    except Exception as e:
        return {"message": f"Không thể kết nối MySQL: {e}", "status_code": 500}
    faiss_manager.reset_index()
    # Xóa toàn bộ dữ liệu bảng nguoi, giữ lại cấu trúc
    try:
        nguoi_repo.truncate_all()
        msg = "Đã xóa toàn bộ FAISS index, metadata và dữ liệu bảng nguoi."
    except Exception as e:
        msg = f"Đã xóa FAISS index, metadata. Lỗi khi xóa bảng nguoi: {e}"
    return {"message": msg}

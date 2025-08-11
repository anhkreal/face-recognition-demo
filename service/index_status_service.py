from fastapi import APIRouter
from fastapi.responses import JSONResponse

from index.faiss import FaissIndexManager
from config import *
from db.nguoi_repository import NguoiRepository

status_router = APIRouter()

faiss_manager = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
faiss_manager.load()
nguoi_repo = NguoiRepository()

def index_status_service():
    faiss_manager.load()
    result = faiss_manager.check_index_data()
    # Thêm thông tin bảng nguoi
    # Lấy tổng số người và ví dụ 5 người
    try:
        total, examples = nguoi_repo.get_total_and_examples(limit=5)
        result['nguoi_total'] = total
        result['nguoi_examples'] = examples
    except Exception:
        # Nếu không kết nối được MySQL thì chỉ trả về kết quả FAISS, không thêm trường nguoi_total và nguoi_examples
        pass
    return result

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from service.shared_instances import get_faiss_manager, get_faiss_lock
from service.performance_monitor import track_operation
from db.nguoi_repository import NguoiRepository

reset_router = APIRouter()

# ✅ Sử dụng shared instances
faiss_manager = get_faiss_manager()
faiss_lock = get_faiss_lock()
nguoi_repo = NguoiRepository()

@track_operation("reset_index")
def reset_index_api_service():
    # ✅ Thread-safe reset operation
    with faiss_lock:
        try:
            _ = faiss_manager.image_ids
        except Exception as e:
            return {"message": f"Không thể kết nối FAISS: {e}", "status_code": 500}
    # Kiểm tra kết nối MySQL
    try:
        nguoi_repo.get_total_and_examples(limit=1)
    except Exception as e:
        return {"message": f"Không thể kết nối MySQL: {e}", "status_code": 500}
    
    # ✅ Thread-safe reset operation
    with faiss_lock:
        faiss_manager.reset_index()
    
    # Xóa toàn bộ dữ liệu bảng nguoi, giữ lại cấu trúc
    try:
        nguoi_repo.truncate_all()
        msg = "Đã xóa toàn bộ FAISS index, metadata và dữ liệu bảng nguoi."
    except Exception as e:
        msg = f"Đã xóa FAISS index, metadata. Lỗi khi xóa bảng nguoi: {e}"
    return {"message": msg}

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from service.shared_instances import get_faiss_manager, get_faiss_lock
from service.performance_monitor import track_operation
from db.nguoi_repository import NguoiRepository

status_router = APIRouter()

# ✅ Sử dụng shared instances
faiss_manager = get_faiss_manager()
faiss_lock = get_faiss_lock()
nguoi_repo = NguoiRepository()

@track_operation("index_status")
def index_status_service():
    # ✅ Thread-safe status check - không load lại
    with faiss_lock:
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

# ===== PERFORMANCE API =====
# File: face_api/api/performance.py
# Mục đích: API endpoint để xem performance metrics

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from service.performance_monitor import get_performance_stats, get_performance_summary
from service.shared_instances import get_faiss_manager

performance_router = APIRouter()

@performance_router.get('/performance/stats')
def get_performance_stats_api():
    """Lấy thống kê chi tiết về hiệu suất"""
    stats = get_performance_stats()
    faiss_manager = get_faiss_manager()
    
    # Thêm thông tin FAISS
    faiss_info = {
        'total_vectors': len(faiss_manager.image_ids) if hasattr(faiss_manager, 'image_ids') else 0,
        'index_type': 'IndexFlatIP',
        'embedding_size': 512
    }
    
    return {
        'performance_stats': stats,
        'faiss_info': faiss_info,
        'summary': get_performance_summary()
    }

@performance_router.get('/performance/summary')
def get_performance_summary_api():
    """Lấy tóm tắt hiệu suất"""
    return {
        'summary': get_performance_summary(),
        'stats': get_performance_stats()
    }

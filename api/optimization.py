# ===== OPTIMIZATION API =====
# File: face_api/api/optimization.py
# Mục đích: API endpoints cho optimization và analysis

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from optimization.faiss_optimizer import get_faiss_optimizer
from service.performance_monitor import get_performance_stats, get_performance_summary
from service.shared_instances import get_faiss_manager

optimization_router = APIRouter()

@optimization_router.get('/optimization/analysis')
def get_optimization_analysis():
    """Phân tích tổng thể hiệu suất và đề xuất tối ưu hóa"""
    optimizer = get_faiss_optimizer()
    
    # Memory analysis
    memory_info = optimizer.memory_usage_analysis()
    
    # Performance stats
    perf_stats = get_performance_stats()
    
    # Recommendations
    recommendations = optimizer.recommend_optimizations()
    
    # FAISS info
    faiss_manager = get_faiss_manager()
    faiss_info = {
        'total_vectors': len(faiss_manager.image_ids) if hasattr(faiss_manager, 'image_ids') else 0,
        'index_type': type(faiss_manager.index).__name__ if hasattr(faiss_manager, 'index') else 'Unknown',
        'embedding_dimension': 512
    }
    
    return {
        'memory_analysis': memory_info,
        'performance_stats': perf_stats,
        'faiss_info': faiss_info,
        'recommendations': recommendations,
        'summary': get_performance_summary()
    }

@optimization_router.post('/optimization/optimize_index')
def optimize_index():
    """Tối ưu hóa FAISS index cho query speed"""
    try:
        optimizer = get_faiss_optimizer()
        optimizer.optimize_index_for_query_speed()
        
        return {
            'message': '✅ FAISS index đã được tối ưu hóa thành công',
            'status': 'optimized'
        }
    except Exception as e:
        return {
            'message': f'❌ Lỗi khi tối ưu hóa index: {e}',
            'status': 'error',
            'status_code': 500
        }

@optimization_router.get('/optimization/memory_usage')
def get_memory_usage():
    """Lấy thông tin sử dụng memory chi tiết"""
    optimizer = get_faiss_optimizer()
    memory_info = optimizer.memory_usage_analysis()
    
    return {
        'memory_usage': memory_info,
        'recommendations': optimizer.recommend_optimizations()
    }

@optimization_router.get('/optimization/recommendations')
def get_optimization_recommendations():
    """Lấy các đề xuất tối ưu hóa"""
    optimizer = get_faiss_optimizer()
    recommendations = optimizer.recommend_optimizations()
    
    return {
        'recommendations': recommendations,
        'total_recommendations': len(recommendations)
    }

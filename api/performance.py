# ===== PERFORMANCE API =====
# File: face_api/api/performance.py
# Mục đích: API endpoint để xem performance metrics

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from service.performance_monitor import get_performance_stats, get_performance_summary
from service.shared_instances import get_faiss_manager

performance_router = APIRouter()

@performance_router.get(
    '/performance/stats',
    summary="Thống kê hiệu suất chi tiết",
    description="""
    **Xem thống kê hiệu suất chi tiết của hệ thống nhận diện khuôn mặt**
    
    API này cung cấp:
    - Metrics hiệu suất chi tiết về CPU, RAM, thời gian phản hồi
    - Thông tin FAISS index (số vectors, loại index, kích thước embedding)
    - Thống kê số lượng request đã xử lý
    - Tỷ lệ thành công/thất bại của các operation
    - Tình trạng sử dụng tài nguyên hệ thống
    
    **Thông tin bao gồm:**
    - performance_stats: CPU usage, memory consumption, response times
    - faiss_info: Vector count, index type, embedding dimensions
    - request_metrics: Total requests, success rate, error rate
    - resource_usage: System resources utilization
    
    **Ứng dụng:**
    - Monitoring hiệu suất real-time
    - Phân tích bottleneck hệ thống
    - Capacity planning
    - Performance tuning
    - Troubleshooting vấn đề hiệu suất
    """,
    response_description="Thống kê hiệu suất chi tiết với metrics đầy đủ",
    tags=["🏥 Health Check"]
)
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

@performance_router.get(
    '/performance/summary',
    summary="Tóm tắt hiệu suất hệ thống",
    description="""
    **Xem tóm tắt hiệu suất tổng quan của hệ thống**
    
    API này cung cấp thông tin tóm tắt:
    - Tình trạng hiệu suất tổng quan
    - Metrics chính được tóm gọn
    - Trends hiệu suất theo thời gian
    - Alerts và warnings nếu có
    - Key performance indicators (KPIs)
    
    **Thông tin tóm tắt:**
    - overall_status: Tình trạng tổng quan (good/warning/critical)
    - key_metrics: Các chỉ số quan trọng nhất
    - trends: Xu hướng thay đổi hiệu suất
    - recommendations: Đề xuất tối ưu hóa (nếu có)
    
    **Phù hợp cho:**
    - Dashboard tổng quan
    - Quick health check
    - Management reporting
    - High-level monitoring
    - Status page hiển thị cho user
    """,
    response_description="Tóm tắt hiệu suất tổng quan của hệ thống",
    tags=["🏥 Health Check"]
)
def get_performance_summary_api():
    """Lấy tóm tắt hiệu suất"""
    return {
        'summary': get_performance_summary(),
        'stats': get_performance_stats()
    }

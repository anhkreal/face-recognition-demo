# ===== HEALTH CHECK API =====
# File: face_api/api/health.py
# Mục đích: Health check và system status APIs

import time
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from optimization.startup import get_server_health
from service.performance_monitor import get_performance_stats
from service.shared_instances import get_faiss_manager

health_router = APIRouter()

@health_router.get(
    '/health',
    summary="Kiểm tra sức khỏe hệ thống",
    description="""
    **Kiểm tra trạng thái cơ bản của hệ thống**
    
    API này cung cấp:
    - Trạng thái hoạt động của server
    - Thời gian phản hồi hệ thống
    - Tình trạng kết nối cơ bản
    - Thông tin uptime
    
    **Kết quả trả về:**
    - status: healthy/unhealthy
    - timestamp: Thời gian kiểm tra
    - uptime: Thời gian hoạt động
    - server_info: Thông tin cơ bản về server
    
    **Mục đích sử dụng:**
    - Monitoring hệ thống
    - Load balancer health check
    - Kiểm tra tình trạng trước khi gửi request
    - Debug kết nối
    """,
    response_description="Trạng thái sức khỏe cơ bản của hệ thống",
    responses={
        200: {"description": "Hệ thống hoạt động bình thường"},
        503: {"description": "Hệ thống gặp sự cố"}
    },
    tags=["🏥 Health Check"]
)
def health_check():
    """Basic health check endpoint"""
    health_status = get_server_health()
    
    # Determine HTTP status code
    status_code = 200 if health_status['status'] == 'healthy' else 503
    
    return JSONResponse(
        content=health_status,
        status_code=status_code
    )

@health_router.get(
    '/health/detailed',
    summary="Kiểm tra sức khỏe chi tiết",
    description="""
    **Kiểm tra trạng thái chi tiết và hiệu suất hệ thống**
    
    API này cung cấp thông tin toàn diện:
    - Tất cả thông tin từ health check cơ bản
    - Metrics hiệu suất chi tiết (CPU, RAM, response time)
    - Thông tin FAISS index (số vectors, loại index)
    - Trạng thái các service nội bộ
    - Statistics về số lượng request đã xử lý
    
    **Thông tin chi tiết bao gồm:**
    - performance_metrics: CPU, memory usage, avg response time
    - faiss_info: Tổng số vectors, loại index, trạng thái sẵn sàng
    - request_stats: Số lượng request đã xử lý, tỷ lệ thành công
    - system_resources: Tình trạng tài nguyên hệ thống
    
    **Ứng dụng:**
    - Monitoring hiệu suất chi tiết
    - Debugging khi có vấn đề
    - Capacity planning
    - Performance optimization
    """,
    response_description="Thông tin sức khỏe và hiệu suất chi tiết",
    responses={
        200: {"description": "Thông tin chi tiết hệ thống"},
        503: {"description": "Hệ thống gặp sự cố với thông tin chi tiết"}
    },
    tags=["🏥 Health Check"]
)
def detailed_health_check():
    """Detailed health check với performance metrics"""
    health_status = get_server_health()
    performance_stats = get_performance_stats()
    
    try:
        faiss_manager = get_faiss_manager()
        faiss_info = {
            'total_vectors': len(faiss_manager.image_ids) if hasattr(faiss_manager, 'image_ids') else 0,
            'index_type': type(faiss_manager.index).__name__ if hasattr(faiss_manager, 'index') else 'Unknown',
            'index_ready': hasattr(faiss_manager, 'index') and faiss_manager.index is not None
        }
    except Exception as e:
        faiss_info = {'error': str(e), 'index_ready': False}
    
    detailed_status = {
        **health_status,
        'performance_metrics': performance_stats,
        'faiss_info': faiss_info
    }
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    
    return JSONResponse(
        content=detailed_status,
        status_code=status_code
    )

@health_router.get('/health/readiness')
def readiness_check():
    """Readiness check cho Kubernetes/Docker"""
    health_status = get_server_health()
    
    # Kiểm tra các components cần thiết
    required_components = ['shared_instances', 'faiss_index', 'model_extractor']
    is_ready = all(health_status['components'].get(comp, False) for comp in required_components)
    
    readiness_status = {
        'ready': is_ready,
        'components': health_status['components'],
        'timestamp': health_status['timestamp']
    }
    
    status_code = 200 if is_ready else 503
    
    return JSONResponse(
        content=readiness_status,
        status_code=status_code
    )

@health_router.get('/health/liveness')
def liveness_check():
    """Liveness check cho Kubernetes/Docker"""
    try:
        # Basic liveness check - server có đang chạy không
        from service.shared_instances import get_faiss_manager
        faiss_manager = get_faiss_manager()
        
        liveness_status = {
            'alive': True,
            'timestamp': time.time()
        }
        
        return JSONResponse(content=liveness_status, status_code=200)
        
    except Exception as e:
        return JSONResponse(
            content={'alive': False, 'error': str(e)},
            status_code=503
        )

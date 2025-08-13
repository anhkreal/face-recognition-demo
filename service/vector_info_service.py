from fastapi import APIRouter
from fastapi.responses import JSONResponse
from service.shared_instances import get_faiss_manager, get_faiss_lock
from service.performance_monitor import track_operation

vector_info_router = APIRouter()

# ✅ Sử dụng shared instances
faiss_manager = get_faiss_manager()
faiss_lock = get_faiss_lock()

@track_operation("vector_info")
def get_vector_info_service():
    # ✅ Thread-safe vector info query - không load lại
    
    with faiss_lock:
        n = 10
        total = len(faiss_manager.image_ids)
        if total == 0:
            return {"message": "Không có vector nào trong FAISS index.", "status_code": 404}
        
        # Lấy 10 vector đầu
        first_vectors = []
        for i in range(min(n, total)):
            first_vectors.append({
                'faiss_index': int(i),
                'image_id': int(faiss_manager.image_ids[i]),
                'image_path': str(faiss_manager.image_paths[i]),
                'class_id': int(faiss_manager.class_ids[i]),
                # 'embedding': faiss_manager.embeddings[i]
            })
        
        # Lấy 10 vector cuối
        last_vectors = []
        for i in range(max(0, total-n), total):
            last_vectors.append({
            'faiss_index': int(i),
            'image_id': int(faiss_manager.image_ids[i]),
            'image_path': str(faiss_manager.image_paths[i]),
            'class_id': int(faiss_manager.class_ids[i]),
            # 'embedding': faiss_manager.embeddings[i]
        })
    faiss_manager.check_index_data()
    return {
        "first_vectors": first_vectors,
        "last_vectors": last_vectors,
        "total": total
    }
    

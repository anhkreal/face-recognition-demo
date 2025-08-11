from fastapi import APIRouter
from fastapi.responses import JSONResponse
from index.faiss import FaissIndexManager
from config import *

vector_info_router = APIRouter()
faiss_manager = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
faiss_manager.load()

def get_vector_info_service():
    faiss_manager.load()
    print('--- Nhận request truy vấn 10 vector đầu và 10 vector cuối ---')
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
    

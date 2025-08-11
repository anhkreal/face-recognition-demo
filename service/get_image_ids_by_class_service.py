from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from index.faiss import FaissIndexManager
from config import *
from db.nguoi_repository import NguoiRepository

get_image_ids_by_class_router = APIRouter()

faiss_manager = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
faiss_manager.load()
nguoi_repo = NguoiRepository()

def get_image_ids_by_class_api_service(class_id: str = Query(..., description="Class ID cần truy vấn")):
    faiss_manager.load()
    image_ids = faiss_manager.get_image_ids_by_class(class_id)
    nguoi = None
    try:
        nguoi = nguoi_repo.get_by_class_id(int(class_id))
    except Exception:
        pass
    return {
        'class_id': class_id,
        'image_ids': image_ids,
        'count': len(image_ids),
        'nguoi': nguoi.to_dict() if nguoi else None
    }

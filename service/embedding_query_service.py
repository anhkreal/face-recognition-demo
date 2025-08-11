from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from index.faiss import FaissIndexManager
from config import FAISS_INDEX_PATH, FAISS_META_PATH

# Khởi tạo instance toàn cục
faiss_manager = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
faiss_manager.load()

router = APIRouter()

@router.get('/search_embeddings')
def search_embeddings_api(
    query: str = Query('', description='Chuỗi tìm kiếm (image_id, image_path, class_id)'),
    page: int = Query(1, ge=1, description='Số trang (bắt đầu từ 1)'),
    page_size: int = Query(15, ge=1, le=15, description='Số kết quả mỗi trang')
):
    faiss_manager.load()
    result = faiss_manager.query_embeddings_by_string(query, page, page_size)
    return result

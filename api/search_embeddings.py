from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from service.embedding_query_service import search_embeddings_api

embedding_search_router = APIRouter()

@embedding_search_router.get('/search_embeddings')
def search_embeddings_api_route(
    query: str = Query('', description='Chuỗi tìm kiếm (image_id, image_path, class_id)'),
    page: int = Query(1, ge=1, description='Số trang (bắt đầu từ 1)'),
    page_size: int = Query(15, ge=1, le=15, description='Số kết quả mỗi trang')
):
    result = search_embeddings_api(query, page, page_size)
    # Convert numpy types to native Python types for JSON serialization
    import numpy as np
    def convert(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [convert(v) for v in obj]
        return obj
    result = convert(result)
    return JSONResponse(content=result)

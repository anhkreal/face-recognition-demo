from fastapi import APIRouter, Query, Form, Depends
from fastapi.responses import JSONResponse
import numpy as np

from index.faiss import FaissIndexManager
from config import *
from db.nguoi_repository import NguoiRepository
from Depend.depend import DeleteClassInput

delete_class_router = APIRouter()

faiss_manager = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
faiss_manager.load()
nguoi_repo = NguoiRepository()

def delete_class_service(
    # class_id: int = Form(...)
    input: DeleteClassInput = Depends(DeleteClassInput.as_form)
                 ):
    # Kiểm tra kết nối FAISS
    try:
        faiss_manager.load()
        _ = faiss_manager.class_ids
    except Exception as e:
        return {"message": f"Không thể kết nối FAISS: {e}", "status_code": 500}
    # Kiểm tra kết nối MySQL
    try:
        _ = nguoi_repo
        # Thử truy vấn đơn giản để kiểm tra kết nối
        nguoi_repo.get_total_and_examples(limit=1)
    except Exception as e:
        return {"message": f"Không thể kết nối MySQL: {e}", "status_code": 500}
    print(f'--- Nhận request xoá class_id={input.class_id} ---')
    # Kiểm tra embedding của image-id 289 trước khi xóa
    # image_id_check = 289
    # try:
    #     emb_before = faiss_manager.index.reconstruct(image_id_check)
    #     print(f'Embedding của image-id={image_id_check} trước khi xóa: {emb_before[:10]} ...')
    # except Exception as e:
    #     print(f'Không reconstruct được embedding image-id={image_id_check} trước khi xóa: {e}')

    # Kiểm tra class_id có tồn tại trong metadata không
    class_ids_set = set([int(cid) for cid in faiss_manager.class_ids])
    if int(input.class_id) not in class_ids_set:
        print(f'class_id={input.class_id} không tồn tại trong không gian embedding.')
        return {"message": f"class_id={input.class_id} không tồn tại trong không gian embedding.", "status_code": 404}
    # Lấy các image_id cần xóa
    idx_to_delete = [int(faiss_manager.image_ids[i]) for i, cid in enumerate(faiss_manager.class_ids) if int(cid) == int(input.class_id)]
    if not idx_to_delete:
        print(f'Không tìm thấy vector với class_id={input.class_id}')
    success = faiss_manager.delete_by_class_id(input.class_id)
    if success:
        faiss_manager.save()
        faiss_manager.load()
        # Xóa trường người có class_id tương ứng trong bảng nguoi
        nguoi_repo.delete_by_class_id(input.class_id)
        return {
            'class_id': input.class_id,
            'status': 'deleted',
            'message': f'Đã xóa toàn bộ ảnh với class_id={input.class_id} và rebuild index. Đã xóa luôn người trong bảng nguoi.'
        }
    else:
        return {
            'class_id': input.class_id,
            'status': 'not_found',
            'message': f'class_id {input.class_id} không tồn tại!'
            , "status_code": 404
        }
    
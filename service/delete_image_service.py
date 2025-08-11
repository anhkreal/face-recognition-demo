from fastapi import APIRouter, Form, Depends
from fastapi.responses import JSONResponse

from index.faiss import FaissIndexManager
from config import *
from db.nguoi_repository import NguoiRepository
from Depend.depend import DeleteImageInput

delete_image_router = APIRouter()

faiss_manager = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
faiss_manager.load()
nguoi_repo = NguoiRepository()

def delete_image_service(
    # image_id: int = Form(...)
    input: DeleteImageInput = Depends(DeleteImageInput.as_form)
    ):
    # Kiểm tra kết nối FAISS
    try:
        faiss_manager.load()
        _ = faiss_manager.image_ids
    except Exception as e:
        return {"message": f"Không thể kết nối FAISS: {e}", "status_code": 500}
    # Kiểm tra kết nối MySQL
    try:
        _ = nguoi_repo
        nguoi_repo.get_total_and_examples(limit=1)
    except Exception as e:
        return {"message": f"Không thể kết nối MySQL: {e}", "status_code": 500}
    print(f'--- Nhận request xóa embedding image_id={input.image_id} ---')
    try:
        # Lấy class_id trước khi xóa
        idxs = [i for i, img_id in enumerate(faiss_manager.image_ids) if str(img_id) == str(input.image_id)]
        class_id = None
        if idxs:
            class_id = int(faiss_manager.class_ids[idxs[0]])
        result = faiss_manager.delete_by_image_id(input.image_id)
        faiss_manager.save()
        faiss_manager.load()
        if result:
            # Kiểm tra còn ảnh nào thuộc class_id không
            if class_id is not None:
                ids_left = faiss_manager.get_image_ids_by_class(class_id)
                if not ids_left:
                    nguoi_repo.delete_by_class_id(class_id)
                    return {"message": f"Đã xóa embedding cho image_id={input.image_id} và xóa luôn người class_id={class_id} vì không còn ảnh nào."}
            return {"message": f"Đã xóa embedding cho image_id={input.image_id}"}
        else:
            return {"message": f"image_id {input.image_id} không tồn tại!", "status_code": 404}
    except Exception as e:
        return {"message": f"Lỗi xóa embedding: {e}", "status_code": 500}

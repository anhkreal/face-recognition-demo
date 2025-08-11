from fastapi import APIRouter, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from service.add_embedding_service import add_embedding_service
from Depend.depend import AddEmbeddingInput
add_router = APIRouter()

@add_router.post('/add_embedding')
def add_embedding(
    input: AddEmbeddingInput = Depends(AddEmbeddingInput.as_form),
    file: UploadFile = File(...)
):
    result = add_embedding_service(input, file)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

# fe cần phải truyền về api toàn bộ trường, không được bỏ trống thông tin
# nếu như chỉ thêm ảnh (class_id đã tồn tại) --> điền dữ liệu rác
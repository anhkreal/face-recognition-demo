from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from Depend.depend import EditEmbeddingInput
from service.edit_embedding_service import edit_embedding_service

edit_embedding_router = APIRouter()

@edit_embedding_router.post('/edit_embedding')
def edit_embedding(
    input: EditEmbeddingInput = Depends(EditEmbeddingInput.as_form),
    file: UploadFile = File(None)
):
    result = edit_embedding_service(input, file)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

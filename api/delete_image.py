from fastapi import APIRouter, Form, Depends
from fastapi.responses import JSONResponse

from service.delete_image_service import delete_image_service
from Depend.depend import DeleteImageInput

delete_image_router = APIRouter()



@delete_image_router.post('/delete_image')
def delete_image(
    input: DeleteImageInput = Depends(DeleteImageInput.as_form)
    ):
    result = delete_image_service(input)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

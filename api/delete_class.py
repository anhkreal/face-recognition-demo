from fastapi import APIRouter, Query, Form, Depends
from fastapi.responses import JSONResponse
import numpy as np

from service.delete_class_service import delete_class_service
from Depend.depend import DeleteClassInput

delete_class_router = APIRouter()



@delete_class_router.post('/delete_class')
def delete_class(
    input: DeleteClassInput = Depends(DeleteClassInput.as_form)
                 ):
    result = delete_class_service(input)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)
    
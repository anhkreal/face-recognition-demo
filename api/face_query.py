from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import time



from service.face_query_service import query_face_service as face_query_service

router = APIRouter()

@router.post('/query')
async def query_face(image: UploadFile = File(...)):
    result = await face_query_service(image)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import time


from service.face_query_top5_service import query_face_top5_service as face_query_top5_service

face_query_top5_router = APIRouter()

@face_query_top5_router.post('/query_top5')
async def query_face_top5(file: UploadFile = File(...)):
    result = await face_query_top5_service(file)
    status_code = result.get("status_code", 200)
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    return JSONResponse(content=result, status_code=status_code)

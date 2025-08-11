from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.face_query import router as face_query_router
from api.delete_class import delete_class_router
from api.add_embedding import add_router
from api.delete_image import delete_image_router
from api.vector_info import vector_info_router
from api.get_image_ids_by_class import get_image_ids_by_class_router
from api.index_status import status_router
from api.reset_index import reset_router
from api.face_query_top5 import face_query_top5_router
from api.edit_embedding import edit_embedding_router
from api.list_nguoi import list_nguoi_router
from api.register import register_router
from api.login import login_router
from api.search_embeddings import embedding_search_router
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(face_query_router)
app.include_router(delete_class_router)
app.include_router(add_router)
app.include_router(delete_image_router)
app.include_router(vector_info_router)
app.include_router(get_image_ids_by_class_router)
app.include_router(status_router)
app.include_router(reset_router)
app.include_router(face_query_top5_router)
app.include_router(edit_embedding_router)
app.include_router(list_nguoi_router)
app.include_router(register_router) 
app.include_router(login_router)
app.include_router(embedding_search_router)
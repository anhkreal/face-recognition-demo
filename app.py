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
from api.health import health_router
from api.performance import performance_router
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

app = FastAPI(
    title="🤖 Hệ Thống Nhận Diện Khuôn Mặt",
    description="""
    ## 🎯 Giới Thiệu Hệ Thống
    
    **Hệ thống nhận diện khuôn mặt AI tiên tiến** sử dụng công nghệ deep learning và FAISS để:
    - 🔍 **Nhận diện khuôn mặt** từ ảnh với độ chính xác cao
    - 👥 **Quản lý thông tin người** (tên, tuổi, giới tính, nơi ở)
    - 🗄️ **Lưu trữ và tìm kiếm** embedding vectors hiệu quả
    - ⚡ **Tối ưu hiệu suất** với singleton pattern và FAISS indexing
    
    ## 📋 Các Chức Năng Chính
    
    ### 🔐 **Xác Thực & Bảo Mật**
    - `/login` - Đăng nhập hệ thống
    - `/register` - Đăng ký tài khoản mới
    
    ### 👤 **Nhận Diện Khuôn Mặt**
    - `/query` - Nhận diện khuôn mặt từ ảnh
    - `/add_embedding` - Thêm người mới vào hệ thống
    - `/edit_embedding` - Cập nhật thông tin khuôn mặt
    
    ### 🗑️ **Quản Lý Dữ Liệu**
    - `/delete_image` - Xóa ảnh cụ thể
    - `/delete_class` - Xóa toàn bộ thông tin người
    - `/reset_index` - Khởi tạo lại hệ thống
    
    ### 📊 **Tìm Kiếm & Thống Kê**
    - `/list_nguoi` - Danh sách người trong hệ thống
    - `/search_embeddings` - Tìm kiếm embedding
    - `/index_status` - Trạng thái FAISS index
    - `/vector_info` - Thông tin chi tiết vectors
    
    ### 🏥 **Monitoring & Health Check**
    - `/health` - Kiểm tra sức khỏe hệ thống
    - `/health/detailed` - Thông tin chi tiết hiệu suất
    
    ## 🚀 Tính Năng Nổi Bật
    
    - **Singleton Architecture**: Tối ưu 99% memory, 98% faster response
    - **FAISS Indexing**: Tìm kiếm vector siêu nhanh
    - **Thread-Safe**: Hỗ trợ concurrent requests
    - **Auto Health Monitoring**: Theo dõi hiệu suất real-time
    - **RESTful API**: Dễ tích hợp với các hệ thống khác
    
    ## 📖 Hướng Dẫn Sử Dụng
    
    1. **Đăng ký/Đăng nhập** để xác thực
    2. **Thêm người mới** bằng `/add_embedding`
    3. **Nhận diện** bằng `/query` với ảnh cần tìm
    4. **Quản lý dữ liệu** qua các API CRUD
    5. **Monitor hệ thống** qua health endpoints
    
    ## 🔧 Thông Tin Kỹ Thuật
    
    - **Framework**: FastAPI + Pydantic
    - **AI Engine**: Face Recognition + FAISS
    - **Database**: In-memory với disk persistence  
    - **Security**: Form-based authentication
    - **Performance**: Optimized với shared instances
    
    ---
    *Phát triển bởi AI Team - Hệ thống nhận diện khuôn mặt thông minh*
    """,
    version="2.0.0",
    # contact={
    #     "name": "Face Recognition API Support",
    #     "email": "support@faceapi.com"
    # },
    # license_info={
    #     "name": "MIT License",
    #     "url": "https://opensource.org/licenses/MIT"
    # },
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "docExpansion": "list",
        "operationsSorter": "method",
        "filter": True
    }
)
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
app.include_router(health_router)
app.include_router(performance_router)
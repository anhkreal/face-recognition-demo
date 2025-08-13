import os
import time
from fastapi import FastAPI, Request
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
from api.search_embeddings import embedding_search_router
from api.health import health_router
# Optional performance monitoring
try:
    from api.performance import performance_router
    PERFORMANCE_AVAILABLE = True
except ImportError:
    PERFORMANCE_AVAILABLE = False
    print("⚠️ Performance monitoring not available")

# MySQL Authentication
from auth.mysql_auth_api import router as mysql_auth_router

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

app = FastAPI(
    title="🤖 Hệ Thống Nhận Diện Khuôn Mặt với MySQL Authentication",
    description="""
    ## 🎯 Giới Thiệu Hệ Thống
    
    **Hệ thống nhận diện khuôn mặt AI tiên tiến** sử dụng công nghệ deep learning và FAISS để:
    
    ### 🚀 Tính Năng Chính
    - **🔍 Tìm kiếm khuôn mặt**: Tìm người giống nhất từ database
    - **➕ Quản lý dữ liệu**: Thêm, sửa, xóa thông tin người dùng
    - **📊 Thống kê**: Xem thông tin database và hiệu suất
    - **🔐 Bảo mật**: Đăng nhập MySQL để bảo vệ các thao tác nhạy cảm
    
    ### 🔐 Hệ Thống Authentication
    **MySQL Database Authentication:**
    - 🏠 **Public APIs**: Tìm kiếm khuôn mặt, xem thông tin (không cần đăng nhập)
    - 🔒 **Protected APIs**: Thêm, sửa, xóa dữ liệu (yêu cầu đăng nhập MySQL)
    
    ### 🛡️ Authentication & Authorization
    
    **MySQL Token Authentication:**
    - Sử dụng `/auth/login` để đăng nhập với username/password từ bảng `taikhoan`
    - Nhận session token để sử dụng cho protected APIs
    - Token được validate qua MySQL database
    - Logout với `/auth/logout` để clear session
    
    **Security Model:**
    - 🟢 **Public**: Query, search, health check (không cần đăng nhập)
    - 🔒 **Protected**: Add, edit, delete (cần đăng nhập qua bảng taikhoan MySQL)
    
    **Yêu Cầu Authentication:**
    Đảm bảo phải đăng nhập thông qua bảng taikhoan MySQL mới được các tác vụ thêm/sửa/xóa MySQL/FAISS, còn truy vấn khỏi cần
    
    ### 📝 Hướng Dẫn Sử Dụng
    1. **Tìm kiếm khuôn mặt**: Dùng `/query` với ảnh upload
    2. **Đăng nhập**: POST `/auth/login` với username/password MySQL
    3. **Quản lý dữ liệu**: Sau khi đăng nhập, có thể add/edit/delete
    4. **Đăng xuất**: POST `/auth/logout` để kết thúc session
    
    ### 🛠️ Công Nghệ Sử Dụng
    - **AI Framework**: ArcFace, FAISS Vector Search
    - **Backend**: FastAPI, Python
    - **Database**: MySQL Authentication
    - **Security**: Session-based Authentication với Bearer tokens
    """,
    version="2.0.0",
    contact={
        "name": "Face Recognition API Support",
        "email": "support@faceapi.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên chỉ định cụ thể
    allow_credentials=False,  # False cho token-based auth
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers Middleware
@app.middleware("http")
async def security_headers(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Check if this is a Swagger/docs request
    is_docs_request = any(path in str(request.url) for path in ["/docs", "/redoc", "/openapi.json"])
    
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # More permissive CSP for Swagger UI
    if is_docs_request:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self' https:; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com https://cdn.jsdelivr.net; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'"
        )
    else:
        # Stricter CSP for API endpoints
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'"
        )
    
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Performance Monitoring Middleware
@app.middleware("http")
async def performance_monitoring(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    
    # Log request performance (without sensitive data)
    if not any(path in str(request.url) for path in ["/docs", "/redoc", "/openapi.json"]):
        process_time = time.time() - start_time
        print(f"📊 {request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
    
    return response

# 🔐 MySQL Authentication APIs
app.include_router(mysql_auth_router)

print("🚀 Khởi tạo Face Recognition System thành công!")
print("🔐 MySQL Authentication system đã được tích hợp!")
print("📊 Security middleware và logging đã được kích hoạt!")

# 🏠 Public APIs (không cần authentication)
app.include_router(face_query_router, tags=["🔍 Tìm Kiếm Khuôn Mặt"])
app.include_router(face_query_top5_router, tags=["🔍 Tìm Kiếm Khuôn Mặt"])
app.include_router(vector_info_router, tags=["📊 Thông Tin Hệ Thống"])
app.include_router(get_image_ids_by_class_router, tags=["📊 Thông Tin Hệ Thống"])
app.include_router(status_router, tags=["📊 Thông Tin Hệ Thống"])
app.include_router(list_nguoi_router, tags=["👥 Danh Sách Người"])
app.include_router(embedding_search_router, tags=["🔍 Tìm Kiếm Khuôn Mặt"])
app.include_router(health_router, tags=["🏥 Kiểm Tra Sức Khỏe"])

# Optional: Performance monitoring if available
if PERFORMANCE_AVAILABLE:
    app.include_router(performance_router, tags=["⚡ Hiệu Suất"])

# 🔒 Protected APIs (cần MySQL authentication)
app.include_router(add_router, tags=["🔒 Quản Lý Dữ Liệu (Protected)"])
app.include_router(edit_embedding_router, tags=["🔒 Quản Lý Dữ Liệu (Protected)"])
app.include_router(delete_class_router, tags=["🔒 Quản Lý Dữ Liệu (Protected)"])
app.include_router(delete_image_router, tags=["🔒 Quản Lý Dữ Liệu (Protected)"])
app.include_router(reset_router, tags=["🔒 Quản Lý Dữ Liệu (Protected)"])

@app.get("/", tags=["🏠 Trang Chủ"])
def read_root():
    """
    ## 🏠 Trang Chủ API
    
    Chào mừng đến với **Hệ Thống Nhận Diện Khuôn Mặt**!
    
    ### 🚀 Bắt Đầu Nhanh
    1. **Tìm kiếm**: Thử `/query` để tìm khuôn mặt
    2. **Đăng nhập**: Dùng `/auth/login` với MySQL account
    3. **Khám phá**: Xem các API categories bên trái
    
    ### 📚 Tài Liệu
    - **Swagger UI**: Trang này (interactive)
    - **ReDoc**: `/redoc` (detailed docs)
    - **OpenAPI Schema**: `/openapi.json`
    """
    return {
        "message": "🤖 Face Recognition API với MySQL Authentication",
        "version": "2.0.0",
        "status": "✅ Hoạt động",
        "authentication": "🔐 MySQL Session-based",
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "public": [
                "POST /query - Tìm kiếm khuôn mặt",
                "POST /query_top5 - Top 5 kết quả tương tự",
                "GET /vector_info - Thông tin database",
                "GET /health - Kiểm tra sức khỏe"
            ],
            "protected": [
                "POST /add_embedding - Thêm người mới (cần đăng nhập)",
                "PUT /edit_embedding - Sửa thông tin (cần đăng nhập)",
                "DELETE /delete_class - Xóa người (cần đăng nhập)",
                "POST /reset_index - Reset database (cần đăng nhập)"
            ],
            "auth": [
                "POST /auth/login - Đăng nhập MySQL",
                "POST /auth/logout - Đăng xuất"
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Face Recognition API with MySQL Authentication...")
    print("📚 Swagger UI: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    uvicorn.run(app, host="0.0.0.0", port=8000)
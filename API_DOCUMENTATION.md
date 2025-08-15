# 🤖 Face Recognition API Documentation

## 📋 API Endpoints Summary

### 🔐 Authentication Endpoints

#### POST `/auth/login`
**Route**: `POST http://localhost:8000/auth/login`
**Đăng nhập với MySQL account**

**Request Body**: Form-data
```
username: "admin"
password: "password123"
```

**Response Examples**:

✅ **Success Case**:
```json
{
  "success": true,
  "message": "Đăng nhập thành công với user admin",
  "username": "admin", 
  "token": "session_token_string_here"
}
```

❌ **Invalid Credentials**:
```json
{
  "detail": "Sai username hoặc password",
  "status_code": 401
}
```

---

#### POST `/auth/logout`
**Route**: `POST http://localhost:8000/auth/logout`
**Đăng xuất và clear session**

**Headers Required**:
```
Authorization: Bearer session_token_string
```

**Response Examples**:

✅ **Success Case**:
```json
{
  "success": true,
  "message": "User admin đã đăng xuất"
}
```

❌ **No Token**:
```json
{
  "detail": "Authentication required",
  "status_code": 401
}
```

---

### 🔍 Face Recognition Endpoints (Public)

#### POST `/query`
**Route**: `POST http://localhost:8000/query`
**Nhận diện khuôn mặt từ ảnh**

**Request**: Multipart form-data
```
image: [image file] (JPEG/PNG/WEBP)
```

**Response Examples**:

✅ **Found Match** (score > 0.5):
```json
{
  "image_id": 12345,
  "image_path": "casia-webface/000042/001.jpg",
  "class_id": "42",
  "score": 0.89,
  "nguoi": {
    "class_id": 42,
    "ten": "Nguyễn Văn An",
    "tuoi": 28,
    "gioitinh": "Nam",
    "noio": "Hà Nội"
  }
}
```

✅ **No Match Found** (score <= 0.5):
```json
{}
```

❌ **Invalid Image**:
```json
{
  "error": "Lỗi: Không decode được ảnh!",
  "status_code": 400
}
```

---

#### POST `/query_top5`
**Route**: `POST http://localhost:8000/query_top5`
**Top 5 kết quả nhận diện**

**Request**: Multipart form-data
```
file: [image file] (JPEG/PNG/WEBP)
```

**Response Examples**:

✅ **Multiple Matches Found**:
```json
{
  "success": true,
  "message": "Tìm thấy 5 kết quả phù hợp nhất",
  "results": [
    {
      "rank": 1,
      "class_id": 42,
      "ten": "Nguyễn Văn An",
      "tuoi": 28,
      "gioitinh": "Nam", 
      "noio": "Hà Nội",
      "similarity": 0.89,
      "confidence": "high"
    },
    {
      "rank": 2,
      "class_id": 17,
      "ten": "Trần Thị Bình",
      "tuoi": 25,
      "gioitinh": "Nữ",
      "noio": "TP.HCM", 
      "similarity": 0.76,
      "confidence": "medium"
    },
    {
      "rank": 3,
      "class_id": 91,
      "ten": "Lê Văn Cường",
      "tuoi": 32,
      "gioitinh": "Nam",
      "noio": "Đà Nẵng",
      "similarity": 0.68,
      "confidence": "medium"
    },
    {
      "rank": 4,
      "class_id": 156,
      "ten": "Phạm Thị Dung",
      "tuoi": 29,
      "gioitinh": "Nữ",
      "noio": "Cần Thơ",
      "similarity": 0.61,
      "confidence": "low"
    },
    {
      "rank": 5,
      "class_id": 203,
      "ten": "Hoàng Văn Em",
      "tuoi": 35,
      "gioitinh": "Nam",
      "noio": "Hải Phòng",
      "similarity": 0.55,
      "confidence": "low"
    }
  ],
  "total_candidates": 1250,
  "processing_time": 2.15,
  "face_detected": true
}
```

✅ **Few Matches Found**:
```json
{
  "success": true,
  "message": "Chỉ tìm thấy 2 kết quả phù hợp",
  "results": [
    {
      "rank": 1,
      "class_id": 88,
      "ten": "Võ Thị Giang",
      "tuoi": 22,
      "gioitinh": "Nữ",
      "noio": "Nha Trang", 
      "similarity": 0.72,
      "confidence": "medium"
    },
    {
      "rank": 2,
      "class_id": 134,
      "ten": "Đặng Văn Hùng",
      "tuoi": 27,
      "gioitinh": "Nam",
      "noio": "Huế",
      "similarity": 0.59,
      "confidence": "low"
    }
  ],
  "total_candidates": 1250,
  "processing_time": 1.89
}
```

---

#### POST `/predict`
**Route**: `POST http://localhost:8000/predict`
**Dự đoán tuổi và giới tính từ ảnh khuôn mặt**

**Request**: Multipart form-data
```
image: [image file] (JPEG/PNG/WEBP)
```

**Response Examples**:

✅ **Successful Prediction**:
```json
{
  "pred_age": 27,
  "pred_gender": "Male"
}
```

❌ **Model Not Loaded**:
```json
{
  "error": "Model not loaded",
  "status_code": 500
}
```

❌ **Invalid Image**:
```json
{
  "error": "Invalid image file", 
  "status_code": 400
}
```

---

### 🔒 Protected Data Management Endpoints

**Note**: All endpoints below require authentication via Bearer token in header.

#### POST `/add_embedding`
**Route**: `POST http://localhost:8000/add_embedding`
**Thêm người mới vào hệ thống**

**Headers Required**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: multipart/form-data
```

**Request**: Multipart form-data
```
file: [image file] (JPEG/PNG/WEBP)
ten: "Nguyễn Văn A"
tuoi: 25
gioitinh: "Nam"  
noio: "Hà Nội"
```

**Response Examples**:

✅ **Successfully Added**:
```json
{
  "success": true,
  "message": "Thêm người thành công",
  "person": {
    "class_id": 1251,
    "ten": "Nguyễn Văn A",
    "tuoi": 25,
    "gioitinh": "Nam",
    "noio": "Hà Nội",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "embedding_added": true,
  "total_people": 1251
}
```

❌ **Validation Error**:
```json
{
  "success": false,
  "error": "Invalid age",
  "message": "Tuổi phải nằm trong khoảng 1-120",
  "field": "tuoi",
  "value": 150
}
```

❌ **Face Detection Failed**:
```json
{
  "success": false,
  "error": "No face detected",
  "message": "Không phát hiện khuôn mặt trong ảnh. Vui lòng upload ảnh khác",
  "face_detected": false
}
```

❌ **Unauthorized**:
```json
{
  "success": false,
  "error": "Authentication failed",
  "message": "Token không hợp lệ hoặc đã hết hạn",
  "code": 401
}
```

---

#### PUT `/edit_embedding`
**Route**: `PUT http://localhost:8000/edit_embedding`
**Chỉnh sửa thông tin người**

**Headers Required**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: multipart/form-data
```

**Request**: Multipart form-data
```
class_id: 42
ten: "Nguyễn Văn An" (optional)
tuoi: 29 (optional)
gioitinh: "Nam" (optional)
noio: "TP.HCM" (optional)
file: [new image file] (optional, JPEG/PNG/WEBP)
```

**Response Examples**:

✅ **Successfully Updated**:
```json
{
  "success": true,
  "message": "Cập nhật thông tin thành công",
  "person": {
    "class_id": 42,
    "ten": "Nguyễn Văn An",
    "tuoi": 29,
    "gioitinh": "Nam",
    "noio": "TP.HCM",
    "updated_at": "2024-01-15T11:45:00Z"
  },
  "embedding_updated": true,
  "fields_changed": ["tuoi", "noio", "face_embedding"]
}
```

✅ **Info Only Update**:
```json
{
  "success": true,
  "message": "Cập nhật thông tin cá nhân thành công",
  "person": {
    "class_id": 42,
    "ten": "Nguyễn Văn An",
    "tuoi": 29,
    "gioitinh": "Nam",
    "noio": "TP.HCM"
  },
  "embedding_updated": false,
  "fields_changed": ["tuoi", "noio"]
}
```

❌ **Person Not Found**:
```json
{
  "success": false,
  "error": "Person not found",
  "message": "Không tìm thấy người với ID: 999",
  "class_id": 999
}
```

❌ **No Fields to Update**:
```json
{
  "success": false,
  "error": "No fields to update",
  "message": "Không có thông tin nào được thay đổi"
}
```

---

#### DELETE `/delete_class/{class_id}`
**Route**: `DELETE http://localhost:8000/delete_class/42`
**Xóa hoàn toàn một người khỏi hệ thống**

**Headers Required**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Path Parameters**:
```
class_id: integer (required)
```

**Response Examples**:

✅ **Successfully Deleted**:
```json
{
  "success": true,
  "message": "Xóa người thành công",
  "deleted_person": {
    "class_id": 42,
    "ten": "Nguyễn Văn An",
    "tuoi": 28,
    "gioitinh": "Nam",
    "noio": "Hà Nội"
  },
  "images_deleted": 5,
  "embedding_removed": true,
  "remaining_people": 1249
}
```

❌ **Person Not Found**:
```json
{
  "success": false,
  "error": "Person not found",
  "message": "Không tìm thấy người với ID: 999",
  "class_id": 999
}
```

❌ **Database Error**:
```json
{
  "success": false,
  "error": "Database error",
  "message": "Lỗi khi xóa dữ liệu từ database",
  "details": "Foreign key constraint failed"
}
```

---

#### DELETE `/delete_image`
**Route**: `DELETE http://localhost:8000/delete_image`
**Xóa một ảnh cụ thể của người**

**Headers Required**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

**Request Body**:
```json
{
  "class_id": 42,
  "image_path": "casia-webface/000042/003.jpg"
}
```

**Response Examples**:

✅ **Successfully Deleted**:
```json
{
  "success": true,
  "message": "Xóa ảnh thành công",
  "deleted_image": {
    "class_id": 42,
    "image_path": "casia-webface/000042/003.jpg",
    "file_size": "45.2KB"
  },
  "remaining_images": 4,
  "embedding_updated": true
}
```

❌ **Image Not Found**:
```json
{
  "success": false,
  "error": "Image not found",
  "message": "Không tìm thấy ảnh: casia-webface/000042/003.jpg"
}
```

❌ **Last Image Protection**:
```json
{
  "success": false,
  "error": "Cannot delete last image",
  "message": "Không thể xóa ảnh cuối cùng của người này",
  "remaining_images": 1
}
```

---

#### POST `/reset_index`
**Route**: `POST http://localhost:8000/reset_index`
**Reset toàn bộ FAISS index và database**

**Headers Required**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request Body** (optional):
```json
{
  "confirm": true,
  "backup": true
}
```

**Response Examples**:

✅ **Successfully Reset**:
```json
{
  "success": true,
  "message": "Reset hệ thống thành công",
  "operations": {
    "faiss_index_cleared": true,
    "database_truncated": true,
    "backup_created": true,
    "backup_path": "/backups/backup_2024-01-15_11-30-00.sql"
  },
  "statistics": {
    "people_removed": 1250,
    "embeddings_cleared": 1250,
    "images_processed": 0
  },
  "reset_time": "2024-01-15T11:30:00Z"
}
```

❌ **Confirmation Required**:
```json
{
  "success": false,
  "error": "Confirmation required",
  "message": "Cần xác nhận để thực hiện reset (confirm: true)",
  "warning": "Thao tác này sẽ xóa toàn bộ dữ liệu!"
}
```

❌ **Backup Failed**:
```json
{
  "success": false,
  "error": "Backup failed",
  "message": "Không thể tạo backup trước khi reset",
  "details": "Insufficient disk space"
}
```

---

### 📊 System Information Endpoints

#### GET `/list_nguoi`
**Route**: `GET http://localhost:8000/list_nguoi?query=&page=1&page_size=15`
**Lấy danh sách tất cả người trong hệ thống**

**Query Parameters**:
```
query: string (default: "") - Từ khóa tìm kiếm theo tên
page: integer (default: 1) - Số trang hiện tại
page_size: integer (default: 15, max: 100) - Số lượng kết quả mỗi trang
```

**Response Examples**:

✅ **With Results**:
```json
{
  "results": {
    "nguoi_list": [
      {
        "class_id": 1,
        "ten": "Nguyễn Văn An",
        "tuoi": 28,
        "gioitinh": "Nam",
        "noio": "Hà Nội"
      },
      {
        "class_id": 2,
        "ten": "Trần Thị Bình",
        "tuoi": 25,
        "gioitinh": "Nữ",
        "noio": "TP.HCM"
      }
    ],
    "total": 1250
  }
}
```

❌ **Error**:
```json
{
  "error": "Database connection failed"
}
```

---

#### GET `/vector_info`
**Route**: `GET http://localhost:8000/vector_info`
**Thông tin về FAISS vector index**

**Headers Required**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response Examples**:

✅ **Index Available**:
```json
{
  "success": true,
  "index_info": {
    "total_vectors": 1250,
    "vector_dimension": 512,
    "index_type": "IndexFlatIP",
    "memory_usage": "2.5MB",
    "last_updated": "2024-01-15T11:30:00Z"
  },
  "statistics": {
    "average_similarity": 0.73,
    "min_similarity": 0.21,
    "max_similarity": 0.98,
    "unique_classes": 1250
  },
  "performance": {
    "search_time_avg": "15ms",
    "build_time": "45s",
    "queries_today": 247
  }
}
```

❌ **Index Not Available**:
```json
{
  "success": false,
  "error": "Index not initialized",
  "message": "FAISS index chưa được khởi tạo",
  "suggestion": "Hãy thêm người đầu tiên để khởi tạo index"
}
```

---

#### GET `/index_status`
**Route**: `GET http://localhost:8000/index_status`
**Trạng thái chi tiết của FAISS index**

**Headers Required**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response Examples**:

✅ **Healthy Index**:
```json
{
  "success": true,
  "status": "healthy",
  "details": {
    "index_size": 1250,
    "is_trained": true,
    "dimension": 512,
    "metric_type": "METRIC_INNER_PRODUCT",
    "memory_usage_bytes": 2621440,
    "last_build_time": "2024-01-15T11:30:00Z"
  },
  "health_checks": {
    "can_search": true,
    "can_add": true,
    "dimension_consistent": true,
    "memory_available": true
  },
  "recommendations": []
}
```

⚠️ **Warning Status**:
```json
{
  "success": true,
  "status": "warning",
  "details": {
    "index_size": 1250,
    "is_trained": true,
    "dimension": 512,
    "metric_type": "METRIC_INNER_PRODUCT",
    "memory_usage_bytes": 2621440
  },
  "health_checks": {
    "can_search": true,
    "can_add": true,
    "dimension_consistent": true,
    "memory_available": false
  },
  "warnings": ["High memory usage detected"],
  "recommendations": ["Consider optimizing index or adding more memory"]
}
```

❌ **Error Status**:
```json
{
  "success": false,
  "status": "error",
  "error": "Index corrupted",
  "message": "FAISS index bị lỗi và cần được rebuild",
  "recommendations": ["Backup current data", "Rebuild index from database"]
}
```

---

#### GET `/health`
**Route**: `GET http://localhost:8000/health`
**Health check cho toàn bộ hệ thống**

**Authentication**: None required

**Response Examples**:

✅ **All Systems Healthy**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T12:00:00Z",
  "services": {
    "api": {
      "status": "up",
      "response_time": "2ms"
    },
    "database": {
      "status": "up",
      "connection_pool": "8/10 active",
      "response_time": "5ms"
    },
    "faiss_index": {
      "status": "up", 
      "total_vectors": 1250,
      "last_updated": "2024-01-15T11:30:00Z"
    },
    "face_recognition": {
      "status": "up",
      "model_loaded": true,
      "gpu_available": true
    },
    "age_gender_prediction": {
      "status": "up",
      "model_loaded": true,
      "last_prediction": "2024-01-15T11:58:00Z"
    }
  },
  "system_info": {
    "uptime": "5 days, 14 hours",
    "memory_usage": "2.1GB / 8GB",
    "cpu_usage": "15%",
    "disk_usage": "45% of 100GB"
  }
}
```

⚠️ **Degraded Performance**:
```json
{
  "status": "degraded",
  "timestamp": "2024-01-15T12:00:00Z",
  "services": {
    "api": {
      "status": "up",
      "response_time": "25ms"
    },
    "database": {
      "status": "up",
      "connection_pool": "10/10 active",
      "response_time": "45ms",
      "warning": "High connection usage"
    },
    "faiss_index": {
      "status": "up",
      "total_vectors": 1250,
      "warning": "High memory usage"
    },
    "face_recognition": {
      "status": "up",
      "model_loaded": true,
      "gpu_available": false,
      "warning": "Running on CPU only"
    }
  },
  "warnings": [
    "Database connection pool at maximum",
    "GPU not available, using CPU for face recognition",
    "High memory usage detected"
  ]
}
```

❌ **System Error**:
```json
{
  "status": "error",
  "timestamp": "2024-01-15T12:00:00Z",
  "services": {
    "api": {
      "status": "up"
    },
    "database": {
      "status": "down",
      "error": "Connection timeout",
      "last_successful": "2024-01-15T11:45:00Z"
    },
    "faiss_index": {
      "status": "error",
      "error": "Index not loaded"
    }
  },
  "errors": [
    "Database connection failed",
    "FAISS index not available"
  ]
}
```

---

## 🛡️ Authentication Details

### Token-based Authentication
Hệ thống sử dụng **MySQL session-based authentication**:

1. **Login Flow**:
   ```bash
   POST /auth/login
   Body: {"username": "your_user", "password": "your_pass"}
   Response: {"token": "session_token_string"}
   ```

2. **Using Token**:
   ```bash
   Authorization: Bearer session_token_string
   ```

3. **Logout**:
   ```bash
   POST /auth/logout
   Header: Authorization: Bearer session_token_string
   ```

### Security Requirements
- **Public APIs**: Không cần authentication (query, search, health)
- **Protected APIs**: Cần Bearer token từ `/auth/login`
- **MySQL Integration**: Authentication thông qua bảng `taikhoan`

---

## 📚 Usage Examples

### JavaScript Frontend Integration
```javascript
// Login
const loginResponse = await fetch('/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username: 'user', password: 'pass'})
});
const {token} = await loginResponse.json();

// Use protected API
const addResponse = await fetch('/add_embedding', {
    method: 'POST',
    headers: {'Authorization': `Bearer ${token}`},
    body: formData
});
```

### Python Client Example
```python
import requests

# Login
login_data = {"username": "user", "password": "password"}
response = requests.post("http://localhost:8000/auth/login", json=login_data)
token = response.json()["token"]

# Use protected API
headers = {"Authorization": f"Bearer {token}"}
files = {"file": open("photo.jpg", "rb")}
data = {"ten_nguoi": "Nguyen Van A", "tuoi": 25}
response = requests.post("http://localhost:8000/add_embedding", 
                        headers=headers, files=files, data=data)
```

---

## 🔧 Error Handling

### Common HTTP Status Codes
- **200**: Success
- **401**: Unauthorized (cần đăng nhập hoặc token invalid)
- **422**: Validation Error (dữ liệu input không hợp lệ)
- **500**: Internal Server Error

### Error Response Format
```json
{
    "success": false,
    "error": "Error description",
    "details": "Additional error details"
}
```

---

## 📝 Development Notes

### Database Schema Required
```sql
-- Bảng authentication
CREATE TABLE taikhoan (
    username VARCHAR(50) PRIMARY KEY,
    passwrd VARCHAR(255) NOT NULL
);

-- Bảng thông tin người
CREATE TABLE nguoi (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    ten VARCHAR(100),
    tuoi INT,
    gioitinh VARCHAR(10),
    noio VARCHAR(200)
);
```

### Environment Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Setup MySQL database và import schema
3. Configure database connection trong `db/mysql_conn.py`
4. Run server: `uvicorn app:app --host 0.0.0.0 --port 8000`

---

**Version**: 2.0.0  
**Last Updated**: August 2025  
**Authentication**: MySQL Session-based  
**Security Model**: Public/Protected API classification

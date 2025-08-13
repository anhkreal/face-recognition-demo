# 🤖 Face Recognition API Documentation

## 📋 API Endpoints Summary

### 🔐 Authentication Endpoints

#### POST `/auth/login`
**Đăng nhập với MySQL account**
- **Input**: `{"username": "string", "password": "string"}`
- **Output**: `{"success": true, "token": "session_token", "username": "string"}`
- **Authentication**: None required
- **Description**: Đăng nhập bằng tài khoản trong bảng `taikhoan` MySQL

#### POST `/auth/logout`
**Đăng xuất và clear session**
- **Input**: None
- **Output**: `{"success": true, "message": "Đăng xuất thành công"}`
- **Authentication**: Bearer token required
- **Description**: Kết thúc session và invalidate token

---

### 🔍 Face Recognition Endpoints (Public)

#### POST `/query`
**Nhận diện khuôn mặt từ ảnh**
- **Input**: `file: UploadFile` (ảnh JPEG/PNG)
- **Output**: Thông tin người được nhận diện hoặc "Không tìm thấy"
- **Authentication**: None required
- **Description**: Upload ảnh và tìm người tương tự nhất trong database

#### POST `/query_top5`
**Top 5 kết quả nhận diện**
- **Input**: `file: UploadFile` (ảnh JPEG/PNG)
- **Output**: Danh sách 5 người giống nhất với độ tin cậy
- **Authentication**: None required
- **Description**: Trả về nhiều kết quả để lựa chọn

---

### 🔒 Data Management Endpoints (Protected)

#### POST `/add_embedding`
**Thêm người mới vào hệ thống**
- **Input**: 
  - `file: UploadFile` (ảnh khuôn mặt)
  - `ten_nguoi: str`
  - `tuoi: int`
  - `gioi_tinh: str`
  - `noi_o: str`
- **Output**: `{"success": true, "class_id": 123, "message": "..."}`
- **Authentication**: Bearer token required
- **Description**: Thêm người mới với thông tin cá nhân

#### PUT `/edit_embedding`
**Chỉnh sửa thông tin người**
- **Input**: `class_id`, các field muốn update
- **Output**: `{"success": true, "message": "Cập nhật thành công"}`
- **Authentication**: Bearer token required
- **Description**: Sửa thông tin người đã có trong hệ thống

#### DELETE `/delete_class`
**Xóa toàn bộ thông tin người**
- **Input**: `{"class_id": 123}`
- **Output**: `{"success": true, "message": "Đã xóa class_id"}`
- **Authentication**: Bearer token required
- **Description**: Xóa vĩnh viễn tất cả dữ liệu của một người

#### DELETE `/delete_image`
**Xóa ảnh cụ thể**
- **Input**: `{"image_id": "path/to/image.jpg"}`
- **Output**: `{"success": true, "message": "Đã xóa ảnh"}`
- **Authentication**: Bearer token required
- **Description**: Xóa một ảnh cụ thể của người

#### POST `/reset_index`
**Reset toàn bộ FAISS index**
- **Input**: None
- **Output**: `{"success": true, "message": "FAISS index đã được reset"}`
- **Authentication**: Bearer token required
- **Description**: ⚠️ NGUY HIỂM - Xóa toàn bộ dữ liệu vector

---

### 📊 System Information Endpoints (Public)

#### GET `/list_nguoi`
**Danh sách người trong hệ thống**
- **Input**: Query parameters cho tìm kiếm và phân trang
- **Output**: Danh sách người với thông tin chi tiết
- **Authentication**: None required
- **Description**: Xem và tìm kiếm người trong database

#### GET `/vector_info`
**Thông tin FAISS vector database**
- **Output**: Thống kê về số lượng vectors, kích thước index
- **Authentication**: None required
- **Description**: Thông tin kỹ thuật về vector database

#### GET `/index_status`
**Trạng thái hệ thống**
- **Output**: Tình trạng FAISS index, performance metrics
- **Authentication**: None required
- **Description**: Kiểm tra sức khỏe của hệ thống

#### GET `/health`
**Health check cơ bản**
- **Output**: `{"status": "healthy", "timestamp": "..."}`
- **Authentication**: None required
- **Description**: Kiểm tra API có hoạt động không

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

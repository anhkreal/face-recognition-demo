# CHANGELOG - Face Recognition API với MySQL Authentication

## [0.2.1] - 2025-08-14 🆕 AGE/GENDER PREDICTION API

### 🆕 Age/Gender Prediction API
- **Added**: Public endpoint `POST /predict` cho phép dự đoán tuổi và giới tính từ ảnh khuôn mặt (không cần đăng nhập)
- **Added**: Module `predict_service.py` và `api/predict.py` cho xử lý và expose API mới
- **No Breaking Change**: Các API cũ vẫn giữ nguyên, không ảnh hưởng authentication

---

## [0.2.0] - 2025-08-13 🔐 MYSQL AUTHENTICATION MAJOR RELEASE

### 🔐 MySQL Authentication System - MAJOR CHANGE
- **CHANGED** Authentication system từ JWT sang MySQL session-based
- **Added** MySQL database authentication thông qua bảng `taikhoan`
- **Added** Session token management với MySQL storage
- **Added** Bearer token authentication cho protected APIs
- **Removed** JWT token system và OAuth2 complexity
- **Simplified** Authentication flow: login → session token → logout

### �️ Security Model Update - BREAKING CHANGE
- **Simplified** Security model thành Public/Protected categories
- **Removed** Role-based access control (RBAC) complexity
- **Updated** Authentication requirement: "Đảm bảo phải đăng nhập thông qua bảng taikhoan MySQL mới được các tác vụ thêm/sửa/xóa MySQL/FAISS, còn truy vấn khỏi cần"
- **Maintained** Security headers và CORS configuration
- **Cleaned** Security logging để remove token exposure
- **Added** Security middleware stack
- **Added** Authentication router integration
- **Updated** API version to 2.1.0
- **Added** Comprehensive logging cho startup

### 📦 Dependencies & Configuration - NEW
- **Updated** `requirements.txt` với JWT dependencies:
  - `python-jose[cryptography]` for JWT handling
  - `passlib[bcrypt]` for password hashing
  - `python-multipart` for form data
  - `pydantic[email]` for validation
  - `python-dotenv` for environment management
- **Added** `.env.example` với all configuration options
- **Updated** `.gitignore` với comprehensive security patterns

### 🛠️ Setup & Testing Tools - NEW
- **Added** `setup_jwt.py` - Automated JWT system setup script
- **Added** `test_jwt_health.py` - Comprehensive JWT health check script
- **Added** Default admin account creation (admin/admin123!@#)
- **Added** Automatic secret key generation

### 🔄 API Endpoint Changes

#### NEW Authentication Endpoints:
- `POST /auth/token` - Login và nhận JWT access token
- `POST /auth/register` - Register user mới (ADMIN only)
- `GET /auth/me` - Current user information
- `POST /auth/change-password` - Change password
- `POST /auth/refresh` - Token refresh (planned)

#### PROTECTED (JWT Required):
- `POST /add_embedding` - Now requires JWT + write scope
- `POST /edit_embedding` - Now requires JWT + write scope
- `POST /delete_image` - Now requires JWT + delete scope (ADMIN)
- `POST /delete_class` - Now requires JWT + delete scope (ADMIN)
- `POST /reset_index` - Now requires JWT + delete scope (ADMIN)

#### PUBLIC (No JWT Required):
- `POST /query` - Face recognition remains public
- `POST /query_top5` - Top 5 results remains public
- `GET /list_nguoi` - Search remains public
- `GET /health` - Health checks remain public
- All monitoring endpoints remain public

### 🏆 Key Features Added

#### Security Features:
- ✅ JWT Authentication với 30-minute expiry
- ✅ Role-based access control (RBAC)
- ✅ Scope-based permissions
- ✅ Rate limiting (5-60 req/min based on endpoint)
- ✅ Password strength validation
- ✅ Account lockout protection
- ✅ Security headers (XSS, CSRF, clickjacking)
- ✅ Audit logging cho protected operations

#### User Management:
- ✅ JSON file-based user storage
- ✅ Bcrypt password hashing
- ✅ Default admin account creation
- ✅ User registration (admin only)
- ✅ Password change functionality
- ✅ User role và scope management

#### Developer Experience:
- ✅ Comprehensive API documentation
- ✅ Setup automation scripts
- ✅ Health check utilities
- ✅ Environment configuration
- ✅ Security best practices documentation

### ⚠️ Breaking Changes
- **BREAKING**: Add/edit/delete APIs now require JWT authentication
- **BREAKING**: Admin-only APIs require ADMIN role
- **BREAKING**: API response format include audit information
- **BREAKING**: CORS now restricted to specific origins

### 🔄 Migration Guide
1. Run `python setup_jwt.py` để setup JWT system
2. Copy `.env.example` to `.env` và configure
3. Install new dependencies: `pip install -r requirements.txt`
4. Login với admin account (admin/admin123!@#)
5. Change admin password immediately
6. Update frontend để include JWT token trong requests
7. Test với `python test_jwt_health.py`

### 🎯 Next Steps & Roadmap
- [ ] Token refresh mechanism
- [ ] Session management
- [ ] Advanced user management UI
- [ ] Integration với external auth providers
- [ ] Advanced audit logging với database storage
- [ ] Rate limiting với Redis backend
- [ ] Multi-factor authentication (MFA)

---

## [0.1.2] - 2025-08-10
- **Added**: Tích hợp FAISS vector database cho tìm kiếm khuôn mặt
- **Added**: API nhận diện khuôn mặt cơ bản (POST /query)
- **Added**: Health check endpoint (GET /health)
- **Added**: Cấu trúc thư mục chuẩn cho backend và model
- **Improved**: Hiệu năng truy vấn với singleton pattern

## [0.1.1] - 2025-08-07
- **Improved**: Tối ưu tốc độ nhận diện khuôn mặt với batch processing
- **Added**: Logging chi tiết cho các API endpoint
- **Fixed**: Sửa lỗi không nhận diện đúng với ảnh đầu vào kích thước lớn
- **Added**: Thêm endpoint GET /list_nguoi để liệt kê danh sách người trong hệ thống
- **Improved**: Cập nhật tài liệu hướng dẫn sử dụng API và ví dụ request/response
- **Fixed**: Sửa lỗi kết nối MySQL không ổn định khi truy vấn liên tục

## [0.1.0] - 2025-08-05
- **Initial release**: Khởi tạo project nhận diện khuôn mặt
- **Added**: Nhận diện khuôn mặt sử dụng ArcFace (POST /query)
- **Added**: Kết nối MySQL cơ bản cho lưu thông tin người dùng
- **Added**: API health check (GET /health)
- **Added**: Cấu trúc thư mục backend chuẩn (app.py, model/, db/)
- **Added**: Tài liệu cài đặt và hướng dẫn sử dụng ban đầu (README.md)
- **Added**: Script import dữ liệu mẫu vào MySQL
- **Added**: Đăng nhập cơ bản với username/password (chưa có token)
- **Known Limitation**: Chưa có xác thực token, chưa có phân quyền, chưa tối ưu hiệu năng cho FAISS

---

**🔐 Security Note**: Đây là major security update. Tất cả protected APIs đều require JWT authentication. Hãy đảm bảo frontend và integrations được update để support JWT tokens.

**📚 Documentation**: Xem README.md được update với comprehensive JWT authentication guide.

**🆘 Support**: Nếu có issues với JWT authentication, chạy `python test_jwt_health.py` để diagnose.

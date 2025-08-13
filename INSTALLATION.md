# 🚀 Installation Guide - Face Recognition API với MySQL Authentication

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Ubuntu 18.04+, macOS 10.15+
- **Python**: 3.8 hoặc mới hơn
- **RAM**: 4GB (khuyến nghị 8GB+)
- **Storage**: 10GB free space
- **MySQL**: 5.7+ hoặc 8.0+

### Recommended for Production
- **RAM**: 16GB+
- **CPU**: 4+ cores
- **Storage**: SSD với 50GB+ free space
- **GPU**: NVIDIA GPU với CUDA support (optional)

---

## 🔧 Step 1: Install Dependencies

### 1.1 Clone Repository
```bash
git clone https://github.com/your-repo/face-recognition-api.git
cd face-recognition-api/face_api
```

### 1.2 Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 1.3 Install Python Packages
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🗄️ Step 2: Setup MySQL Database

### 2.1 Install MySQL Server

#### Windows (XAMPP - Recommended)
1. Download XAMPP từ https://www.apachefriends.org/
2. Install và khởi động Apache + MySQL
3. Access phpMyAdmin: http://localhost/phpmyadmin

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

#### macOS (Homebrew)
```bash
brew install mysql
brew services start mysql
```

### 2.2 Create Database và Tables
```sql
-- Create database
CREATE DATABASE face_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE face_db;

-- Create authentication table
CREATE TABLE taikhoan (
    username VARCHAR(50) PRIMARY KEY,
    passwrd VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Create people information table
CREATE TABLE nguoi (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    ten VARCHAR(100) NOT NULL,
    tuoi INT,
    gioitinh VARCHAR(10),
    noio VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample authentication account
INSERT INTO taikhoan (username, passwrd) VALUES 
('admin', 'admin123'),
('user1', 'password123');
```

### 2.3 Import Sample Data (Optional)
```bash
cd db
python dump_import_class_info_to_mysql.py
```

---

## ⚙️ Step 3: Configuration

### 3.1 Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file với database credentials
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=face_db
```

### 3.2 Database Connection Test
```bash
python -c "
from db.mysql_conn import get_connection
try:
    conn = get_connection()
    print('✅ Database connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"
```

---

## 🤖 Step 4: Download AI Models

### 4.1 Create Model Directory
```bash
mkdir -p model
cd model
```

### 4.2 Download ArcFace Models
Download the following models và đặt vào thư mục `model/`:

1. **ms1mv3_arcface_r18_fp16.pth** (ResNet-18 model)
   - Size: ~84MB
   - Download link: [Contact support for model files]

2. **glint360k_cosface_r18_fp16_0.1.pth** (Alternative model)
   - Size: ~84MB
   - Backup model cho comparison

### 4.3 Verify Model Files
```bash
# Check model files exist
ls -la model/
# Should show:
# ms1mv3_arcface_r18_fp16.pth
# glint360k_cosface_r18_fp16_0.1.pth
```

---

## 🚀 Step 5: First Run

### 5.1 Start Development Server
```bash
# From face_api directory
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 5.2 Verify Installation
1. **Check Startup Logs**:
   ```
   🚀 Khởi tạo Face Recognition System thành công!
   🔐 MySQL Authentication system đã được tích hợp!
   📊 Security middleware và logging đã được kích hoạt!
   ```

2. **Access API Documentation**:
   - Open browser: http://localhost:8000/docs
   - Should see Swagger UI with MySQL authentication

3. **Test Health Endpoint**:
   ```bash
   curl http://localhost:8000/health
   # Expected: {"status": "healthy", "timestamp": "..."}
   ```

### 5.3 Test Authentication
```bash
# Test login
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'

# Expected response:
# {"success": true, "token": "session_token_string", "username": "admin"}
```

---

## 🌐 Step 6: Frontend Setup (Optional)

### 6.1 Access Web Interface
- **Main App**: http://localhost:8000/
- **Login Page**: http://localhost:8000/auth.html
- **API Docs**: http://localhost:8000/docs

### 6.2 Configure Frontend (if needed)
Edit `frontend/utils/main.js` để update API base URL:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

---

## 🔒 Step 7: Security Setup

### 7.1 Change Default Passwords
```sql
-- Update admin password
UPDATE taikhoan SET passwrd = 'your_secure_password' WHERE username = 'admin';

-- Remove or update test accounts
DELETE FROM taikhoan WHERE username = 'user1';
```

### 7.2 Production Security Settings
In `.env` file:
```bash
# Production settings
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SECURITY_HEADERS=true
DB_PASSWORD=very_secure_password
```

---

## 🔍 Step 8: Verification Tests

### 8.1 Test Public APIs
```bash
# Health check
curl http://localhost:8000/health

# List people (should be empty initially)
curl http://localhost:8000/list_nguoi
```

### 8.2 Test Protected APIs
```bash
# Login first
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | \
  grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# Test protected endpoint
curl -X POST "http://localhost:8000/add_embedding" \
     -H "Authorization: Bearer $TOKEN" \
     -F "file=@test_image.jpg" \
     -F "ten_nguoi=Test User" \
     -F "tuoi=25" \
     -F "gioi_tinh=Nam" \
     -F "noi_o=Ha Noi"
```

---

## ⚡ Step 9: Performance Optimization

### 9.1 For GPU Support (Optional)
```bash
# Install GPU-enabled PyTorch
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install FAISS-GPU
pip uninstall faiss-cpu
pip install faiss-gpu
```

### 9.2 Production Deployment
```bash
# Use production ASGI server
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. Database Connection Error
```
Error: (2003, "Can't connect to MySQL server")
```
**Solution**:
- Verify MySQL service is running
- Check credentials trong `.env`
- Test connection manually

#### 2. Model File Not Found
```
FileNotFoundError: model file not found
```
**Solution**:
- Download model files vào thư mục `model/`
- Check file permissions
- Verify file paths trong `config.py`

#### 3. Import Error
```
ModuleNotFoundError: No module named 'faiss'
```
**Solution**:
```bash
pip install faiss-cpu
# hoặc cho GPU: pip install faiss-gpu
```

#### 4. Authentication Failed
```
{"success": false, "error": "Invalid credentials"}
```
**Solution**:
- Check MySQL taikhoan table có data
- Verify username/password
- Check database connection

---

## 📚 Next Steps

### After Installation
1. **Read Documentation**: Review `README.md` và `API_DOCUMENTATION.md`
2. **Import Data**: Add initial people vào database
3. **Test Face Recognition**: Upload test images
4. **Setup Production**: Configure domain và SSL
5. **Monitoring**: Setup logging và monitoring tools

### Development
1. **Code Structure**: Review `api/` và `service/` directories
2. **Database Schema**: Understand `db/` models
3. **Authentication**: Review `auth/` implementation
4. **Frontend**: Customize `frontend/` interface

---

**Installation Complete!** 🎉

Your Face Recognition API với MySQL Authentication đã sẵn sàng sử dụng.

**Quick Access:**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Login: http://localhost:8000/auth.html

**Support**: Check `CHANGELOG.md` và `README.md` để biết thêm chi tiết.

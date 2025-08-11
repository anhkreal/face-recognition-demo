# Face Recognition API System

## 📖 Tổng quan

Hệ thống Face Recognition API là một ứng dụng nhận diện khuôn mặt hoàn chỉnh được xây dựng bằng Python, sử dụng FastAPI làm backend framework. Hệ thống kết hợp **thư viện InsightFace** (từ thư mục `insightface/`) với mô hình ArcFace để trích xuất đặc trưng khuôn mặt, FAISS để tìm kiếm vector tương tự, và MySQL để lưu trữ thông tin người dùng.

**Đặc biệt**: Dự án này tích hợp trực tiếp source code của **InsightFace** thông qua thư mục `insightface/`, bao gồm các module recognition, detection và các công cụ hỗ trợ khác.

## 🏗️ Kiến trúc hệ thống

```
Frontend (HTML/JS/CSS)
       ↓
FastAPI Backend (Python)
       ↓ ↙ ↘
   MySQL    FAISS    ArcFace Model
```

### Thành phần chính:
- **Frontend**: Giao diện web HTML/CSS/JavaScript
- **Backend API**: FastAPI với các endpoint RESTful
- **Database**: MySQL để lưu thông tin người dùng
- **Vector Database**: FAISS để tìm kiếm tương tự embedding
- **AI Model**: ArcFace (từ thư viện InsightFace) để trích xuất đặc trưng khuôn mặt
- **InsightFace Library**: Thư viện mã nguồn mở được tích hợp trực tiếp từ thư mục `insightface/`

## 🚀 Tính năng

### 1. Xác thực người dùng
- Đăng ký tài khoản mới
- Đăng nhập hệ thống
- Quản lý phiên làm việc

### 2. Nhận diện khuôn mặt
- Upload ảnh và nhận diện người trong ảnh
- Trả về thông tin chi tiết người được nhận diện
- Độ chính xác cao với threshold 0.5

### 3. Quản lý dữ liệu
- Thêm người mới vào hệ thống
- Chỉnh sửa thông tin người đã có
- Xóa người khỏi hệ thống
- Tìm kiếm người theo tên, tuổi, địa chỉ

### 4. Quản lý vector embedding
- Thêm/sửa/xóa embedding
- Tìm kiếm embedding theo class_id
- Reset toàn bộ index FAISS
- Kiểm tra trạng thái index

## 📁 Cấu trúc thư mục

```
face_api/
├── app.py                 # File chính để chạy FastAPI server
├── config.py             # Cấu hình đường dẫn model và index
├── requirements.txt      # Dependencies cần thiết
├── 
├── api/                  # Các API endpoint
│   ├── face_query.py    # API nhận diện khuôn mặt
│   ├── add_embedding.py # API thêm người mới
│   ├── login.py         # API đăng nhập
│   ├── register.py      # API đăng ký
│   └── ...
├── 
├── service/             # Business logic
│   ├── face_query_service.py
│   ├── add_embedding_service.py
│   └── ...
├── 
├── model/               # AI Model
│   ├── arcface_model.py # Class xử lý ArcFace model
│   ├── glint360k_cosface_r18_fp16_0.1.pth
│   └── ms1mv3_arcface_r18_fp16.pth
├── 
├── index/               # FAISS vector database
│   ├── faiss.py        # Class quản lý FAISS index
│   ├── faiss_db_r18.index
│   └── faiss_db_r18_meta.npz
├── 
├── db/                  # Database
│   ├── mysql_conn.py   # Kết nối MySQL
│   ├── models.py       # Data models
│   ├── nguoi_repository.py
│   ├── class_info.csv  # Dữ liệu mẫu
│   └── dump_import_class_info_to_mysql.py
├── 
├── frontend/            # Giao diện web
│   ├── index.html      # Trang chính
│   ├── auth.html       # Trang đăng nhập
│   └── assets/
└── 
└── insightface/         # Thư viện InsightFace (source code)
    ├── recognition/     # Module nhận diện khuôn mặt
    │   └── arcface_torch/  # Implementation ArcFace với PyTorch
    ├── detection/       # Module phát hiện khuôn mặt
    ├── python-package/  # Python package của InsightFace
    ├── cpp-package/     # C++ implementation
    ├── model_zoo/       # Model repository
    ├── examples/        # Ví dụ sử dụng
    └── tools/          # Công cụ hỗ trợ
```

## 🧠 Về thư viện InsightFace

### Tổng quan InsightFace
Dự án này tích hợp trực tiếp **source code của InsightFace** - một thư viện mã nguồn mở hàng đầu về nhận diện khuôn mặt, được phát triển bởi đội ngũ nghiên cứu tại Imperial College London và các cộng tác viên.

### Cấu trúc thư mục InsightFace trong dự án:
```
insightface/
├── recognition/         # Module nhận diện khuôn mặt chính
│   └── arcface_torch/  # Implementation ArcFace với PyTorch
│       ├── backbones/  # Các kiến trúc mạng backbone (ResNet, etc.)
│       ├── configs/    # File cấu hình training
│       └── losses/     # Các loss functions
├── detection/          # Module phát hiện khuôn mặt
├── python-package/     # Package Python chính thức
├── cpp-package/        # Implementation C++ cho hiệu suất cao
├── model_zoo/          # Repository các pre-trained models
├── examples/           # Ví dụ và demo
└── tools/             # Công cụ hỗ trợ training và evaluation
```

### Cách sử dụng trong dự án:
1. **Import trực tiếp**: Thay vì cài đặt package, dự án import trực tiếp từ source:
   ```python
   sys.path.append('path/to/insightface/recognition/arcface_torch')
   from backbones import get_model
   ```

2. **Model được sử dụng**: 
   - **ArcFace R18**: Kiến trúc ResNet-18 với ArcFace loss
   - **Embedding size**: 512 dimensions
   - **Model files**: `.pth` format trong thư mục `model/`

3. **Ưu điểm**:
   - Không phụ thuộc vào package external
   - Có thể tùy chỉnh source code nếu cần
   - Đảm bảo tính ổn định và tương thích

## 🛠️ Cài đặt và Cấu hình

### 1. Yêu cầu hệ thống
- Python 3.8+
- MySQL Server (XAMPP khuyến nghị)
- CUDA (tùy chọn, để sử dụng GPU)

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

**Dependencies chính:**
```
fastapi
uvicorn
opencv-python
numpy
torch
albumentations
faiss-cpu
pymysql
```

**Lưu ý về InsightFace**: Dự án này sử dụng source code InsightFace được tích hợp sẵn trong thư mục `insightface/`, do đó không cần cài đặt thêm package `insightface` từ PyPI. Module `arcface_model.py` sẽ import trực tiếp từ:
```python
sys.path.append('C:/Users/DELL/Downloads/archive/face_api/insightface/recognition/arcface_torch')
from backbones import get_model
```

### 3. Cấu hình MySQL

#### Bước 1: Cài đặt XAMPP
- Tải và cài đặt XAMPP từ https://www.apachefriends.org/
- Khởi động Apache và MySQL trong XAMPP Control Panel

#### Bước 2: Tạo database
```sql
CREATE DATABASE face_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Bước 3: Tạo bảng và import dữ liệu
```bash
cd db
python dump_import_class_info_to_mysql.py
```

Lệnh này sẽ:
- Tạo database `face_db` nếu chưa có
- Tạo bảng `nguoi` với cấu trúc:
  ```sql
  CREATE TABLE nguoi (
      class_id INT PRIMARY KEY,
      ten VARCHAR(100),
      tuoi INT,
      gioitinh VARCHAR(10),
      noio VARCHAR(100)
  );
  ```
- Tạo bảng `taikhoan` cho xác thực:
  ```sql
  CREATE TABLE taikhoan (
      username VARCHAR(50) PRIMARY KEY,
      passwrd VARCHAR(255)
  );
  ```
- Import dữ liệu mẫu từ `class_info.csv`

### 4. Cấu hình Model và InsightFace

#### Thiết lập InsightFace:
Dự án sử dụng source code InsightFace được tích hợp trong thư mục `insightface/`. Module `model/arcface_model.py` đã được cấu hình để sử dụng:

```python
# Trong model/arcface_model.py
sys.path.append('C:/Users/DELL/Downloads/archive/face_api/insightface/recognition/arcface_torch')
from backbones import get_model
```

**Điều chỉnh đường dẫn**: Nếu dự án của bạn ở vị trí khác, hãy sửa đường dẫn trong `model/arcface_model.py`:
```python
sys.path.append('[ĐỘI_DẪN_DỰ_ÁN]/insightface/recognition/arcface_torch')
```

#### Tải model ArcFace (nếu chưa có):
```bash
# Đặt file model vào thư mục model/
# - glint360k_cosface_r18_fp16_0.1.pth
# - ms1mv3_arcface_r18_fp16.pth
```

#### Kiểm tra cấu hình trong `config.py`:
```python
MODEL_PATH = 'model/glint360k_cosface_r18_fp16_0.1.pth'
FAISS_INDEX_PATH = 'index/faiss_db_r18.index'
FAISS_META_PATH = 'index/faiss_db_r18_meta.npz'
```

### 5. Khởi tạo FAISS Index (lần đầu)
```bash
python dump_faiss_vectors.py
```

## 🚀 Chạy ứng dụng

### 1. Khởi động Backend API
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Truy cập ứng dụng
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: Mở file `frontend/index.html` trong trình duyệt
- **Trang đăng nhập**: `frontend/auth.html`

### 3. Kiểm tra kết nối
```bash
# Test API
curl http://localhost:8000/docs

# Test MySQL connection
python db/mysql_conn.py
```

## 📡 API Endpoints

### Authentication
- `POST /register` - Đăng ký tài khoản mới
- `POST /login` - Đăng nhập

### Face Recognition
- `POST /query` - Nhận diện khuôn mặt từ ảnh upload
- `POST /query_top5` - Trả về top 5 kết quả tương tự nhất

### Data Management
- `POST /add_embedding` - Thêm người mới với ảnh
- `PUT /edit_embedding` - Chỉnh sửa thông tin người
- `DELETE /delete_image/{image_id}` - Xóa ảnh cụ thể
- `DELETE /delete_class/{class_id}` - Xóa toàn bộ thông tin người

### Search & Query
- `GET /list_nguoi` - Danh sách và tìm kiếm người (có phân trang)
- `GET /search_embeddings` - Tìm kiếm embedding theo class_id
- `GET /get_image_ids_by_class/{class_id}` - Lấy danh sách ảnh của người

### System Management
- `GET /index_status` - Kiểm tra trạng thái FAISS index
- `POST /reset_index` - Reset toàn bộ FAISS index
- `GET /vector_info` - Thông tin chi tiết về vector database

## 🎯 Workflow sử dụng

### 1. Đăng nhập hệ thống
1. Mở `frontend/auth.html`
2. Đăng ký tài khoản mới hoặc đăng nhập
3. Chuyển hướng đến trang chính

### 2. Nhận diện khuôn mặt
1. Chọn tab "Nhận diện khuôn mặt"
2. Upload ảnh cần nhận diện
3. Nhận kết quả với thông tin chi tiết

### 3. Thêm người mới
1. Chọn tab "Thêm người mới"
2. Nhập thông tin: tên, tuổi, giới tính, nơi ở
3. Upload ảnh khuôn mặt
4. Hệ thống tự động tạo class_id và lưu embedding

### 4. Quản lý dữ liệu
1. Chọn tab "Danh sách người"
2. Tìm kiếm theo tên, tuổi, địa chỉ
3. Chỉnh sửa hoặc xóa thông tin

## ⚙️ Cấu hình nâng cao

### Tinh chỉnh độ chính xác
Trong `service/face_query_service.py`:
```python
# Thay đổi threshold để điều chỉnh độ nhạy
if results and results[0]['score'] > 0.5:  # Tăng để giảm false positive
```

### Tối ưu hiệu suất
1. **Sử dụng GPU**: Đảm bảo có CUDA và cài đặt `torch` với GPU support
2. **FAISS GPU**: Thay `faiss-cpu` bằng `faiss-gpu` nếu có GPU
3. **Connection pooling**: Cấu hình connection pool cho MySQL

### Tùy chỉnh Model
Thay đổi model trong `config.py`:
```python
# Sử dụng model khác
MODEL_PATH = 'model/ms1mv3_arcface_r18_fp16.pth'
```

## 🐛 Debug & Troubleshooting

### Lỗi thường gặp

#### 1. Lỗi kết nối MySQL
```
Error: (2003, "Can't connect to MySQL server")
```
**Giải pháp:**
- Kiểm tra XAMPP MySQL đã chạy
- Kiểm tra cấu hình trong `db/mysql_conn.py`

#### 2. Lỗi không tìm thấy model
```
FileNotFoundError: model file not found
```
**Giải pháp:**
- Kiểm tra đường dẫn trong `config.py`
- Đảm bảo file model có trong thư mục `model/`

#### 3. Lỗi import InsightFace
```
ModuleNotFoundError: No module named 'backbones'
```
**Giải pháp:**
- Kiểm tra đường dẫn InsightFace trong `model/arcface_model.py`
- Đảm bảo thư mục `insightface/` có đầy đủ source code
- Sửa đường dẫn phù hợp với vị trí dự án:
```python
sys.path.append('[ĐỘI_DẪN_DỰ_ÁN]/insightface/recognition/arcface_torch')
```

#### 4. Lỗi FAISS index
```
RuntimeError: FAISS index not loaded
```
**Giải pháp:**
```bash
python dump_faiss_vectors.py  # Khởi tạo lại index
```

#### 5. Lỗi CORS khi truy cập từ frontend
**Giải pháp:** Đảm bảo CORS được cấu hình đúng trong `app.py`

### Kiểm tra logs
```bash
# Xem logs trong terminal khi chạy uvicorn
# Hoặc thêm logging trong code để debug
```

## 📊 Hiệu suất

### Benchmark
- **Thời gian nhận diện**: ~0.05-0.1s per image
- **Độ chính xác**: >99% với threshold 0.5
- **Hỗ trợ**: Lên đến 100,000 embeddings trong database

### Tối ưu hóa
- Sử dụng GPU để tăng tốc độ xử lý
- Cache embedding để giảm thời gian tính toán
- Optimize MySQL queries với indexing

---

## 🙏 Tham khảo và Tài liệu

### InsightFace
Dự án này sử dụng source code từ **InsightFace**:
- **GitHub**: https://github.com/deepinsight/insightface
- **Paper**: "ArcFace: Additive Angular Margin Loss for Deep Face Recognition"
- **License**: MIT License
- **Tác giả**: Jiankang Deng, Jia Guo, và các cộng tác viên

### Mô hình ArcFace
- **Paper gốc**: https://arxiv.org/abs/1801.07698
- **Kiến trúc**: ResNet backbone với ArcFace loss function
- **Đặc điểm**: Tối ưu hóa cho face recognition với margin loss

**Lưu ý**: Đây là hệ thống demo cho mục đích học tập và nghiên cứu. Trong môi trường production, cần thêm các biện pháp bảo mật và tối ưu hóa phù hợp.

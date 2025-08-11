# Tài liệu hệ thống Face Recognition - Mô tả chức năng

## 0. Quy trình hoạt động tổng thể

### 0.1. Kiến trúc hệ thống tổng quát
Hệ thống Face Recognition sử dụng kiến trúc 3-tier với Frontend → Backend API → Database/Vector Storage:

```
Frontend (HTML/JS/CSS)
       ↓
FastAPI Backend (Python)
       ↓ ↙ ↘
   MySQL    FAISS    ArcFace Model
```

### 0.2. Workflow chính của hệ thống

**1. Authentication Flow:**
```
User → auth.html → Login/Register → API (/login, /register) → MySQL (taikhoan) → Session → index.html
```

**2. Face Recognition Flow (Query):**
```
User uploads image → Frontend → API (/query) → ArcFace Model (extract embedding) 
→ FAISS (similarity search) → MySQL (get person info) → Return results
```

**3. Add New Person Flow:**
```
User fills form + uploads image → Frontend → API (/add_embedding) 
→ ArcFace Model (extract embedding) → FAISS (add vector) + MySQL (add person info) → Success response
```

**4. Search Person Flow:**
```
User enters search query → Frontend → API (/list_nguoi) → MySQL (search with pagination) → Return results
```

**5. Management Flow (Edit/Delete):**
```
User selects action → Frontend → API (/edit_embedding, /delete_image, /delete_class) 
→ FAISS (update/delete) + MySQL (update/delete) → Sync response
```

### 0.3. Data Flow và Synchronization

**Embedding Pipeline:**
1. **Input:** Raw image file (JPG/PNG)
2. **Processing:** ArcFace model extracts 512-dim embedding
3. **Normalization:** L2 normalization for cosine similarity
4. **Storage:** FAISS index (vectors) + MySQL (metadata)
5. **Retrieval:** Similarity search + metadata lookup

**Metadata Consistency:**
- **FAISS:** Stores image_id, image_path, class_id as metadata
- **MySQL:** Stores detailed person info (ten, tuoi, gioitinh, noio)
- **Sync:** Both systems updated atomically in API operations
- **Backup:** FAISS index + metadata saved to .index/.npz files

### 0.4. Performance và Scalability

**FAISS Optimization:**
- IndexFlatIP cho exact cosine similarity
- L2 normalization cho performance
- Intelligent caching (embeddings, metadata)
- File-based persistence (.index, .npz)

**Database Optimization:**
- Connection pooling với ConnectionHelper
- Prepared statements cho security
- Pagination cho large datasets
- Unicode normalization cho Vietnamese search

**Frontend Optimization:**
- Single-page application (SPA) pattern
- Lazy loading và progressive enhancement
- Real-time validation to reduce API calls
- Client-side caching cho repeated queries

### 0.5. Error Handling và Recovery

**System Resilience:**
- Transaction rollback on database errors
- FAISS index rebuilding on corruption
- Graceful degradation on service unavailability
- Comprehensive error logging

**User Experience:**
- Real-time validation feedback
- Progress indicators for long operations
- Meaningful error messages
- Confirmation dialogs for destructive actions

**Data Integrity:**
- Atomic operations across FAISS + MySQL
- Backup và restore procedures
- Consistency checks on startup
- Automatic index rebuilding when needed

### 0.6. Security Considerations

**Authentication:**
- Username/password authentication
- Session management
- Input validation và sanitization

**File Upload Security:**
- File type validation (images only)
- Size limits (10MB max)
- Safe file handling

**API Security:**
- CORS configuration
- Input validation với Pydantic
- Error message sanitization

## 1. FAISS (Facebook AI Similarity Search)

### 1.1. Giới thiệu và vai trò trong hệ thống
FAISS là thư viện tìm kiếm vector tương tự của Facebook, được sử dụng làm cơ sở dữ liệu vector chính trong hệ thống nhận diện khuôn mặt. Thư viện này cho phép tìm kiếm nhanh chóng các embedding tương tự nhau trong không gian nhiều chiều.

### 1.2. Cấu trúc FaissIndexManager (index/faiss.py)
**Khởi tạo hệ thống:**
- Class `FaissIndexManager` quản lý toàn bộ FAISS operations
- Embedding dimension: 512 (phù hợp với ArcFace model)
- Sử dụng `IndexFlatIP` (Inner Product) để tính cosine similarity
- Attributes chính:
  ```
  - embedding_size: kích thước vector (512)
  - index: FAISS IndexFlatIP object
  - image_ids: danh sách ID ảnh
  - image_paths: đường dẫn file ảnh
  - class_ids: danh sách class ID
  - embeddings: cache embeddings đã chuẩn hóa
  - index_path: đường dẫn file .index
  - meta_path: đường dẫn file .npz metadata
  ```

**Quản lý dữ liệu và metadata:**
- Automatic L2 normalization trước khi add vào index
- Metadata sync: image_ids, image_paths, class_ids, embeddings
- File management: .index (FAISS) + .npz (numpy metadata)
- Intelligent loading: kiểm tra mtime để tránh load không cần thiết

**Thêm embeddings (add_embeddings):**
- Normalize vectors với L2 norm
- Thêm đồng thời vào FAISS index và metadata lists
- Extend embeddings cache để tránh reconstruct

**Tìm kiếm embeddings (query):**
- Input: query vector, top_k
- Normalize query vector trước search
- Return: list với image_id, image_path, class_id, score, faiss_index
- Performance logging với timing

**Tìm kiếm theo string (query_embeddings_by_string):**
- Exact match search theo class_id (case-insensitive)
- Support pagination: page, page_size
- Return all nếu query rỗng
- Output format: total, total_pages, page, page_size, results

**Xóa operations:**
- `delete_by_image_id`: xóa theo image_id, rebuild index
- `delete_by_class_id`: xóa tất cả ảnh của class, rebuild index
- Automatic index reconstruction từ remaining embeddings

**Data management:**
- `load()`: intelligent loading với mtime checking
- `save()`: lưu cả index và metadata
- `reset_index()`: xóa toàn bộ data, giữ file structure
- `check_index_data()`: validation và statistics

**Utilities:**
- `get_image_ids_by_class()`: lấy image_ids theo class_id
- `print_example_vectors()`: debug utility
- Embedding reconstruction nếu metadata corrupted

## 2. MySQL (XAMPP) - Quản lý dữ liệu

### 2.1. Cấu hình kết nối (db/mysql_conn.py)
MySQL đóng vai trò lưu trữ thông tin người dùng, metadata, và thông tin quản lý hệ thống. XAMPP cung cấp môi trường phát triển tích hợp cho MySQL.

**Connection Settings:**
```
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # XAMPP default
MYSQL_DB = 'face_db'
charset = 'utf8mb4'
cursorclass = pymysql.cursors.DictCursor
```

**Connection Helper (db/connection_helper.py):**
- Context manager pattern với `__enter__` và `__exit__`
- Automatic commit/rollback handling
- Auto connection close sau mỗi operation
- Exception-safe database operations

### 2.2. Data Models (db/models.py)

**TaiKhoan Model:**
- Attributes: username (str), passwrd (str)
- `from_row()`: static method tạo object từ MySQL row dict
- Dùng cho authentication system

**Nguoi Model:**
- Attributes: class_id (int), ten (str), tuoi (int), gioitinh (str), noio (str)
- `from_row()`: static method từ MySQL row dict
- `to_dict()`: convert to JSON-serializable dict
- Quản lý thông tin cá nhân liên kết với class_id

### 2.3. Repository Pattern

**TaiKhoanRepository (db/taikhoan_repository.py):**
- `add(taikhoan)`: thêm tài khoản mới
- `get_by_username(username)`: lấy tài khoản theo username
- `check_login(username, passwrd)`: verify login credentials
- Sử dụng ConnectionHelper để manage transactions

**NguoiRepository (db/nguoi_repository.py):**

*CRUD Operations:*
- `add(nguoi)`: INSERT/REPLACE người mới
- `get_by_class_id(class_id)`: lấy thông tin theo class_id
- `delete_by_class_id(class_id)`: xóa người theo class_id

*Search Operations:*
- `search_nguoi(query)`: tìm kiếm theo tên, nơi ở, tuổi, giới tính
- `search_nguoi_paged(query, page, page_size)`: search với pagination
- Unicode normalization để hỗ trợ tiếng Việt không dấu
- LIKE queries với case-insensitive matching

*Advanced Features:*
- `get_total_and_examples(limit)`: thống kê + examples
- `truncate_all()`: xóa toàn bộ data, giữ structure
- Multiple field search: ten, noio, tuoi, gioitinh
- Accent-insensitive Vietnamese search

**Search Implementation Details:**
```python
# Unicode normalization cho tiếng Việt
def remove_accents(input_str):
    return ''.join(
        c for c in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(c) != 'Mn'
    )

# Multi-field search với LIKE
WHERE LOWER(ten) LIKE %s 
   OR LOWER(noio) LIKE %s 
   OR CAST(tuoi AS CHAR) LIKE %s 
   OR CAST(gioitinh AS CHAR) LIKE %s
```

**Pagination Logic:**
- LIMIT/OFFSET cho database-level pagination
- Separate COUNT query để lấy total results
- Page calculation: `offset = (page - 1) * page_size`
- Return format: `{nguoi_list: [...], total: int}`

### 2.4. Database Schema

**Bảng taikhoan:**
```sql
CREATE TABLE taikhoan (
    username VARCHAR(50) PRIMARY KEY,
    passwrd VARCHAR(255) NOT NULL
);
```

**Bảng nguoi:**
```sql
CREATE TABLE nguoi (
    class_id INT PRIMARY KEY,
    ten VARCHAR(255) NOT NULL,
    tuoi INT,
    gioitinh VARCHAR(10),
    noio VARCHAR(500)
);
```

### 2.5. Transaction Management
- ConnectionHelper đảm bảo ACID properties
- Automatic rollback khi có exception
- Commit chỉ khi operation thành công
- Resource cleanup (cursor, connection) guaranteed

## 4. Frontend Interface - Giao diện người dùng

### 4.1. Cấu trúc tổng quan (frontend/)
Frontend sử dụng HTML5, Tailwind CSS, FontAwesome, và vanilla JavaScript để tạo giao diện hiện đại và responsive.

**File Structure:**
```
frontend/
├── index.html          # Main interface với 6 tabs chính
├── auth.html           # Authentication interface
├── assets/style.css    # Basic CSS (minimal)
└── utils/
    ├── main.js         # Core functions, API handling
    ├── upload.js       # Image upload logic
    └── ui.js, api.js, events.js, global-api.js (empty)
```

### 4.2. Main Interface (index.html)

**Design System:**
- **Framework:** Tailwind CSS với custom styles
- **Icons:** FontAwesome 6.4.0
- **Fonts:** Inter font family cho typography hiện đại
- **Color Scheme:** Indigo/blue primary, với accent colors theo từng chức năng

**Layout Architecture:**
- Fixed top navigation với 6 tabs
- Single-page application pattern
- Responsive grid layout (grid-cols-1 lg:grid-cols-2)
- Sharp design philosophy với border-radius: 6px

**Enhanced UI Components:**

*Tab System:*
- Active tab highlighting với gradient background
- Smooth transitions (cubic-bezier easing)
- Sharp indicator bars với gradient effects
- Hover animations với transform effects

*Form Components:*
- Smart file upload areas với drag-and-drop
- Real-time validation với color-coded feedback
- Tooltip system cho contextual help
- Enhanced focus states với ring effects

*Button System:*
- Primary buttons với gradient backgrounds
- Hover animations (translateY + scale)
- Loading states với spinning indicators
- Disabled states với opacity và cursor handling

*Modal System:*
- Confirmation modals với backdrop blur
- Smooth entry/exit animations
- Error/success snackbar notifications
- Global loading overlays

### 4.3. Functional Tabs

**1. Query Tab (Nhận diện)**
- File upload với preview
- Real-time filename display
- Progress indicators
- Result display với JSON formatting

**2. Add Tab (Thêm người mới)**
- Multi-field form: class_id, tên, tuổi, giới tính, nơi ở
- Image upload (optional)
- Real-time validation cho từng field
- Tooltips giải thích chi tiết từng trường

**3. Edit Tab (Sửa thông tin)**
- Image ID lookup required
- Optional file upload cho ảnh mới
- Validation cho existing records

**4. Delete Tab (Xóa đối tượng)**
- Radio button selection: embedding vs class_id
- Confirmation modal với detailed warnings
- Two-step deletion process

**5. Search Nguoi Tab (Tìm kiếm)**
- Fuzzy search across multiple fields
- Pagination support
- Unicode normalization cho tiếng Việt
- Results display trong table format

**6. Reset Tab (Reset Index)**
- Danger zone với multiple warnings
- Confirmation modal với detailed consequences
- Complete FAISS index reset

### 4.4. Form Validation System

**Real-time Validation:**
- `validateImageId()`: unique identifier validation
- `validateClassId()`: person identifier validation
- `validateName()`: Vietnamese name validation
- `validateAge()`: age range validation (1-120)
- `validateLocation()`: address validation
- `validatePath()`: file path validation

**Validation Feedback:**
- Color-coded validation messages
- Dynamic border colors (red/green)
- Inline error/success indicators
- Tooltip guidance cho best practices

### 4.5. Enhanced UX Features

**Sharp Design Elements:**
- Consistent 6px border-radius
- Sharp indicator bars (no rounding)
- Clean geometric forms
- High contrast color relationships

**Animation System:**
- Page transitions với slide-in effects
- Button hover states với transform
- Modal entrance/exit animations
- Loading spinners với smooth rotation

**Responsive Design:**
- Mobile-first approach
- Breakpoint-based layouts
- Touch-friendly interfaces
- Adaptive component sizing

**Accessibility Features:**
- ARIA labels và roles
- Keyboard navigation support
- High contrast text/background
- Screen reader friendly structures

### 4.6. Authentication Interface (auth.html)

**Design Philosophy:**
- Centered layout với gradient background
- Tab-based switching (Login/Register)
- Form animations với sliding transitions
- Consistent validation patterns

**Features:**
- Username/password authentication
- Registration form với validation
- Error handling với snackbar notifications
- Redirect to main interface sau login

**Styling:**
- Gradient backgrounds (linear-gradient 135deg)
- Sharp tab design matching main interface
- Form input styling consistency
- Hover/focus state enhancements

### 4.7. JavaScript Architecture (utils/main.js)

**Core Functions:**

*API Configuration:*
- Dynamic API host detection (localhost vs production)
- Fetch wrapper functions
- Error handling patterns

*UI Utilities:*
- `showLoading()`: loading state management
- `showApiResult()`: result display với formatting
- `showEmptyState()`: empty state handling
- `showSnackbar()`: notification system

*File Handling:*
- `updateFileName()`: file input feedback
- Drag-and-drop support
- File type validation
- Size limit enforcement

*Form Management:*
- Field validation functions
- Form submission handling
- Data serialization
- Error state management

**Upload Logic (utils/upload.js):**
- Simple file upload implementation
- FormData handling
- Fetch API usage cho image submission
- JSON response processing

## 3. FastAPI - Giao diện API

### 3.1. Kiến trúc và vai trò
FastAPI cung cấp RESTful API cho toàn bộ hệ thống, kết nối frontend với backend processing. Hỗ trợ CORS để cho phép truy cập từ nhiều domain khác nhau.

### 3.2. Các endpoint chi tiết

**Authentication (Xác thực):**

1. **POST /login** - Đăng nhập hệ thống
   - **Input:** 
     ```json
     {
       "username": "string (min 6 chars)",
       "passwrd": "string (min 6 chars)"
     }
     ```
   - **Output thành công (200):**
     ```json
     {
       "success": true,
       "message": "Đăng nhập thành công"
     }
     ```
   - **Output thất bại (401):**
     ```json
     {
       "success": false,
       "message": "Sai tên đăng nhập hoặc mật khẩu"
     }
     ```

2. **POST /register** - Đăng ký tài khoản mới
   - **Input:**
     ```json
     {
       "username": "string (min 6 chars)",
       "passwrd": "string (min 6 chars)"
     }
     ```
   - **Output thành công (200):**
     ```json
     {
       "success": true,
       "message": "Đăng ký thành công"
     }
     ```
   - **Output thất bại (400):**
     ```json
     {
       "success": false,
       "message": "Lỗi đăng ký (username đã tồn tại)"
     }
     ```

**Face Query (Truy vấn khuôn mặt):**

3. **POST /query** - Truy vấn khuôn mặt đơn
   - **Input:** Multipart form với file ảnh
     ```
     file: UploadFile (required)
     ```
   - **Output:**
     ```json
     {
       "image_id": "int",
       "image_path": "string",
       "class_id": "int", 
       "score": "float",
       "metadata": "object"
     }
     ```

4. **POST /query_top5** - Truy vấn top 5 khuôn mặt tương tự
   - **Input:** Multipart form với file ảnh
     ```
     file: UploadFile (required)
     ```
   - **Output:**
     ```json
     [
       {
         "image_id": "int",
         "image_path": "string", 
         "class_id": "int",
         "score": "float",
         "rank": "int"
       }
     ]
     ```

**Embedding Management (Quản lý embedding):**

5. **POST /add_embedding** - Thêm embedding mới
   - **Input:** Multipart form
     ```
     image_id: int (required)
     image_path: string (required)
     class_id: int (required)
     ten: string (required)
     gioitinh: boolean (required)
     tuoi: int (required)
     noio: string (required)
     file: UploadFile (required)
     ```
   - **Output:**
     ```json
     {
       "message": "Thêm embedding thành công",
       "image_id": "int",
       "class_id": "int"
     }
     ```

6. **POST /edit_embedding** - Sửa embedding
   - **Input:** Multipart form
     ```
     image_id: int (required)
     image_path: string (optional)
     file: UploadFile (optional)
     ```
   - **Output:**
     ```json
     {
       "message": "Đã cập nhật: embedding, image_path cho image_id=123"
     }
     ```

7. **POST /delete_class** - Xóa class
   - **Input:** Form data
     ```
     class_id: int (required)
     ```
   - **Output:**
     ```json
     {
       "message": "Xóa class thành công",
       "deleted_count": "int"
     }
     ```

8. **POST /delete_image** - Xóa image
   - **Input:** Form data
     ```
     image_id: int (required)
     ```
   - **Output:**
     ```json
     {
       "message": "Xóa image thành công"
     }
     ```

**Search và Info (Tìm kiếm và thông tin):**

9. **GET /search_embeddings** - Tìm kiếm embedding
   - **Input:** Query parameters
     ```
     query: string (optional, default="") - tìm theo image_id, image_path, class_id
     page: int (optional, default=1) - số trang
     page_size: int (optional, default=15, max=15) - số kết quả mỗi trang
     ```
   - **Output:**
     ```json
     {
       "results": [
         {
           "image_id": "int",
           "image_path": "string",
           "class_id": "int",
           "embedding": "array[512]"
         }
       ],
       "total": "int",
       "page": "int",
       "page_size": "int"
     }
     ```

10. **GET /vector_info** - Thông tin vector FAISS
    - **Input:** Không có
    - **Output:**
      ```json
      {
        "total_vectors": "int",
        "embedding_dimension": "int",
        "index_type": "string",
        "memory_usage": "string"
      }
      ```

11. **GET /get_image_ids_by_class** - Lấy image_ids theo class
    - **Input:** Query parameter
      ```
      class_id: string (required)
      ```
    - **Output:**
      ```json
      {
        "class_id": "string",
        "image_ids": ["int", "int", ...],
        "total_count": "int"
      }
      ```

12. **GET /index_status** - Trạng thái FAISS index
    - **Input:** Không có
    - **Output:**
      ```json
      {
        "status": "ready|loading|error",
        "total_vectors": "int",
        "last_updated": "timestamp",
        "index_file_size": "string"
      }
      ```

13. **POST /reset_index** - Reset FAISS index
    - **Input:** Không có
    - **Output:**
      ```json
      {
        "message": "Reset index thành công",
        "new_total_vectors": "int"
      }
      ```

**User Management (Quản lý người dùng):**

14. **GET /list_nguoi** - Danh sách người
    - **Input:** Query parameters
      ```
      query: string (optional, default="") - tìm theo tên, class_id
      page: int (optional, default=1)
      page_size: int (optional, default=15, max=100)
      ```
    - **Output:**
      ```json
      {
        "results": [
          {
            "class_id": "int",
            "ten": "string",
            "gioitinh": "boolean",
            "tuoi": "int", 
            "noio": "string",
            "total_images": "int"
          }
        ]
      }
      ```

### 3.3. Xử lý lỗi và validation
- Tất cả API đều có xử lý exception và trả về status code phù hợp
- Input validation thông qua Pydantic models
- Multipart form handling cho file upload
- JSON response với message descriptive cho debugging

## 4. Frontend - Giao diện người dùng

### 4.1. Kiến trúc và công nghệ
Frontend sử dụng HTML, CSS (Tailwind), JavaScript để tạo giao diện tương tác. Thiết kế responsive và modern với các hiệu ứng smooth.

### 4.2. Các thành phần chính

**Layout và Navigation:**
- Topbar: tiêu đề, search box, user info
- Sidebar: menu chức năng, danh sách class
- Main content: hiển thị kết quả, forms
- Modal: dialog thêm/sửa embedding

**Authentication UI:**
- Form đăng nhập/đăng ký với validation
- Tab switching giữa login/register
- Hiệu ứng transition và feedback
- Error handling và success notification

**Search và Query:**
- Input field với real-time validation
- Upload ảnh để extract embedding
- Hiển thị kết quả dưới dạng card grid
- Pagination cho nhiều kết quả

**Embedding Management:**
- Form thêm embedding với JSON input
- Danh sách embedding với action buttons
- Edit modal với pre-filled data
- Confirm dialog cho delete action

### 4.3. Tương tác với API
**HTTP Requests:**
- Sử dụng fetch API để gọi backend
- Async/await pattern cho code sạch
- Error handling và timeout management
- Loading states và progress indicators

**State Management:**
- Local state cho pagination, search results
- Session storage cho user authentication
- Real-time validation và feedback
- Optimistic updates cho UX tốt hơn

**UI/UX Features:**
- Smooth transitions và animations
- Drag & drop file upload
- Tooltip và snackbar notifications
- Responsive design cho mobile/desktop

## 5. Quy trình hoạt động tổng thể

### 5.1. Quy trình nhận diện khuôn mặt
1. **Upload ảnh:** User upload ảnh qua frontend
2. **Extract embedding:** Sử dụng ArcFace model để tạo vector 512 chiều
3. **Tìm kiếm FAISS:** Query embedding trong FAISS để tìm kết quả tương tự
4. **Trả kết quả:** Hiển thị top-k kết quả với score và thông tin chi tiết
5. **Lưu lịch sử:** Log query và kết quả vào database

### 5.2. Quy trình quản lý dữ liệu
1. **Thêm mới:** Upload ảnh + metadata → Extract embedding → Lưu FAISS + MySQL
2. **Cập nhật:** Load từ FAISS → Modify embedding/metadata → Save lại
3. **Xóa:** Remove từ FAISS + MySQL → Rebuild index nếu cần
4. **Backup:** Định kỳ backup FAISS index và MySQL database

### 5.3. Bảo mật và hiệu năng
**Bảo mật:**
- Hash password với SHA256
- CORS policy cho API access
- Input validation và sanitization
- Session management cho authentication

**Hiệu năng:**
- FAISS indexing cho tìm kiếm nhanh
- Database indexing cho truy vấn SQL
- Caching embedding results
- Lazy loading cho UI components

Tài liệu này mô tả chi tiết cách các module hoạt động trong thực tế dựa trên code hiện có của dự án, thay vì chỉ đưa ra các ví dụ lý thuyết.

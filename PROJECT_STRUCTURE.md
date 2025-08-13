# 📁 Project Structure - Face Recognition API với MySQL Authentication

## 🏗️ Overview
```
face_api/
├── 📄 Core Application Files
├── 🔐 Authentication Module
├── 🚀 API Endpoints
├── 🛠️ Business Logic Services
├── 🗄️ Database Layer
├── 🎨 Frontend Interface
├── 🤖 AI Models & Indexes
├── 📚 Documentation
└── ⚙️ Configuration Files
```

## 📂 Detailed Structure

### 📄 Core Application Files
```
face_api/
├── app.py                    # Main FastAPI application với MySQL auth
├── config.py                 # Application configuration
├── requirements.txt          # Python dependencies (updated)
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
└── __init__.py              # Python package initialization
```

### 🔐 Authentication Module
```
auth/
├── mysql_auth.py            # Core MySQL authentication dependency
├── mysql_auth_api.py        # Login/logout API endpoints
├── mysql_integration.py     # MySQL integration utilities
├── mysql_user_service.py    # User management service
└── __init__.py              # Auth module initialization
```

**Removed JWT Files** (Cleaned up):
- ❌ `jwt_models.py` - JWT data models (not needed)
- ❌ `jwt_utils.py` - JWT utilities (not needed)
- ❌ `oauth2.py` - OAuth2 implementation (not needed)
- ❌ `auth_api.py` - JWT auth endpoints (replaced)
- ❌ `config.py` - JWT config (not needed)
- ❌ `user_service.py` - JWT user service (not needed)

### 🚀 API Endpoints
```
api/
├── face_query.py            # Face recognition query endpoint
├── face_query_top5.py       # Top 5 similar faces
├── add_embedding.py         # Add new person (protected)
├── edit_embedding.py        # Edit person info (protected)
├── delete_class.py          # Delete person (protected)
├── delete_image.py          # Delete specific image (protected)
├── reset_index.py           # Reset FAISS index (protected)
├── list_nguoi.py            # List people (public)
├── search_embeddings.py     # Search embeddings (public)
├── vector_info.py           # Vector database info (public)
├── get_image_ids_by_class.py # Get images by class (public)
├── index_status.py          # System status (public)
└── health.py                # Health check endpoints (public)
```

### 🛠️ Business Logic Services
```
service/
├── face_query_service.py    # Face recognition business logic
├── add_embedding_service.py # Add person business logic
├── edit_embedding_service.py # Edit person business logic
├── delete_service.py        # Delete operations business logic
├── list_nguoi_service.py    # List people business logic
├── shared_instances.py      # Singleton pattern for optimization
└── performance_monitor.py   # Performance tracking service
```

### 🗄️ Database Layer
```
db/
├── mysql_conn.py            # MySQL connection management
├── models.py                # Database models and schemas
├── nguoi_repository.py      # People data access layer
├── class_info.csv           # Sample data file
├── dump_import_class_info_to_mysql.py # Data import utility
└── __init__.py              # Database module initialization
```

**Required Database Tables**:
```sql
-- Authentication table
taikhoan (username, passwrd, created_at, last_login)

-- People information table  
nguoi (class_id, ten, tuoi, gioitinh, noio, created_at, updated_at)
```

### 🎨 Frontend Interface
```
frontend/
├── index.html               # Main application interface
├── auth.html                # Login page (updated for MySQL)
├── assets/
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   └── images/              # Static images
└── utils/
    └── main.js              # Main JavaScript utilities (updated)
```

### 🤖 AI Models & Indexes
```
model/
├── ms1mv3_arcface_r18_fp16.pth        # Primary ArcFace model
└── glint360k_cosface_r18_fp16_0.1.pth # Backup model

index/
├── faiss_db_r18.index       # FAISS vector index
├── faiss_db_r18_meta.npz    # FAISS metadata
└── faiss.py                 # FAISS management class

insightface/                 # InsightFace source code
├── recognition/             # Face recognition modules
│   └── arcface_torch/       # ArcFace implementation
├── detection/               # Face detection modules
└── python-package/          # Python package
```

### 📚 Documentation
```
📚 Documentation Files:
├── README.md                # Main documentation (updated)
├── API_DOCUMENTATION.md     # Complete API reference (new)
├── INSTALLATION.md          # Installation guide (updated)
├── CHANGELOG.md             # Version history (updated)
└── PROJECT_STRUCTURE.md     # This file
```

**Removed Documentation** (Cleaned up):
- ❌ `README_MySQL_Auth.md` - Duplicate
- ❌ `README_NEW.md` - Duplicate  
- ❌ `doc_face_api.md` - Outdated
- ❌ `detailed_documentation.md` - Merged
- ❌ `system_documentation.md` - Merged
- ❌ `API_DOCUMENTATION_SUMMARY.md` - Replaced
- ❌ `CODE_LOGIC_ANALYSIS.md` - Not needed
- ❌ `FINAL_VALIDATION_REPORT.md` - Not needed
- ❌ `SINGLETON_ARCHITECTURE.md` - Merged
- ❌ `UPDATE_SUMMARY.md` - Not needed

### ⚙️ Configuration Files
```
🔧 Configuration:
├── .env.example             # Environment template (updated)
├── .gitignore               # Git ignore rules
├── pytest.ini              # Testing configuration
└── config.py                # Application config (updated)
```

### 🧹 Cleaned Up Files
**Removed Application Files**:
- ❌ `app_fixed.py` - Development version
- ❌ `app_simple.py` - Simplified version
- ❌ `app_mysql.py` - Merged into main app.py

**Removed Test/Development Files**:
- ❌ `setup_jwt.py` - JWT setup script
- ❌ `test_jwt_health.py` - JWT testing
- ❌ `test_mysql_auth.py` - Development test
- ❌ `test_startup.py` - Startup test
- ❌ `validate_system.py` - System validation
- ❌ `diagnose.py` - Diagnostic script
- ❌ `cleanup_project.py` - Project cleanup script

---

## 🔄 Data Flow Architecture

### Authentication Flow
```
1. POST /auth/login → MySQL taikhoan table → Generate session token
2. Protected API call → Bearer token validation → MySQL lookup
3. POST /auth/logout → Clear session token
```

### Face Recognition Flow
```
1. Upload image → Face detection → Feature extraction
2. FAISS vector search → Find similar faces
3. Return person info from MySQL nguoi table
```

### Data Management Flow
```
1. Authentication check → MySQL validation
2. CRUD operations → MySQL nguoi table + FAISS index
3. Audit logging → Performance monitoring
```

---

## 🎯 Key Features After Cleanup

### ✅ What's Included
- **MySQL Authentication**: Session-based với bearer tokens
- **Face Recognition**: ArcFace model với FAISS search
- **API Documentation**: Complete Swagger UI integration  
- **Security**: Headers, CORS, authentication middleware
- **Frontend**: Web interface với proper token handling
- **Performance**: Optimized với shared instances pattern
- **Documentation**: Comprehensive guides và references

### ❌ What's Removed
- JWT authentication complexity
- Unused development files
- Duplicate documentation
- Obsolete test scripts
- Role-based permission systems
- OAuth2 implementation

---

## 🚀 Production Ready

The cleaned up project structure is now:
- **Simplified**: No unnecessary complexity
- **Focused**: MySQL authentication only
- **Documented**: Complete documentation set
- **Tested**: Core functionality verified
- **Secure**: Proper authentication và security headers
- **Maintainable**: Clean code structure
- **Scalable**: Optimized performance patterns

**Total Files**: ~50+ files organized trong logical structure  
**Documentation**: 5 key documentation files  
**Authentication**: Simple MySQL session-based system  
**APIs**: Public/Protected classification rõ ràng

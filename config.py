# Face Recognition API - Configuration
# Version: 2.0.0 - MySQL Authentication System
# Updated: August 2025

# AI Model Configuration
MODEL_PATH = 'model/ms1mv3_arcface_r18_fp16.pth'  # Primary ArcFace model
BACKUP_MODEL_PATH = 'model/glint360k_cosface_r18_fp16_0.1.pth'  # Backup model
AGE_MODEL=  'model/ModelAge.pth' # Age prediction model
GENDER_MODEL = 'model/ModelGender.pth' # Gender prediction model


# FAISS Vector Database Configuration
FAISS_INDEX_PATH = 'index/faiss_db_r18.index'
FAISS_META_PATH = 'index/faiss_db_r18_meta.npz'

# Application Configuration
IMAGES_LIST = 'images.txt'
THRESHOLD = 0.5  # Face recognition confidence threshold

# Authentication Configuration
AUTH_TABLE = 'taikhoan'
AUTH_USERNAME_FIELD = 'username'
AUTH_PASSWORD_FIELD = 'passwrd'

# API Configuration
API_TITLE = "🤖 Hệ Thống Nhận Diện Khuôn Mặt với MySQL Authentication"
API_VERSION = "2.0.0"
API_DESCRIPTION = "Face Recognition API với MySQL session-based authentication"

# Security Configuration
CORS_ORIGINS = ["*"]  # In production, specify exact origins
ALLOW_CREDENTIALS = False  # False for token-based auth
SECURITY_HEADERS = True

# Performance Configuration
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_FORMATS = ["image/jpeg", "image/png", "image/jpg"]
PERFORMANCE_MONITORING = True 
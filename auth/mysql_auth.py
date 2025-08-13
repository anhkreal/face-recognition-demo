"""
Simple MySQL-based Authentication Service
File: auth/mysql_auth.py
"""

from fastapi import HTTPException, status, Depends, Request, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer
from typing import Optional
import secrets
import hashlib
from db.taikhoan_repository import TaiKhoanRepository

# Simple session storage (in production, use Redis or database)
active_sessions = {}

class MySQLAuthService:
    def __init__(self):
        self.repo = TaiKhoanRepository()
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Kiểm tra đăng nhập với MySQL database"""
        try:
            return self.repo.check_login(username, password)
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def create_session(self, username: str) -> str:
        """Tạo session token cho user đã đăng nhập"""
        session_token = secrets.token_urlsafe(32)
        active_sessions[session_token] = {
            "username": username,
            "created_at": __import__("time").time()
        }
        return session_token
    
    def get_current_user(self, session_token: Optional[str]) -> Optional[str]:
        """Lấy username từ session token"""
        if not session_token or session_token not in active_sessions:
            return None
        
        session_data = active_sessions[session_token]
        # Check if session expired (24 hours)
        if __import__("time").time() - session_data["created_at"] > 86400:
            del active_sessions[session_token]
            return None
        
        return session_data["username"]
    
    def logout(self, session_token: str):
        """Đăng xuất - xóa session"""
        if session_token in active_sessions:
            del active_sessions[session_token]

# Global auth service instance
mysql_auth = MySQLAuthService()

# Dependency để check authentication từ Authorization header
def get_current_user_mysql(authorization: Optional[str] = Header(None)):
    """FastAPI Dependency để check user đã đăng nhập chưa"""
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chưa đăng nhập hoặc session đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.replace("Bearer ", "")
    username = mysql_auth.get_current_user(token)
    
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chưa đăng nhập hoặc session đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username

# Optional dependency (không bắt buộc đăng nhập)
def get_current_user_optional(authorization: Optional[str] = Header(None)):
    """FastAPI Dependency để check user (optional)"""
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        return mysql_auth.get_current_user(token)
    return None

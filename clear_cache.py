"""
Clear Python Cache Script
File: clear_cache.py
"""

import os
import shutil

def clear_python_cache():
    """Dọn dẹp tất cả __pycache__ directories"""
    
    base_path = r"c:\Users\DELL\Downloads\archive\face_api"
    
    print("🧹 Clearing Python cache directories...")
    
    cache_count = 0
    for root, dirs, files in os.walk(base_path):
        if "__pycache__" in dirs:
            cache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(cache_path)
                print(f"   ✅ Cleared: {cache_path}")
                cache_count += 1
            except Exception as e:
                print(f"   ❌ Error clearing {cache_path}: {e}")
    
    print(f"\n✅ Cleared {cache_count} cache directories")
    print("🚀 Python cache cleared. Try running the server again.")

if __name__ == "__main__":
    clear_python_cache()

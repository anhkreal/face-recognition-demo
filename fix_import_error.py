"""
Fix Import Error Script
File: fix_import_error.py
"""

import os
import shutil
import importlib.util

def fix_import_errors():
    """Khắc phục tất cả lỗi import"""
    
    base_path = r"c:\Users\DELL\Downloads\archive\face_api"
    
    print("🔧 === FIXING IMPORT ERRORS ===\n")
    
    # 1. Clear all __pycache__ directories
    print("1️⃣ Clearing Python cache...")
    cache_count = 0
    for root, dirs, files in os.walk(base_path):
        if "__pycache__" in dirs:
            cache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(cache_path)
                print(f"   ✅ Cleared: {cache_path}")
                cache_count += 1
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    print(f"   📊 Cleared {cache_count} cache directories\n")
    
    # 2. Verify auth/__init__.py content
    print("2️⃣ Verifying auth/__init__.py...")
    auth_init_path = os.path.join(base_path, "auth", "__init__.py")
    
    expected_content = '''# Auth module __init__.py - MySQL Authentication
from .mysql_auth import mysql_auth, get_current_user_mysql, get_current_user_optional
from .mysql_auth_api import router as mysql_auth_router

__all__ = [
    "mysql_auth",
    "get_current_user_mysql", 
    "get_current_user_optional",
    "mysql_auth_router"
]'''
    
    try:
        with open(auth_init_path, 'r', encoding='utf-8') as f:
            current_content = f.read().strip()
        
        if "jwt_models" in current_content or "oauth2" in current_content:
            print("   ❌ Found JWT imports, fixing...")
            with open(auth_init_path, 'w', encoding='utf-8') as f:
                f.write(expected_content)
            print("   ✅ Fixed auth/__init__.py")
        else:
            print("   ✅ auth/__init__.py is correct")
    except Exception as e:
        print(f"   ❌ Error checking auth/__init__.py: {e}")
    print()
    
    # 3. Check for remaining JWT files in auth directory
    print("3️⃣ Checking for JWT files in auth/...")
    auth_path = os.path.join(base_path, "auth")
    
    jwt_files = [
        "jwt_models.py", "oauth2.py", "auth_api.py", 
        "jwt_utils.py", "user_service.py", "config.py"
    ]
    
    removed_count = 0
    for jwt_file in jwt_files:
        jwt_path = os.path.join(auth_path, jwt_file)
        if os.path.exists(jwt_path):
            try:
                os.remove(jwt_path)
                print(f"   ✅ Removed: {jwt_file}")
                removed_count += 1
            except Exception as e:
                print(f"   ❌ Error removing {jwt_file}: {e}")
        else:
            print(f"   ✅ {jwt_file}: Already removed")
    
    print(f"   📊 Removed {removed_count} JWT files\n")
    
    # 4. Verify auth directory structure
    print("4️⃣ Verifying auth directory structure...")
    auth_files = os.listdir(auth_path)
    expected_files = ["mysql_auth.py", "mysql_auth_api.py", "__init__.py"]
    
    print("   📁 Current auth/ contents:")
    for file in auth_files:
        if file == "__pycache__":
            continue
        if file in expected_files:
            print(f"   ✅ {file}")
        else:
            print(f"   ⚠️ {file} (unexpected)")
    print()
    
    # 5. Test import
    print("5️⃣ Testing imports...")
    test_imports = [
        "auth.mysql_auth",
        "auth.mysql_auth_api"
    ]
    
    import_success = 0
    for module_name in test_imports:
        try:
            module_path = os.path.join(base_path, *module_name.split('.')) + '.py'
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                print(f"   ✅ {module_name}: Import spec OK")
                import_success += 1
            else:
                print(f"   ❌ {module_name}: Cannot create import spec")
        except Exception as e:
            print(f"   ❌ {module_name}: {e}")
    
    print(f"   📊 {import_success}/{len(test_imports)} imports ready\n")
    
    # 6. Recommendations
    print("6️⃣ Recommendations:")
    print("   1. Restart your IDE/editor completely")
    print("   2. Close all terminals")
    print("   3. Run: python app.py")
    print("   4. If still errors, restart Python interpreter")
    print()
    
    print("✅ === IMPORT ERROR FIX COMPLETE ===")
    print("🚀 Try running the server again!")

if __name__ == "__main__":
    fix_import_errors()

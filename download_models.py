"""
Railway Model Download Script
Download model files khi deploy tren Railway
"""

import os
import urllib.request
import zipfile
from pathlib import Path

# URLs de download models (thay the bang URLs thuc te)
MODEL_URLS = {
    "glint360k_cosface_r18_fp16_0.1.pth": "https://your-storage/models/glint360k_cosface_r18_fp16_0.1.pth",
    "ModelAge.pth": "https://your-storage/models/ModelAge.pth", 
    "ModelGender.pth": "https://your-storage/models/ModelGender.pth",
    "faiss_db_r18.index": "https://your-storage/index/faiss_db_r18.index",
    "faiss_db_r18_meta.npz": "https://your-storage/index/faiss_db_r18_meta.npz"
}

def download_file(url, filepath):
    """Download file from URL"""
    print(f"Downloading {filepath}...")
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        urllib.request.urlretrieve(url, filepath)
        print(f"Downloaded {filepath}")
        return True
    except Exception as e:
        print(f"Failed to download {filepath}: {str(e)}")
        return False

def download_models():
    """Download all model files"""
    print("Starting model download for Railway...")
    
    # Tao directories
    os.makedirs("model", exist_ok=True)
    os.makedirs("index", exist_ok=True)
    
    success_count = 0
    for filename, url in MODEL_URLS.items():
        if filename.endswith('.pth') or filename.endswith('.onnx'):
            filepath = f"model/{filename}"
        else:
            filepath = f"index/{filename}"
        
        # Skip if file already exists
        if os.path.exists(filepath):
            print(f"{filename} already exists, skipping...")
            success_count += 1
            continue
        
        if download_file(url, filepath):
            success_count += 1
    
    print(f"Downloaded {success_count}/{len(MODEL_URLS)} files successfully!")
    return success_count == len(MODEL_URLS)

if __name__ == "__main__":
    download_models()

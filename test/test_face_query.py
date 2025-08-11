import requests
import os
import time
from tqdm import tqdm

IMAGES_LIST = 'images.txt'  # File chứa danh sách đường dẫn ảnh
API_URL = 'http://127.0.0.1:8000/query'
MAX_IMAGES = 1000

def test_face_query(image_path, url=API_URL):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        start = time.time()
        response = requests.post(url, files=files)
        elapsed = time.time() - start
        return response.status_code, response.json(), elapsed

if __name__ == '__main__':
    if not os.path.exists(IMAGES_LIST):
        print(f'Không tìm thấy file: {IMAGES_LIST}')
        exit(1)
    with open(IMAGES_LIST, 'r') as f:
        image_paths = [line.strip().split()[-1] for line in f if line.strip()]
    image_paths = image_paths[:MAX_IMAGES]
    total_time = 0
    success = 0
    for idx, img_path in enumerate(tqdm(image_paths, desc='Testing images', unit='img'), 1):
        if not os.path.exists(img_path):
            print(f'[{idx}] Không tìm thấy file ảnh: {img_path}')
            continue
        status, resp, elapsed = test_face_query(img_path)
        # print(f'[{idx}] {img_path} | Status: {status} | Time: {elapsed:.3f}s | Result: {resp}')
        total_time += elapsed
        success += 1
    if success > 0:
        print(f'--- Tổng số ảnh test: {success} ---')
        print(f'Thời gian trung bình xử lý 1 ảnh: {total_time/success:.3f}s')
    else:
        print('Không có ảnh nào được test thành công.')

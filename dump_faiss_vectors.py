import numpy as np
import pandas as pd
from index.faiss import FaissIndexManager
from config import *
import os

print("Kiểm tra tồn tại file index:", os.path.exists('face_api/index/faiss_db_r18.index'))
print("Bắt đầu load FAISS index và metadata...")
faiss_manager = FaissIndexManager(embedding_size=512, index_path='face_api/'+FAISS_INDEX_PATH, meta_path='face_api/'+FAISS_META_PATH)
faiss_manager.load()
print(f'Số lượng vector: {len(faiss_manager.image_ids)}')

print("Bắt đầu reconstruct vector...")

N = 2000
total = len(faiss_manager.image_ids)
vectors = []
# Lấy 2000 đầu
for idx, (id, path, cid) in enumerate(zip(faiss_manager.image_ids, faiss_manager.image_paths, faiss_manager.class_ids)):
    if idx >= N:
        break
    if (idx+1) % 1000 == 0:
        print(f'  Đã reconstruct {idx+1} vector đầu...')
    try:
        vec = faiss_manager.index.reconstruct(idx)
    except Exception as e:
        print(f'  Lỗi reconstruct vector idx={idx}: {e}')
        continue
    vectors.append({
        'image_id': id,
        'image_path': path,
        'class_id': cid,
        'vector': vec.tolist()
    })
# Lấy 2000 cuối
for idx, (id, path, cid) in enumerate(zip(faiss_manager.image_ids, faiss_manager.image_paths, faiss_manager.class_ids)):
    if idx < total - N:
        continue
    if (idx - (total-N)+1) % 1000 == 0:
        print(f'  Đã reconstruct {idx+1} vector cuối...')
    try:
        vec = faiss_manager.index.reconstruct(idx)
    except Exception as e:
        print(f'  Lỗi reconstruct vector idx={idx}: {e}')
        continue
    vectors.append({
        'image_id': id,
        'image_path': path,
        'class_id': cid,
        'vector': vec.tolist()
    })
print(f'Hoàn thành reconstruct {len(vectors)} vector.')

print("Chuyển thành DataFrame...")
rows = []
for idx, v in enumerate(vectors, 1):
    if idx % 1000 == 0:
        print(f'  Đã chuyển {idx} vector vào DataFrame...')
    row = {
        'vector_id': v['image_id'],  # id FAISS gốc
        'image_id': v['image_id'],
        'image_path': v['image_path'],
        'class_id': v['class_id']
    }
    for i, val in enumerate(v['vector'][:10]):
        row[f'vec_{i}'] = val
    rows.append(row)
df = pd.DataFrame(rows)

print("Ghi ra file CSV...")
csv_path = 'faiss_vectors_dump.csv'
df.to_csv(csv_path, index=False)
print(f'Đã ghi toàn bộ vector và thông tin ra file {csv_path}')

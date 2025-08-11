import numpy as np
import faiss
import os
import pandas as pd


class FaissIndexManager:
    def reset_index(self):
        """
        Xóa toàn bộ dữ liệu FAISS index và metadata
        """
        self.index = faiss.IndexFlatIP(self.embedding_size)
        self.image_ids = []
        self.image_paths = []
        self.class_ids = []
        self.embeddings = []
        # Làm trống file index và metadata, giữ cấu trúc file
        if self.index_path:
            faiss.write_index(self.index, self.index_path)
        if self.meta_path:
            np.savez(self.meta_path,
                     image_ids=np.array([]),
                     image_paths=np.array([]),
                     class_ids=np.array([]),
                     embeddings=np.array([], dtype=np.float32))
        print('Đã làm trống FAISS index và metadata, giữ cấu trúc file.')
    def __init__(self, embedding_size, index_path=None, meta_path=None):
        self.embedding_size = embedding_size
        self.index = faiss.IndexFlatIP(embedding_size)
        self.image_ids = []
        self.image_paths = []
        self.class_ids = []
        self.embeddings = []
        self.index_path = index_path
        self.meta_path = meta_path

    def add_embeddings(self, embeddings, image_ids, image_paths, class_ids):
        embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        self.index.add(embeddings_norm.astype(np.float32))
        self.image_ids.extend(image_ids)
        self.image_paths.extend(image_paths)
        self.class_ids.extend(class_ids)
        if len(self.embeddings) == 0:
            self.embeddings = embeddings_norm.tolist()
        else:
            self.embeddings.extend(embeddings_norm.tolist())

    def save(self):
        faiss.write_index(self.index, self.index_path)
        np.savez(self.meta_path,
                 image_ids=np.array(self.image_ids),
                 image_paths=np.array(self.image_paths),
                 class_ids=np.array(self.class_ids),
                 embeddings=np.array(self.embeddings, dtype=np.float32))

    def load(self):
        idx = faiss.read_index(self.index_path)
        self.index = idx
        meta = np.load(self.meta_path, allow_pickle=True)
        self.image_ids = list(meta['image_ids']) if 'image_ids' in meta else []
        self.image_paths = list(meta['image_paths']) if 'image_paths' in meta else []
        self.class_ids = list(meta['class_ids']) if 'class_ids' in meta else []
        if 'embeddings' in meta and meta['embeddings'].shape[0] == len(self.image_ids):
            self.embeddings = meta['embeddings'].tolist()
        else:
            print('Embeddings bị thiếu hoặc không khớp, reconstruct lại từ FAISS index...')
            self.embeddings = []
            for i in range(len(self.image_ids)):
                self.embeddings.append(self.index.reconstruct(i).tolist())
        print(f'LOAD: số lượng embeddings : {len(self.embeddings)}')
    def delete_by_image_id(self, image_id):
        image_id = str(image_id)
        if image_id not in [str(i) for i in self.image_ids]:
            print(f'image_id {image_id} không tồn tại!')
            return False
        idx = [str(i) for i in self.image_ids].index(str(image_id))
        print(f"image_ids: {self.image_ids[:10]}")
        print(f"idx: {idx}, len(image_ids): {len(self.image_ids)}, len(image_paths): {len(self.image_paths)}, len(class_ids): {len(self.class_ids)}, len(embeddings): {len(self.embeddings)}")
        del self.image_ids[idx]
        del self.image_paths[idx]
        del self.class_ids[idx]
        del self.embeddings[idx]
        self.index = faiss.IndexFlatIP(self.embedding_size)
        if len(self.embeddings) > 0:
            self.index.add(np.array(self.embeddings, dtype=np.float32))
        print(f'Đã xóa vector với image_id={image_id} tại vị trí {idx} và rebuild index.')
        return True

    def delete_by_class_id(self, class_id):
        """
        Xóa toàn bộ ảnh có class_id chỉ định và rebuild lại FAISS index
        """
        class_id = str(class_id)
        # Lấy các chỉ số cần xóa
        idxs_to_delete = [i for i, cls in enumerate(self.class_ids) if str(cls) == class_id]
        if not idxs_to_delete:
            print(f'class_id {class_id} không tồn tại!')
            return False
        print(f'Số lượng ảnh sẽ xóa: {len(idxs_to_delete)}')
        # Xóa các phần tử metadata tại các vị trí index
        self.image_ids = [img_id for i, img_id in enumerate(self.image_ids) if i not in idxs_to_delete]
        self.image_paths = [img_path for i, img_path in enumerate(self.image_paths) if i not in idxs_to_delete]
        self.class_ids = [cls for i, cls in enumerate(self.class_ids) if i not in idxs_to_delete]
        self.embeddings = [emb for i, emb in enumerate(self.embeddings) if i not in idxs_to_delete]
        # Rebuild lại FAISS index từ embeddings còn lại
        self.index = faiss.IndexFlatIP(self.embedding_size)
        if len(self.embeddings) > 0:
            self.index.add(np.array(self.embeddings, dtype=np.float32))
        print(f'Đã xóa toàn bộ ảnh với class_id={class_id} và rebuild index.')
        return True
    def query(self, query_emb, topk=5):
        import time
        print(f'--- FAISS query ---')
        print(f'Số lượng vector trong index: {self.index.ntotal}')
        start = time.time()
        query_emb_norm = query_emb / np.linalg.norm(query_emb)
        D, I = self.index.search(query_emb_norm.reshape(1, -1).astype(np.float32), topk)
        print(f'Thời gian search FAISS: {time.time() - start:.3f}s')
        results = []
        for idx, dist in zip(I[0], D[0]):
            if idx >= 0 and idx < len(self.image_ids):
                results.append({
                    'image_id': self.image_ids[idx],
                    'image_path': self.image_paths[idx],
                    'class_id': self.class_ids[idx],
                    'score': dist,
                    'faiss_index': idx
                })
        print(f'Kết quả truy vấn: {results}')
        return results

    def print_example_vectors(self, n=5):
        print('Ví dụ một số vector trong FAISS index:')
        for i in range(min(n, len(self.image_paths))):
            vec = self.index.reconstruct(i)
            image_id = self.image_ids[i] if i < len(self.image_ids) else None
            image_path = self.image_paths[i]
            class_id = self.class_ids[i]
            norm = np.linalg.norm(vec)
            print(f'Vector {i}:')
            print(f'  image_id: {image_id}')
            print(f'  image_path: {image_path}')
            print(f'  class_id: {class_id}')
            # print(f'  norm: {norm:.4f}')
            print(f'  values[:10]: {vec[:10]} ...')
    def check_index_data(self):
        result = {
            'num_vectors': self.index.ntotal,
            'num_image_ids': len(self.image_ids),
            'num_image_paths': len(self.image_paths),
            'num_class_ids': len(self.class_ids),
            'num_embeddings': len(self.embeddings),
            'num_unique_image_ids': len(set(self.image_ids)),
            'num_unique_image_paths': len(set(self.image_paths)),
            'num_unique_class_ids': len(set(self.class_ids)),
        }
        # Kiểm tra vector NaN và min/max
        if self.index.ntotal > 0:
            vecs = np.zeros((self.index.ntotal, self.embedding_size), dtype=np.float32)
            for i in range(self.index.ntotal):
                vecs[i] = self.index.reconstruct(i)
            result['num_nan_vectors'] = int(np.isnan(vecs).any(axis=1).sum())
            result['min_vector_value'] = float(vecs.min())
            result['max_vector_value'] = float(vecs.max())
        else:
            result['num_nan_vectors'] = 0
            result['min_vector_value'] = None
            result['max_vector_value'] = None
        return result
    def get_image_ids_by_class(self, class_id):
        """
        Trả về danh sách image_id có class trùng với class_id được truy vấn
        """
        class_id = str(class_id)
        return [str(img_id) for img_id, cls in zip(self.image_ids, self.class_ids) if str(cls) == class_id]
## Module only: import and use FaissIndexManager from another file



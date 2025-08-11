import os
import numpy as np
import cv2
from index.faiss import FaissIndexManager
from config import FAISS_INDEX_PATH, FAISS_META_PATH
from model.arcface_model import ArcFaceFeatureExtractor
from config import MODEL_PATH
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
def extract_embedding(image_path):
    img = cv2.imread(image_path)
    extractor = ArcFaceFeatureExtractor(model_path=MODEL_PATH, device=None)
    return extractor.extract(img)

def test_edit_embedding_and_query():
    faiss_manager = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
    faiss_manager.load()
    image_id = 2
    idxs = [i for i, img_id in enumerate(faiss_manager.image_ids) if str(img_id) == str(image_id)]
    if not idxs:
        print(f"Không tìm thấy image_id={image_id} trong FAISS")
        return
    idx = idxs[0]
    print(f"Trước khi chỉnh sửa:")
    print("image_path:", faiss_manager.image_paths[idx])
    print("embedding[:10]:", faiss_manager.embeddings[idx][:10])
    # Trích xuất embedding từ ảnh 8
    emb_8 = extract_embedding(r"C:\Users\DELL\Downloads\archive\casia-webface\000000\00000008.jpg")
    faiss_manager.embeddings[idx] = emb_8
    faiss_manager.image_paths[idx] = "casia-webface/000000/00000008.jpg"
    faiss_manager.save()
    faiss_manager.load()
    print(f"Sau khi chỉnh sửa:")
    print("image_path:", faiss_manager.image_paths[idx])
    print("embedding[:10]:", faiss_manager.embeddings[idx][:10])
    # Query lại bằng ảnh 2
    emb_2 = extract_embedding(r"C:\Users\DELL\Downloads\archive\casia-webface\000000\00000002.jpg")
    print("emb_2[:10]:", emb_2[:10])
    print("emb_8[:10]:", emb_8[:10])
    results_2 = faiss_manager.query(emb_2, topk=1)
    print("Query bằng ảnh 2:", results_2)
    # Query lại bằng ảnh 8
    results_8 = faiss_manager.query(emb_8, topk=1)
    print("Query bằng ảnh 8:", results_8)

if __name__ == "__main__":
    test_edit_embedding_and_query()

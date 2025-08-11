import numpy as np
import cv2
import faiss
from index.faiss import FaissIndexManager
from config import *
from model.arcface_model import ArcFaceFeatureExtractor
from db.nguoi_repository import NguoiRepository
from db.models import Nguoi

def edit_embedding_service(input, file):
    faiss_manager = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
    faiss_manager.load()
    nguoi_repo = NguoiRepository()
    
    # Kiểm tra tồn tại image_id
    if str(input.image_id) not in [str(id) for id in faiss_manager.image_ids]:
        return {"message": f"image_id {input.image_id} không tồn tại!", "status_code": 404}
    
    try:
        idxs = [i for i, img_id in enumerate(faiss_manager.image_ids) if str(img_id) == str(input.image_id)]
        if not idxs:
            return {"message": f"Không tìm thấy index cho image_id {input.image_id}", "status_code": 404}
        
        idx = idxs[0]
        updated_fields = []
        
        print(f"=== DEBUG: Edit Embedding cho image_id={input.image_id} tại index={idx} ===")
        
        # Debug: In thông tin trước khi cập nhật
        old_embedding = faiss_manager.embeddings[idx] if idx < len(faiss_manager.embeddings) else None
        if old_embedding:
            old_embedding_norm = np.linalg.norm(old_embedding)
            print(f"Embedding cũ - Index: {idx}")
            print(f"  - Norm: {old_embedding_norm:.6f}")
            print(f"  - First 10 values: {np.array(old_embedding)[:10]}")
            print(f"  - Last 10 values: {np.array(old_embedding)[-10:]}")
            
            # Verify với FAISS index
            faiss_old_vector = faiss_manager.index.reconstruct(idx)
            faiss_old_norm = np.linalg.norm(faiss_old_vector)
            print(f"FAISS vector cũ - Index: {idx}")
            print(f"  - Norm: {faiss_old_norm:.6f}")
            print(f"  - First 10 values: {faiss_old_vector[:10]}")
            print(f"  - Match với embedding: {np.allclose(old_embedding, faiss_old_vector, atol=1e-6)}")
        
        # Cập nhật embedding nếu file ảnh được gửi lên
        if file is not None and hasattr(file, 'file'):
            try:
                image_bytes = file.file.read()
                np_img = np.frombuffer(image_bytes, np.uint8)
                img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
                
                if img is None:
                    return {"message": "Không thể decode ảnh!", "status_code": 400}
                
                extractor = ArcFaceFeatureExtractor(model_path=MODEL_PATH, device=None)
                new_embedding = extractor.extract(img)
                
                # L2 normalization (quan trọng!)
                new_embedding_norm = new_embedding / np.linalg.norm(new_embedding)
                
                print(f"Embedding mới:")
                print(f"  - Original norm: {np.linalg.norm(new_embedding):.6f}")
                print(f"  - Normalized norm: {np.linalg.norm(new_embedding_norm):.6f}")
                print(f"  - First 10 values: {new_embedding_norm[:10]}")
                print(f"  - Last 10 values: {new_embedding_norm[-10:]}")
                
                # Cập nhật embedding trong memory
                faiss_manager.embeddings[idx] = new_embedding_norm.tolist()
                
                # QUAN TRỌNG: Rebuild FAISS index với embeddings mới
                print("Rebuilding FAISS index với embedding mới...")
                faiss_manager.index = faiss_manager.index.__class__(faiss_manager.embedding_size)
                if len(faiss_manager.embeddings) > 0:
                    embeddings_array = np.array(faiss_manager.embeddings, dtype=np.float32)
                    faiss_manager.index.add(embeddings_array)
                    print(f"FAISS index rebuilt với {faiss_manager.index.ntotal} vectors")
                
                # Verify embedding đã được cập nhật
                updated_faiss_vector = faiss_manager.index.reconstruct(idx)
                updated_faiss_norm = np.linalg.norm(updated_faiss_vector)
                print(f"FAISS vector sau update:")
                print(f"  - Norm: {updated_faiss_norm:.6f}")
                print(f"  - First 10 values: {updated_faiss_vector[:10]}")
                print(f"  - Match với embedding mới: {np.allclose(new_embedding_norm, updated_faiss_vector, atol=1e-6)}")
                
                # Test query với chính embedding này
                test_query_results = faiss_manager.query(new_embedding_norm, topk=3)
                print(f"Test query results:")
                for i, result in enumerate(test_query_results):
                    print(f"  Rank {i+1}: image_id={result['image_id']}, score={result['score']:.6f}")
                
                updated_fields.append('embedding')
                
            except Exception as e:
                print(f"Lỗi chi tiết khi trích xuất embedding: {str(e)}")
                import traceback
                traceback.print_exc()
                return {"message": f"Lỗi trích xuất embedding: {e}", "status_code": 500}
        
        # Cập nhật image_path nếu truyền lên và không rỗng
        if hasattr(input, 'image_path') and input.image_path:
            old_path = faiss_manager.image_paths[idx]
            faiss_manager.image_paths[idx] = input.image_path
            print(f"Updated image_path: '{old_path}' -> '{input.image_path}'")
            updated_fields.append('image_path')
        
        # Lưu thay đổi
        print("Saving changes to files...")
        faiss_manager.save()
        
        # Verification sau khi save
        print("=== VERIFICATION AFTER SAVE ===")
        faiss_manager_verify = FaissIndexManager(embedding_size=512, index_path=FAISS_INDEX_PATH, meta_path=FAISS_META_PATH)
        faiss_manager_verify.load()
        
        # Tìm lại index sau khi load
        verify_idxs = [i for i, img_id in enumerate(faiss_manager_verify.image_ids) if str(img_id) == str(input.image_id)]
        if verify_idxs:
            verify_idx = verify_idxs[0]
            verify_vector = faiss_manager_verify.index.reconstruct(verify_idx)
            verify_embedding = faiss_manager_verify.embeddings[verify_idx]
            print(f"Verification - image_id={input.image_id} at index={verify_idx}")
            print(f"  - FAISS norm: {np.linalg.norm(verify_vector):.6f}")
            print(f"  - Embedding norm: {np.linalg.norm(verify_embedding):.6f}")
            print(f"  - First 10 values: {verify_vector[:10]}")
        
        print("=== END DEBUG ===")
        
        if updated_fields:
            return {"message": f"Đã cập nhật: {', '.join(updated_fields)} cho image_id={input.image_id}"}
        else:
            return {"message": f"Không có trường nào được cập nhật cho image_id={input.image_id}"}
            
    except Exception as e:
        print(f"Lỗi chi tiết: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"message": f"Lỗi cập nhật embedding: {e}", "status_code": 500}

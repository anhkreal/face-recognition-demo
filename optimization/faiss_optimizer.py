# ===== ADVANCED FAISS PERFORMANCE OPTIMIZATION =====
# File: face_api/optimization/faiss_optimizer.py
# Mục đích: Tối ưu hóa nâng cao cho FAISS operations

import numpy as np
import faiss
import time
from typing import Dict, List, Tuple, Optional
import threading
from config import *

class FaissOptimizer:
    """Các kỹ thuật tối ưu hóa nâng cao cho FAISS"""
    
    def __init__(self, faiss_manager):
        self.faiss_manager = faiss_manager
        self._cache = {}
        self._cache_lock = threading.Lock()
        self._cache_timeout = 300  # 5 phút
        
    def optimize_index_for_query_speed(self):
        """Tối ưu hóa index cho tốc độ query"""
        print("🚀 Optimizing FAISS index for query speed...")
        
        # Rebuild index với optimization
        if hasattr(self.faiss_manager, 'embeddings') and len(self.faiss_manager.embeddings) > 0:
            # Sử dụng OMP threads cho parallel search
            faiss.omp_set_num_threads(4)
            
            # Pre-compute norms nếu sử dụng Inner Product
            if isinstance(self.faiss_manager.index, faiss.IndexFlatIP):
                embeddings = np.array(self.faiss_manager.embeddings)
                # L2 normalize embeddings
                norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
                normalized_embeddings = embeddings / (norms + 1e-8)
                
                # Rebuild index với normalized embeddings
                self.faiss_manager.index.reset()
                self.faiss_manager.index.add(normalized_embeddings.astype(np.float32))
                
                print("✅ Index optimized with L2 normalized embeddings")
    
    def get_cached_query_result(self, embedding_hash: str, topk: int) -> Optional[List]:
        """Lấy kết quả query từ cache"""
        with self._cache_lock:
            cache_key = f"{embedding_hash}_{topk}"
            if cache_key in self._cache:
                result, timestamp = self._cache[cache_key]
                if time.time() - timestamp < self._cache_timeout:
                    return result
                else:
                    del self._cache[cache_key]
        return None
    
    def cache_query_result(self, embedding_hash: str, topk: int, result: List):
        """Cache kết quả query"""
        with self._cache_lock:
            cache_key = f"{embedding_hash}_{topk}"
            self._cache[cache_key] = (result, time.time())
            
            # Cleanup old cache entries (giữ tối đa 100 entries)
            if len(self._cache) > 100:
                oldest_key = min(self._cache.keys(), 
                               key=lambda k: self._cache[k][1])
                del self._cache[oldest_key]
    
    def batch_query_optimization(self, embeddings: np.ndarray, topk: int = 5) -> List[List]:
        """Tối ưu hóa cho batch query"""
        print(f"🔍 Batch querying {len(embeddings)} embeddings...")
        
        # Normalize embeddings
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized_embeddings = embeddings / (norms + 1e-8)
        
        # Batch search
        scores, indices = self.faiss_manager.index.search(
            normalized_embeddings.astype(np.float32), topk
        )
        
        # Format results
        batch_results = []
        for i in range(len(embeddings)):
            query_results = []
            for j in range(topk):
                if indices[i][j] != -1 and scores[i][j] > 0:
                    query_results.append({
                        'image_id': int(self.faiss_manager.image_ids[indices[i][j]]),
                        'image_path': str(self.faiss_manager.image_paths[indices[i][j]]),
                        'class_id': int(self.faiss_manager.class_ids[indices[i][j]]),
                        'score': float(scores[i][j])
                    })
            batch_results.append(query_results)
        
        return batch_results
    
    def memory_usage_analysis(self) -> Dict:
        """Phân tích memory usage"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        # FAISS index size
        index_size = 0
        if hasattr(self.faiss_manager, 'embeddings'):
            index_size = len(self.faiss_manager.embeddings) * 512 * 4  # float32
        
        return {
            'process_memory_mb': round(memory_info.rss / 1024 / 1024, 2),
            'index_size_mb': round(index_size / 1024 / 1024, 2),
            'total_vectors': len(self.faiss_manager.image_ids) if hasattr(self.faiss_manager, 'image_ids') else 0,
            'cache_entries': len(self._cache)
        }
    
    def recommend_optimizations(self) -> List[str]:
        """Đề xuất các tối ưu hóa"""
        recommendations = []
        
        total_vectors = len(self.faiss_manager.image_ids) if hasattr(self.faiss_manager, 'image_ids') else 0
        
        if total_vectors > 50000:
            recommendations.append("🔥 Với >50K vectors, nên sử dụng IndexIVFFlat thay vì IndexFlatIP")
        
        if total_vectors > 100000:
            recommendations.append("🚀 Với >100K vectors, nên sử dụng IndexIVFPQ để giảm memory")
        
        memory_info = self.memory_usage_analysis()
        if memory_info['process_memory_mb'] > 2000:
            recommendations.append("⚠️  Memory usage cao, nên implement disk-based index")
        
        if len(self._cache) == 0:
            recommendations.append("💡 Query cache chưa được sử dụng, nên enable caching")
        
        return recommendations

# Global optimizer instance
faiss_optimizer = None

def get_faiss_optimizer():
    """Lấy FAISS optimizer instance"""
    global faiss_optimizer
    if faiss_optimizer is None:
        from service.shared_instances import get_faiss_manager
        faiss_optimizer = FaissOptimizer(get_faiss_manager())
    return faiss_optimizer

# ===== CRITICAL FIXES FOR PRODUCTION =====
# File: face_api/fixes/atomic_operations.py
# Mục đích: Implement atomic operations cho FAISS để fix critical issues

import numpy as np
import faiss
import shutil
import tempfile
import threading
import time
from typing import Dict, List, Optional
from contextlib import contextmanager

class AtomicFaissManager:
    """
    Enhanced FAISS Manager với atomic operations và error recovery
    Fixes các critical issues đã phát hiện trong code review
    """
    
    def __init__(self, embedding_size: int, index_path: str, meta_path: str):
        self.embedding_size = embedding_size
        self.index_path = index_path
        self.meta_path = meta_path
        self.backup_dir = tempfile.mkdtemp(prefix='faiss_backup_')
        
        # Thread safety
        self._lock = threading.RLock()  # Reentrant lock
        self._transaction_active = False
        
        # Initialize
        self.index = faiss.IndexFlatIP(embedding_size)
        self.image_ids = []
        self.image_paths = []
        self.class_ids = []
        self.embeddings = []
        
        # Load existing data
        self.load()
    
    @contextmanager
    def transaction(self):
        """
        ✅ FIX: Implement transaction-like behavior
        Ensures atomic operations với rollback capability
        """
        with self._lock:
            if self._transaction_active:
                raise RuntimeError("Nested transactions not supported")
            
            # Backup current state
            backup_path = self._create_backup()
            self._transaction_active = True
            
            try:
                yield self
                # If we get here, transaction successful
                self._cleanup_backup(backup_path)
                self._transaction_active = False
                
            except Exception as e:
                # Rollback on any error
                print(f"🔄 Transaction failed, rolling back: {e}")
                self._restore_backup(backup_path)
                self._transaction_active = False
                raise e
    
    def _create_backup(self) -> str:
        """Tạo backup của current state"""
        timestamp = int(time.time())
        backup_path = f"{self.backup_dir}/backup_{timestamp}"
        
        # Backup index file
        if hasattr(self, 'index_path') and self.index_path:
            index_backup = f"{backup_path}_index.bak"
            shutil.copy2(self.index_path, index_backup)
        
        # Backup metadata
        if hasattr(self, 'meta_path') and self.meta_path:
            meta_backup = f"{backup_path}_meta.bak"
            shutil.copy2(self.meta_path, meta_backup)
        
        return backup_path
    
    def _restore_backup(self, backup_path: str):
        """Restore từ backup"""
        try:
            # Restore index
            index_backup = f"{backup_path}_index.bak"
            if os.path.exists(index_backup):
                shutil.copy2(index_backup, self.index_path)
            
            # Restore metadata
            meta_backup = f"{backup_path}_meta.bak"
            if os.path.exists(meta_backup):
                shutil.copy2(meta_backup, self.meta_path)
            
            # Reload data
            self.load()
            print("✅ Backup restored successfully")
            
        except Exception as e:
            print(f"❌ Failed to restore backup: {e}")
            raise e
    
    def _cleanup_backup(self, backup_path: str):
        """Cleanup backup files"""
        try:
            for file in os.listdir(self.backup_dir):
                if file.startswith(os.path.basename(backup_path)):
                    os.remove(os.path.join(self.backup_dir, file))
        except Exception as e:
            print(f"⚠️  Failed to cleanup backup: {e}")
    
    def atomic_delete_by_image_id(self, image_id: int) -> bool:
        """
        ✅ FIX: Atomic delete operation
        Fixes critical issue với non-atomic rebuilds
        """
        with self.transaction():
            return self._unsafe_delete_by_image_id(image_id)
    
    def _unsafe_delete_by_image_id(self, image_id: int) -> bool:
        """Internal delete method (not thread-safe)"""
        image_id = str(image_id)
        
        # Find index
        try:
            idx = [str(i) for i in self.image_ids].index(image_id)
        except ValueError:
            return False  # Not found
        
        # Remove from metadata
        del self.image_ids[idx]
        del self.image_paths[idx]
        del self.class_ids[idx]
        del self.embeddings[idx]
        
        # Rebuild index efficiently
        self._rebuild_index_efficient()
        
        # Save atomically
        self._atomic_save()
        
        return True
    
    def _rebuild_index_efficient(self):
        """
        ✅ FIX: Efficient index rebuild
        Tránh O(n) complexity cho mỗi delete
        """
        # Create new index
        new_index = faiss.IndexFlatIP(self.embedding_size)
        
        if len(self.embeddings) > 0:
            # Add all embeddings at once (more efficient)
            embeddings_array = np.array(self.embeddings, dtype=np.float32)
            new_index.add(embeddings_array)
        
        # Replace old index
        self.index = new_index
    
    def _atomic_save(self):
        """
        ✅ FIX: Atomic save operation
        Prevents corruption during save
        """
        # Save to temporary files first
        temp_index = f"{self.index_path}.tmp"
        temp_meta = f"{self.meta_path}.tmp"
        
        try:
            # Write to temp files
            faiss.write_index(self.index, temp_index)
            np.savez(temp_meta,
                     image_ids=np.array(self.image_ids),
                     image_paths=np.array(self.image_paths),
                     class_ids=np.array(self.class_ids),
                     embeddings=np.array(self.embeddings, dtype=np.float32))
            
            # Atomic move (rename is atomic on most filesystems)
            shutil.move(temp_index, self.index_path)
            shutil.move(temp_meta, self.meta_path)
            
        except Exception as e:
            # Cleanup temp files on failure
            for temp_file in [temp_index, temp_meta]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            raise e
    
    def batch_delete_by_image_ids(self, image_ids: List[int]) -> Dict[int, bool]:
        """
        ✅ FIX: Batch delete operations
        Much more efficient than individual deletes
        """
        results = {}
        
        with self.transaction():
            # Sort indices in reverse order để không ảnh hưởng indices khi delete
            image_ids_str = [str(id) for id in image_ids]
            indices_to_remove = []
            
            for image_id in image_ids_str:
                try:
                    idx = [str(i) for i in self.image_ids].index(image_id)
                    indices_to_remove.append(idx)
                    results[int(image_id)] = True
                except ValueError:
                    results[int(image_id)] = False
            
            # Remove in reverse order
            for idx in sorted(indices_to_remove, reverse=True):
                del self.image_ids[idx]
                del self.image_paths[idx]
                del self.class_ids[idx]
                del self.embeddings[idx]
            
            # Single rebuild for all deletes
            if indices_to_remove:
                self._rebuild_index_efficient()
                self._atomic_save()
        
        return results
    
    def health_check(self) -> Dict:
        """
        ✅ FIX: System health check
        Verifies data consistency
        """
        with self._lock:
            health = {
                'status': 'healthy',
                'checks': {}
            }
            
            # Check metadata consistency
            lengths = [
                len(self.image_ids),
                len(self.image_paths), 
                len(self.class_ids),
                len(self.embeddings)
            ]
            
            if len(set(lengths)) == 1:
                health['checks']['metadata_consistent'] = True
            else:
                health['status'] = 'unhealthy'
                health['checks']['metadata_consistent'] = False
                health['checks']['lengths'] = lengths
            
            # Check FAISS index consistency
            if self.index.ntotal == lengths[0]:
                health['checks']['faiss_consistent'] = True
            else:
                health['status'] = 'unhealthy'
                health['checks']['faiss_consistent'] = False
                health['checks']['faiss_ntotal'] = self.index.ntotal
                health['checks']['metadata_length'] = lengths[0]
            
            return health
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        with self._lock:
            return {
                'total_vectors': len(self.image_ids),
                'unique_classes': len(set(self.class_ids)),
                'index_size_mb': len(self.embeddings) * 512 * 4 / 1024 / 1024,
                'transaction_active': self._transaction_active
            }

# ===== USAGE EXAMPLE =====
if __name__ == '__main__':
    # Example của atomic operations
    manager = AtomicFaissManager(
        embedding_size=512,
        index_path='test_index.faiss',
        meta_path='test_meta.npz'
    )
    
    # Atomic delete
    with manager.transaction():
        success = manager._unsafe_delete_by_image_id(123)
        if not success:
            raise Exception("Delete failed")  # Will trigger rollback
    
    # Batch delete
    results = manager.batch_delete_by_image_ids([1, 2, 3, 4, 5])
    print(f"Batch delete results: {results}")
    
    # Health check
    health = manager.health_check()
    print(f"System health: {health}")

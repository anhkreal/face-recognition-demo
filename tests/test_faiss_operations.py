# ===== UNIT TESTS FOR FACE RECOGNITION API =====
# File: face_api/tests/test_faiss_operations.py
# Mục đích: Unit tests cho các FAISS operations và API endpoints

import pytest
import numpy as np
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from index.faiss import FaissIndexManager
from service.shared_instances import SharedInstances
from optimization.faiss_optimizer import FaissOptimizer

class TestFaissIndexManager:
    """Test cases cho FaissIndexManager"""
    
    @pytest.fixture
    def temp_files(self):
        """Tạo temporary files cho test"""
        index_file = tempfile.NamedTemporaryFile(delete=False, suffix='.index')
        meta_file = tempfile.NamedTemporaryFile(delete=False, suffix='.npz')
        yield index_file.name, meta_file.name
        # Cleanup
        os.unlink(index_file.name)
        os.unlink(meta_file.name)
    
    @pytest.fixture
    def faiss_manager(self, temp_files):
        """Tạo FaissIndexManager instance cho test"""
        index_path, meta_path = temp_files
        manager = FaissIndexManager(
            embedding_size=512,
            index_path=index_path,
            meta_path=meta_path
        )
        return manager
    
    def test_init(self, faiss_manager):
        """Test khởi tạo FaissIndexManager"""
        assert faiss_manager.embedding_size == 512
        assert faiss_manager.index is not None
        assert len(faiss_manager.image_ids) == 0
        assert len(faiss_manager.embeddings) == 0
    
    def test_add_embeddings(self, faiss_manager):
        """Test thêm embeddings vào index"""
        # Tạo test data
        embeddings = np.random.rand(3, 512).astype(np.float32)
        image_ids = [1, 2, 3]
        image_paths = ['img1.jpg', 'img2.jpg', 'img3.jpg']
        class_ids = [10, 20, 30]
        
        # Add embeddings
        faiss_manager.add_embeddings(embeddings, image_ids, image_paths, class_ids)
        
        # Verify
        assert len(faiss_manager.image_ids) == 3
        assert len(faiss_manager.image_paths) == 3
        assert len(faiss_manager.class_ids) == 3
        assert len(faiss_manager.embeddings) == 3
        assert faiss_manager.index.ntotal == 3
    
    def test_query(self, faiss_manager):
        """Test query functionality"""
        # Setup test data
        embeddings = np.random.rand(5, 512).astype(np.float32)
        image_ids = [1, 2, 3, 4, 5]
        image_paths = ['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg', 'img5.jpg']
        class_ids = [10, 20, 10, 30, 20]
        
        faiss_manager.add_embeddings(embeddings, image_ids, image_paths, class_ids)
        
        # Query with first embedding
        query_emb = embeddings[0]
        results = faiss_manager.query(query_emb, topk=3)
        
        # Verify results
        assert len(results) <= 3
        assert results[0]['image_id'] == 1  # Closest should be itself
        assert 'score' in results[0]
        assert 'class_id' in results[0]
    
    def test_delete_by_image_id(self, faiss_manager):
        """Test xóa theo image_id"""
        # Setup
        embeddings = np.random.rand(3, 512).astype(np.float32)
        image_ids = [1, 2, 3]
        image_paths = ['img1.jpg', 'img2.jpg', 'img3.jpg']
        class_ids = [10, 20, 30]
        
        faiss_manager.add_embeddings(embeddings, image_ids, image_paths, class_ids)
        
        # Delete image_id = 2
        result = faiss_manager.delete_by_image_id(2)
        
        # Verify
        assert result == True
        assert len(faiss_manager.image_ids) == 2
        assert 2 not in faiss_manager.image_ids
        assert faiss_manager.index.ntotal == 2
    
    def test_delete_by_class_id(self, faiss_manager):
        """Test xóa theo class_id"""
        # Setup
        embeddings = np.random.rand(4, 512).astype(np.float32)
        image_ids = [1, 2, 3, 4]
        image_paths = ['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg']
        class_ids = [10, 20, 10, 30]  # class_id 10 có 2 images
        
        faiss_manager.add_embeddings(embeddings, image_ids, image_paths, class_ids)
        
        # Delete class_id = 10
        result = faiss_manager.delete_by_class_id(10)
        
        # Verify
        assert result == True
        assert len(faiss_manager.image_ids) == 2
        assert 10 not in faiss_manager.class_ids
        assert faiss_manager.index.ntotal == 2
    
    def test_save_and_load(self, faiss_manager):
        """Test save và load functionality"""
        # Setup test data
        embeddings = np.random.rand(2, 512).astype(np.float32)
        image_ids = [1, 2]
        image_paths = ['img1.jpg', 'img2.jpg']
        class_ids = [10, 20]
        
        faiss_manager.add_embeddings(embeddings, image_ids, image_paths, class_ids)
        
        # Save
        faiss_manager.save()
        
        # Create new manager and load
        new_manager = FaissIndexManager(
            embedding_size=512,
            index_path=faiss_manager.index_path,
            meta_path=faiss_manager.meta_path
        )
        new_manager.load()
        
        # Verify loaded data
        assert len(new_manager.image_ids) == 2
        assert new_manager.image_ids == faiss_manager.image_ids
        assert new_manager.index.ntotal == 2
    
    def test_reset_index(self, faiss_manager):
        """Test reset functionality"""
        # Setup
        embeddings = np.random.rand(3, 512).astype(np.float32)
        image_ids = [1, 2, 3]
        image_paths = ['img1.jpg', 'img2.jpg', 'img3.jpg']
        class_ids = [10, 20, 30]
        
        faiss_manager.add_embeddings(embeddings, image_ids, image_paths, class_ids)
        
        # Reset
        faiss_manager.reset_index()
        
        # Verify reset
        assert len(faiss_manager.image_ids) == 0
        assert len(faiss_manager.embeddings) == 0
        assert faiss_manager.index.ntotal == 0

class TestSharedInstances:
    """Test cases cho SharedInstances singleton"""
    
    def test_singleton_pattern(self):
        """Test singleton pattern hoạt động đúng"""
        # Tạo 2 instances
        instance1 = SharedInstances()
        instance2 = SharedInstances()
        
        # Verify cùng 1 instance
        assert instance1 is instance2
        assert id(instance1) == id(instance2)
    
    @patch('service.shared_instances.ArcFaceFeatureExtractor')
    @patch('service.shared_instances.FaissIndexManager')
    def test_initialization(self, mock_faiss, mock_extractor):
        """Test khởi tạo shared instances"""
        # Mock return values
        mock_faiss_instance = Mock()
        mock_extractor_instance = Mock()
        mock_faiss.return_value = mock_faiss_instance
        mock_extractor.return_value = mock_extractor_instance
        
        # Create instance
        shared = SharedInstances()
        
        # Verify initialization
        assert shared.extractor is not None
        assert shared.faiss_manager is not None
        assert shared.faiss_lock is not None

class TestFaissOptimizer:
    """Test cases cho FaissOptimizer"""
    
    @pytest.fixture
    def mock_faiss_manager(self):
        """Mock FaissIndexManager"""
        manager = Mock()
        manager.embeddings = np.random.rand(100, 512).tolist()
        manager.image_ids = list(range(100))
        manager.image_paths = [f'img_{i}.jpg' for i in range(100)]
        manager.class_ids = [i // 10 for i in range(100)]
        manager.index = Mock()
        return manager
    
    @pytest.fixture
    def optimizer(self, mock_faiss_manager):
        """Tạo FaissOptimizer instance"""
        return FaissOptimizer(mock_faiss_manager)
    
    def test_cache_operations(self, optimizer):
        """Test cache functionality"""
        # Test cache miss
        result = optimizer.get_cached_query_result("test_hash", 5)
        assert result is None
        
        # Cache result
        test_result = [{'image_id': 1, 'score': 0.9}]
        optimizer.cache_query_result("test_hash", 5, test_result)
        
        # Test cache hit
        cached_result = optimizer.get_cached_query_result("test_hash", 5)
        assert cached_result == test_result
    
    def test_memory_analysis(self, optimizer):
        """Test memory analysis"""
        with patch('optimization.faiss_optimizer.psutil') as mock_psutil:
            mock_process = Mock()
            mock_process.memory_info.return_value.rss = 1024 * 1024 * 1024  # 1GB
            mock_psutil.Process.return_value = mock_process
            
            memory_info = optimizer.memory_usage_analysis()
            
            assert 'process_memory_mb' in memory_info
            assert 'index_size_mb' in memory_info
            assert 'total_vectors' in memory_info
    
    def test_recommendations(self, optimizer):
        """Test optimization recommendations"""
        recommendations = optimizer.recommend_optimizations()
        
        assert isinstance(recommendations, list)
        # Should have recommendations for 100 vectors (small dataset)
        assert len(recommendations) > 0

class TestAPILogic:
    """Test cases cho API logic"""
    
    @pytest.fixture
    def mock_shared_instances(self):
        """Mock shared instances"""
        with patch('service.shared_instances.get_faiss_manager') as mock_get_faiss, \
             patch('service.shared_instances.get_extractor') as mock_get_extractor, \
             patch('service.shared_instances.get_faiss_lock') as mock_get_lock:
            
            mock_faiss = Mock()
            mock_extractor = Mock()
            mock_lock = Mock()
            
            mock_get_faiss.return_value = mock_faiss
            mock_get_extractor.return_value = mock_extractor
            mock_get_lock.return_value = mock_lock
            
            yield mock_faiss, mock_extractor, mock_lock
    
    def test_face_query_logic(self, mock_shared_instances):
        """Test face query service logic"""
        mock_faiss, mock_extractor, mock_lock = mock_shared_instances
        
        # Mock return values
        mock_extractor.extract.return_value = np.random.rand(512)
        mock_faiss.query.return_value = [
            {'image_id': 1, 'score': 0.95, 'class_id': 10, 'image_path': 'test.jpg'}
        ]
        
        # Import after mocking
        from service.face_query_service import query_face_service
        
        # Create mock file
        mock_file = Mock()
        mock_file.read.return_value = b'fake_image_data'
        
        # Test would require more complex mocking for cv2.imdecode
        # This is a simplified test structure

# ===== TEST CONFIGURATION =====
if __name__ == '__main__':
    pytest.main(['-v', __file__])

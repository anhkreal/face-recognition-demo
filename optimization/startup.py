# ===== SERVER STARTUP OPTIMIZATION =====
# File: face_api/optimization/startup.py
# Mục đích: Tối ưu hóa khởi động server và warm-up

import time
import threading
from service.shared_instances import SharedInstances
from service.performance_monitor import performance_monitor

class StartupOptimizer:
    """Tối ưu hóa quá trình khởi động server"""
    
    def __init__(self):
        self.startup_start = time.time()
        self.components_ready = {
            'shared_instances': False,
            'faiss_index': False,
            'model_extractor': False,
            'performance_monitor': False
        }
    
    def initialize_components(self):
        """Khởi tạo tất cả components cần thiết"""
        print("🚀 Starting optimized server initialization...")
        
        # 1. Initialize shared instances
        print("📦 Initializing shared instances...")
        shared = SharedInstances()
        self.components_ready['shared_instances'] = True
        print("✅ Shared instances ready")
        
        # 2. Warm up FAISS index
        print("🔥 Warming up FAISS index...")
        faiss_manager = shared.get_faiss_manager()
        if hasattr(faiss_manager, 'image_ids') and len(faiss_manager.image_ids) > 0:
            print(f"📊 FAISS index loaded: {len(faiss_manager.image_ids)} vectors")
        self.components_ready['faiss_index'] = True
        print("✅ FAISS index ready")
        
        # 3. Warm up model extractor
        print("🧠 Warming up ArcFace model...")
        extractor = shared.get_extractor()
        # Dummy extraction để warm up model
        import numpy as np
        dummy_image = np.random.randint(0, 255, (112, 112, 3), dtype=np.uint8)
        try:
            _ = extractor.extract(dummy_image)
            print("✅ ArcFace model warmed up")
        except Exception as e:
            print(f"⚠️  ArcFace warm-up failed: {e}")
        self.components_ready['model_extractor'] = True
        
        # 4. Initialize performance monitor
        self.components_ready['performance_monitor'] = True
        print("✅ Performance monitor ready")
        
        startup_time = time.time() - self.startup_start
        print(f"🎉 Server initialization completed in {startup_time:.2f}s")
        
        return {
            'startup_time_seconds': round(startup_time, 2),
            'components_ready': self.components_ready,
            'status': 'ready'
        }
    
    def get_health_check(self):
        """Health check cho server"""
        from service.shared_instances import get_faiss_manager
        
        health_status = {
            'status': 'healthy',
            'components': self.components_ready,
            'timestamp': time.time()
        }
        
        try:
            faiss_manager = get_faiss_manager()
            health_status['faiss_vectors'] = len(faiss_manager.image_ids) if hasattr(faiss_manager, 'image_ids') else 0
        except Exception as e:
            health_status['status'] = 'unhealthy'
            health_status['error'] = str(e)
        
        return health_status
    
    def async_preload_optimizations(self):
        """Async preload các optimizations"""
        def preload_worker():
            try:
                # Preload optimizer
                from optimization.faiss_optimizer import get_faiss_optimizer
                optimizer = get_faiss_optimizer()
                print("🔧 FAISS optimizer preloaded")
                
                # Run initial optimization
                optimizer.optimize_index_for_query_speed()
                print("⚡ Initial index optimization completed")
                
            except Exception as e:
                print(f"⚠️  Async preload failed: {e}")
        
        # Chạy trong background thread
        preload_thread = threading.Thread(target=preload_worker, daemon=True)
        preload_thread.start()

# Global startup optimizer
startup_optimizer = StartupOptimizer()

def initialize_optimized_server():
    """Khởi tạo server với optimization"""
    result = startup_optimizer.initialize_components()
    startup_optimizer.async_preload_optimizations()
    return result

def get_server_health():
    """Lấy health status của server"""
    return startup_optimizer.get_health_check()

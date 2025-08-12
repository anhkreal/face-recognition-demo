# ===== CONCURRENT LOAD TESTING =====
# File: face_api/test/load_test_concurrent.py
# Mục đích: Mô phỏng 100 clients request đồng thời

import asyncio
import aiohttp
import time
import random
import json
import os
import numpy as np
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RequestResult:
    """Kết quả của một request"""
    client_id: int
    endpoint: str
    status_code: int
    response_time: float
    success: bool
    error: str = None
    response_data: Dict = None

class LoadTester:
    """Class chính để thực hiện load testing"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[RequestResult] = []
        self.results_lock = threading.Lock()
        
        # Test configuration
        self.num_clients = 100
        self.requests_per_client = 5
        self.concurrent_limit = 50  # Giới hạn số request đồng thời
        
    async def create_test_image_file(self) -> bytes:
        """Tạo test image data"""
        # Tạo fake image data (có thể thay bằng real image)
        fake_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        # Convert to bytes (simplified - thực tế cần encode thành JPEG)
        import cv2
        _, buffer = cv2.imencode('.jpg', fake_image)
        return buffer.tobytes()
    
    async def make_request(self, session: aiohttp.ClientSession, client_id: int, 
                          endpoint: str, method: str = "GET", **kwargs) -> RequestResult:
        """Thực hiện một request và đo thời gian"""
        start_time = time.time()
        
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == "GET":
                async with session.get(url, **kwargs) as response:
                    response_data = await response.json()
                    status_code = response.status
            elif method.upper() == "POST":
                async with session.post(url, **kwargs) as response:
                    response_data = await response.json()
                    status_code = response.status
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response_time = time.time() - start_time
            success = 200 <= status_code < 300
            
            return RequestResult(
                client_id=client_id,
                endpoint=endpoint,
                status_code=status_code,
                response_time=response_time,
                success=success,
                response_data=response_data if success else None
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return RequestResult(
                client_id=client_id,
                endpoint=endpoint,
                status_code=0,
                response_time=response_time,
                success=False,
                error=str(e)
            )
    
    async def client_worker(self, client_id: int, session: aiohttp.ClientSession) -> List[RequestResult]:
        """Worker function cho mỗi client"""
        client_results = []
        
        # Các endpoint để test
        test_scenarios = [
            # Health checks (lightweight)
            {"endpoint": "/health", "method": "GET"},
            {"endpoint": "/health/detailed", "method": "GET"},
            
            # Status checks
            {"endpoint": "/index_status", "method": "GET"},
            {"endpoint": "/vector_info", "method": "GET"},
            
            # Performance monitoring
            {"endpoint": "/performance/stats", "method": "GET"},
        ]
        
        # Heavy operations (ít hơn để tránh overload)
        if client_id % 10 == 0:  # Chỉ 10% clients test heavy operations
            test_scenarios.extend([
                {"endpoint": "/search_embeddings?query=1&page=1&page_size=5", "method": "GET"},
                {"endpoint": "/get_image_ids_by_class?class_id=1", "method": "GET"},
            ])
        
        # Face query (rất heavy - chỉ một số client)
        if client_id % 20 == 0:  # Chỉ 5% clients test face query
            try:
                image_data = await self.create_test_image_file()
                test_scenarios.append({
                    "endpoint": "/query",
                    "method": "POST",
                    "data": aiohttp.FormData([
                        ('file', image_data, {'filename': f'test_{client_id}.jpg', 'content-type': 'image/jpeg'})
                    ])
                })
            except Exception as e:
                print(f"Client {client_id}: Failed to create test image: {e}")
        
        # Random delay để mô phỏng real users
        await asyncio.sleep(random.uniform(0, 2))
        
        # Thực hiện requests
        for i in range(self.requests_per_client):
            scenario = random.choice(test_scenarios)
            
            print(f"Client {client_id}: Request {i+1}/{self.requests_per_client} to {scenario['endpoint']}")
            
            result = await self.make_request(
                session, client_id, 
                scenario["endpoint"], 
                scenario["method"],
                **{k: v for k, v in scenario.items() if k not in ["endpoint", "method"]}
            )
            
            client_results.append(result)
            
            # Lưu result thread-safe
            with self.results_lock:
                self.results.append(result)
            
            # Random delay giữa các requests
            await asyncio.sleep(random.uniform(0.1, 0.5))
        
        return client_results
    
    async def run_load_test(self):
        """Chạy load test chính"""
        print(f"🚀 Starting load test with {self.num_clients} clients...")
        print(f"📊 Each client will make {self.requests_per_client} requests")
        print(f"⚡ Maximum {self.concurrent_limit} concurrent requests")
        
        start_time = time.time()
        
        # Tạo semaphore để giới hạn concurrent requests
        semaphore = asyncio.Semaphore(self.concurrent_limit)
        
        async def limited_client_worker(client_id: int, session: aiohttp.ClientSession):
            async with semaphore:
                return await self.client_worker(client_id, session)
        
        # Tạo HTTP session với connection pooling
        connector = aiohttp.TCPConnector(
            limit=100,  # Total connection pool size
            limit_per_host=50,  # Connections per host
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        
        async with aiohttp.ClientSession(
            connector=connector, 
            timeout=timeout,
            headers={"User-Agent": "LoadTester/1.0"}
        ) as session:
            
            # Tạo tasks cho tất cả clients
            tasks = []
            for client_id in range(self.num_clients):
                task = asyncio.create_task(
                    limited_client_worker(client_id, session),
                    name=f"client_{client_id}"
                )
                tasks.append(task)
            
            # Chờ tất cả tasks hoàn thành
            print("⏳ Waiting for all clients to complete...")
            completed_tasks = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Xử lý exceptions
            for i, result in enumerate(completed_tasks):
                if isinstance(result, Exception):
                    print(f"❌ Client {i} failed: {result}")
        
        total_time = time.time() - start_time
        print(f"✅ Load test completed in {total_time:.2f} seconds")
        
        return self.analyze_results(total_time)
    
    def analyze_results(self, total_time: float) -> Dict[str, Any]:
        """Phân tích kết quả load test"""
        if not self.results:
            return {"error": "No results to analyze"}
        
        # Basic metrics
        total_requests = len(self.results)
        successful_requests = sum(1 for r in self.results if r.success)
        failed_requests = total_requests - successful_requests
        success_rate = (successful_requests / total_requests) * 100
        
        # Response time metrics
        response_times = [r.response_time for r in self.results if r.success]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            
            # Percentiles
            response_times_sorted = sorted(response_times)
            p50 = response_times_sorted[len(response_times_sorted) // 2]
            p95_idx = int(len(response_times_sorted) * 0.95)
            p95 = response_times_sorted[p95_idx] if p95_idx < len(response_times_sorted) else response_times_sorted[-1]
            p99_idx = int(len(response_times_sorted) * 0.99)
            p99 = response_times_sorted[p99_idx] if p99_idx < len(response_times_sorted) else response_times_sorted[-1]
        else:
            avg_response_time = min_response_time = max_response_time = p50 = p95 = p99 = 0
        
        # Requests per second
        rps = total_requests / total_time if total_time > 0 else 0
        
        # Error analysis
        error_counts = {}
        for result in self.results:
            if not result.success:
                error_key = f"HTTP_{result.status_code}" if result.status_code > 0 else "Network_Error"
                error_counts[error_key] = error_counts.get(error_key, 0) + 1
        
        # Endpoint analysis
        endpoint_stats = {}
        for result in self.results:
            endpoint = result.endpoint
            if endpoint not in endpoint_stats:
                endpoint_stats[endpoint] = {
                    "total": 0, "success": 0, "failed": 0, 
                    "avg_time": 0, "response_times": []
                }
            
            stats = endpoint_stats[endpoint]
            stats["total"] += 1
            if result.success:
                stats["success"] += 1
                stats["response_times"].append(result.response_time)
            else:
                stats["failed"] += 1
        
        # Calculate avg time per endpoint
        for endpoint, stats in endpoint_stats.items():
            if stats["response_times"]:
                stats["avg_time"] = sum(stats["response_times"]) / len(stats["response_times"])
                stats["success_rate"] = (stats["success"] / stats["total"]) * 100
            del stats["response_times"]  # Remove raw data for cleaner output
        
        analysis = {
            "summary": {
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "failed_requests": failed_requests,
                "success_rate_percent": round(success_rate, 2),
                "total_time_seconds": round(total_time, 2),
                "requests_per_second": round(rps, 2),
                "concurrent_clients": self.num_clients
            },
            "response_times": {
                "average_ms": round(avg_response_time * 1000, 2),
                "min_ms": round(min_response_time * 1000, 2),
                "max_ms": round(max_response_time * 1000, 2),
                "p50_ms": round(p50 * 1000, 2),
                "p95_ms": round(p95 * 1000, 2),
                "p99_ms": round(p99 * 1000, 2)
            },
            "errors": error_counts,
            "endpoint_performance": endpoint_stats
        }
        
        return analysis
    
    def print_results(self, analysis: Dict[str, Any]):
        """In kết quả load test đẹp mắt"""
        print("\n" + "="*80)
        print("🎯 LOAD TEST RESULTS")
        print("="*80)
        
        # Summary
        summary = analysis["summary"]
        print(f"📊 SUMMARY:")
        print(f"   Total Requests: {summary['total_requests']}")
        print(f"   Successful: {summary['successful_requests']} ({summary['success_rate_percent']}%)")
        print(f"   Failed: {summary['failed_requests']}")
        print(f"   Duration: {summary['total_time_seconds']}s")
        print(f"   Throughput: {summary['requests_per_second']} req/s")
        print(f"   Concurrent Clients: {summary['concurrent_clients']}")
        
        # Response Times
        times = analysis["response_times"]
        print(f"\n⏱️  RESPONSE TIMES:")
        print(f"   Average: {times['average_ms']}ms")
        print(f"   Min: {times['min_ms']}ms")
        print(f"   Max: {times['max_ms']}ms")
        print(f"   P50: {times['p50_ms']}ms")
        print(f"   P95: {times['p95_ms']}ms")
        print(f"   P99: {times['p99_ms']}ms")
        
        # Errors
        if analysis["errors"]:
            print(f"\n❌ ERRORS:")
            for error_type, count in analysis["errors"].items():
                print(f"   {error_type}: {count}")
        
        # Top endpoints by performance
        print(f"\n🚀 ENDPOINT PERFORMANCE:")
        endpoints = analysis["endpoint_performance"]
        for endpoint, stats in sorted(endpoints.items(), key=lambda x: x[1]["avg_time"]):
            print(f"   {endpoint}:")
            print(f"      Success Rate: {stats.get('success_rate', 0):.1f}%")
            print(f"      Avg Time: {stats['avg_time']*1000:.1f}ms")
            print(f"      Total Requests: {stats['total']}")
        
        print("="*80)
    
    def save_results(self, analysis: Dict[str, Any], filename: str = None):
        """Lưu kết quả ra file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"load_test_results_{timestamp}.json"
        
        # Thêm raw results
        analysis["raw_results"] = [
            {
                "client_id": r.client_id,
                "endpoint": r.endpoint,
                "status_code": r.status_code,
                "response_time": r.response_time,
                "success": r.success,
                "error": r.error
            }
            for r in self.results
        ]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {filename}")

async def main():
    """Main function để chạy load test"""
    print("🔥 Face Recognition API Load Test")
    print("📝 Testing with 100 concurrent clients...")
    
    # Tạo load tester
    tester = LoadTester(base_url="http://localhost:8000")
    
    # Cấu hình test
    tester.num_clients = 100
    tester.requests_per_client = 3  # Giảm xuống để tránh overload server
    tester.concurrent_limit = 25    # Giới hạn reasonable
    
    try:
        # Chạy load test
        analysis = await tester.run_load_test()
        
        # In kết quả
        tester.print_results(analysis)
        
        # Lưu kết quả
        tester.save_results(analysis)
        
        # Performance assessment
        summary = analysis["summary"]
        avg_time = analysis["response_times"]["average_ms"]
        
        print(f"\n🎯 PERFORMANCE ASSESSMENT:")
        if summary["success_rate_percent"] >= 95 and avg_time < 1000:
            print("✅ EXCELLENT: System handles concurrent load well!")
        elif summary["success_rate_percent"] >= 90 and avg_time < 2000:
            print("🟡 GOOD: System performs adequately under load")
        elif summary["success_rate_percent"] >= 80:
            print("🟠 FAIR: System struggles with concurrent load")
        else:
            print("🔴 POOR: System cannot handle concurrent load")
        
    except KeyboardInterrupt:
        print("\n⏹️  Load test interrupted by user")
    except Exception as e:
        print(f"\n❌ Load test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())

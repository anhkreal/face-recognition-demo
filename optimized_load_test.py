"""
=== OPTIMIZED CONCURRENT LOAD TEST ===
Thực hiện load test với endpoints thực tế của API
Thiết kế cho 100+ concurrent clients
"""

import asyncio
import aiohttp
import time
import json
import statistics
from dataclasses import dataclass
from typing import List, Dict, Any
import random

@dataclass
class TestResult:
    """Kết quả từng request"""
    endpoint: str
    status_code: int
    response_time: float
    success: bool
    error_message: str = ""

class OptimizedLoadTester:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.results: List[TestResult] = []
        
    async def test_endpoint(self, session: aiohttp.ClientSession, method: str, 
                           endpoint: str, data: dict = None) -> TestResult:
        """Test một endpoint cụ thể"""
        start_time = time.time()
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                async with session.get(url) as response:
                    response_time = time.time() - start_time
                    content = await response.text()
                    
                    return TestResult(
                        endpoint=endpoint,
                        status_code=response.status,
                        response_time=response_time,
                        success=response.status < 400
                    )
            
            elif method.upper() == "POST":
                headers = {"Content-Type": "application/json"}
                async with session.post(url, json=data, headers=headers) as response:
                    response_time = time.time() - start_time
                    content = await response.text()
                    
                    return TestResult(
                        endpoint=endpoint,
                        status_code=response.status,
                        response_time=response_time,
                        success=response.status < 400
                    )
                    
        except Exception as e:
            response_time = time.time() - start_time
            return TestResult(
                endpoint=endpoint,
                status_code=0,
                response_time=response_time,
                success=False,
                error_message=str(e)
            )
    
    async def run_health_checks(self, session: aiohttp.ClientSession) -> List[TestResult]:
        """Kiểm tra tất cả health endpoints"""
        health_endpoints = [
            ("GET", "/health"),
            ("GET", "/health/detailed"),
            ("GET", "/health/readiness"),
            ("GET", "/health/liveness")
        ]
        
        tasks = []
        for method, endpoint in health_endpoints:
            tasks.append(self.test_endpoint(session, method, endpoint))
        
        return await asyncio.gather(*tasks)
    
    async def run_status_checks(self, session: aiohttp.ClientSession) -> List[TestResult]:
        """Kiểm tra status endpoints"""
        status_endpoints = [
            ("GET", "/index/status"),
            ("GET", "/vector/info"),
            ("GET", "/vector/count")
        ]
        
        tasks = []
        for method, endpoint in status_endpoints:
            tasks.append(self.test_endpoint(session, method, endpoint))
        
        return await asyncio.gather(*tasks)
    
    async def run_query_simulation(self, session: aiohttp.ClientSession) -> List[TestResult]:
        """Simulation query với test data"""
        # Test data cho face query
        test_query_data = {
            "query_feature": [random.random() for _ in range(512)],  # Random 512-dim vector
            "top_k": 5
        }
        
        query_endpoints = [
            ("POST", "/face/query", test_query_data),
            ("POST", "/face/query_top5", test_query_data)
        ]
        
        tasks = []
        for method, endpoint, data in query_endpoints:
            tasks.append(self.test_endpoint(session, method, endpoint, data))
        
        return await asyncio.gather(*tasks)
    
    async def run_single_client_test(self, client_id: int) -> List[TestResult]:
        """Chạy test cho 1 client"""
        connector = aiohttp.TCPConnector(limit=10)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            all_results = []
            
            # 1. Health checks
            health_results = await self.run_health_checks(session)
            all_results.extend(health_results)
            
            # 2. Status checks  
            status_results = await self.run_status_checks(session)
            all_results.extend(status_results)
            
            # 3. Query simulation (optional - chỉ test nếu có data)
            # query_results = await self.run_query_simulation(session)
            # all_results.extend(query_results)
            
            return all_results
    
    async def run_concurrent_test(self, num_clients: int = 100) -> Dict[str, Any]:
        """Chạy concurrent test với nhiều clients"""
        print(f"🚀 Starting concurrent load test with {num_clients} clients...")
        
        start_time = time.time()
        
        # Tạo tasks cho tất cả clients
        tasks = []
        for i in range(num_clients):
            tasks.append(self.run_single_client_test(i))
        
        # Chạy tất cả concurrent
        all_client_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        
        # Xử lý kết quả
        all_results = []
        for client_results in all_client_results:
            if isinstance(client_results, list):
                all_results.extend(client_results)
            else:
                print(f"❌ Client error: {client_results}")
        
        return self.analyze_results(all_results, total_time, num_clients)
    
    def analyze_results(self, results: List[TestResult], total_time: float, 
                       num_clients: int) -> Dict[str, Any]:
        """Phân tích kết quả test"""
        if not results:
            return {"error": "No results to analyze"}
        
        # Tổng quan
        total_requests = len(results)
        successful_requests = sum(1 for r in results if r.success)
        failed_requests = total_requests - successful_requests
        success_rate = (successful_requests / total_requests) * 100
        
        # Response times
        response_times = [r.response_time for r in results if r.success]
        avg_response_time = statistics.mean(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        
        # Phân tích theo endpoint
        endpoint_stats = {}
        for result in results:
            endpoint = result.endpoint
            if endpoint not in endpoint_stats:
                endpoint_stats[endpoint] = {
                    'total': 0, 'success': 0, 'failed': 0, 
                    'response_times': [], 'status_codes': []
                }
            
            stats = endpoint_stats[endpoint]
            stats['total'] += 1
            stats['status_codes'].append(result.status_code)
            
            if result.success:
                stats['success'] += 1
                stats['response_times'].append(result.response_time)
            else:
                stats['failed'] += 1
        
        # Tính toán cho từng endpoint
        for endpoint, stats in endpoint_stats.items():
            if stats['response_times']:
                stats['avg_response_time'] = statistics.mean(stats['response_times'])
                stats['min_response_time'] = min(stats['response_times'])
                stats['max_response_time'] = max(stats['response_times'])
            else:
                stats['avg_response_time'] = 0
                stats['min_response_time'] = 0
                stats['max_response_time'] = 0
            
            stats['success_rate'] = (stats['success'] / stats['total']) * 100
        
        # Status code analysis
        status_code_counts = {}
        for result in results:
            code = result.status_code
            status_code_counts[code] = status_code_counts.get(code, 0) + 1
        
        return {
            "test_summary": {
                "total_clients": num_clients,
                "total_time_seconds": round(total_time, 2),
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "failed_requests": failed_requests,
                "success_rate_percent": round(success_rate, 2),
                "requests_per_second": round(total_requests / total_time, 2)
            },
            "response_time_analysis": {
                "average_ms": round(avg_response_time * 1000, 2),
                "minimum_ms": round(min_response_time * 1000, 2),
                "maximum_ms": round(max_response_time * 1000, 2)
            },
            "endpoint_analysis": endpoint_stats,
            "status_code_distribution": status_code_counts
        }

async def main():
    """Main function để chạy load test"""
    print("=" * 60)
    print("🔥 OPTIMIZED CONCURRENT LOAD TEST")
    print("=" * 60)
    
    tester = OptimizedLoadTester()
    
    # Test với 50 clients trước (ít hơn để tránh overload)
    results = await tester.run_concurrent_test(num_clients=50)
    
    print("\n📊 TEST RESULTS:")
    print("=" * 60)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Lưu kết quả
    with open("optimized_load_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Kết quả đã được lưu vào: optimized_load_test_results.json")

if __name__ == "__main__":
    asyncio.run(main())

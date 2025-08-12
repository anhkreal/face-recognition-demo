# ===== ADVANCED LOAD TESTING SCENARIOS =====
# File: face_api/test/load_test_scenarios.py
# Mục đích: Các scenarios khác nhau để test performance

import asyncio
import aiohttp
import time
import random
import json
import numpy as np
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import threading
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import pandas as pd

class AdvancedLoadTester:
    """Advanced load tester với nhiều scenarios"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        self.results_lock = threading.Lock()
    
    async def scenario_health_check_storm(self, num_clients: int = 200):
        """Scenario 1: Storm các health check requests"""
        print(f"🌪️  Scenario: Health Check Storm ({num_clients} clients)")
        
        async def health_check_client(client_id: int):
            results = []
            async with aiohttp.ClientSession() as session:
                for i in range(10):  # Mỗi client gửi 10 requests
                    start_time = time.time()
                    try:
                        async with session.get(f"{self.base_url}/health") as response:
                            response_time = time.time() - start_time
                            results.append({
                                'client_id': client_id,
                                'scenario': 'health_storm',
                                'request_id': i,
                                'status_code': response.status,
                                'response_time': response_time,
                                'success': 200 <= response.status < 300
                            })
                    except Exception as e:
                        response_time = time.time() - start_time
                        results.append({
                            'client_id': client_id,
                            'scenario': 'health_storm',
                            'request_id': i,
                            'status_code': 0,
                            'response_time': response_time,
                            'success': False,
                            'error': str(e)
                        })
                    
                    await asyncio.sleep(0.01)  # Very short delay
            
            return results
        
        # Chạy tất cả clients đồng thời
        tasks = [health_check_client(i) for i in range(num_clients)]
        all_results = await asyncio.gather(*tasks)
        
        # Flatten results
        for client_results in all_results:
            self.results.extend(client_results)
        
        return self.analyze_scenario_results('health_storm')
    
    async def scenario_face_query_stress(self, num_clients: int = 50):
        """Scenario 2: Stress test face query endpoints"""
        print(f"🔥 Scenario: Face Query Stress ({num_clients} clients)")
        
        async def face_query_client(client_id: int):
            results = []
            
            # Tạo test images
            test_images = []
            for i in range(5):
                fake_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
                import cv2
                _, buffer = cv2.imencode('.jpg', fake_image)
                test_images.append(buffer.tobytes())
            
            async with aiohttp.ClientSession() as session:
                for i in range(3):  # Mỗi client gửi 3 face queries
                    start_time = time.time()
                    try:
                        image_data = random.choice(test_images)
                        data = aiohttp.FormData()
                        data.add_field('file', image_data, 
                                     filename=f'test_{client_id}_{i}.jpg', 
                                     content_type='image/jpeg')
                        
                        async with session.post(f"{self.base_url}/query", data=data) as response:
                            response_time = time.time() - start_time
                            response_data = await response.json()
                            
                            results.append({
                                'client_id': client_id,
                                'scenario': 'face_query_stress',
                                'request_id': i,
                                'status_code': response.status,
                                'response_time': response_time,
                                'success': 200 <= response.status < 300,
                                'response_size': len(str(response_data))
                            })
                    except Exception as e:
                        response_time = time.time() - start_time
                        results.append({
                            'client_id': client_id,
                            'scenario': 'face_query_stress',
                            'request_id': i,
                            'status_code': 0,
                            'response_time': response_time,
                            'success': False,
                            'error': str(e)
                        })
                    
                    await asyncio.sleep(random.uniform(0.5, 2.0))  # Random delay
            
            return results
        
        # Chạy với giới hạn concurrent để tránh overload
        semaphore = asyncio.Semaphore(25)  # Max 25 concurrent face queries
        
        async def limited_face_query_client(client_id: int):
            async with semaphore:
                return await face_query_client(client_id)
        
        tasks = [limited_face_query_client(i) for i in range(num_clients)]
        all_results = await asyncio.gather(*tasks)
        
        for client_results in all_results:
            self.results.extend(client_results)
        
        return self.analyze_scenario_results('face_query_stress')
    
    async def scenario_mixed_workload(self, num_clients: int = 100):
        """Scenario 3: Mixed workload simulation"""
        print(f"🎭 Scenario: Mixed Workload ({num_clients} clients)")
        
        async def mixed_client(client_id: int):
            results = []
            
            # Define workload distribution
            workload_patterns = [
                # Light users (70%)
                {'health': 5, 'status': 3, 'search': 1, 'face_query': 0},
                # Medium users (20%)  
                {'health': 3, 'status': 2, 'search': 3, 'face_query': 1},
                # Heavy users (10%)
                {'health': 2, 'status': 1, 'search': 5, 'face_query': 3}
            ]
            
            # Assign pattern based on client_id
            if client_id < 70:
                pattern = workload_patterns[0]  # Light
            elif client_id < 90:
                pattern = workload_patterns[1]  # Medium
            else:
                pattern = workload_patterns[2]  # Heavy
            
            async with aiohttp.ClientSession() as session:
                request_id = 0
                
                # Health checks
                for i in range(pattern['health']):
                    start_time = time.time()
                    try:
                        async with session.get(f"{self.base_url}/health") as response:
                            response_time = time.time() - start_time
                            results.append({
                                'client_id': client_id,
                                'scenario': 'mixed_workload',
                                'request_type': 'health',
                                'request_id': request_id,
                                'status_code': response.status,
                                'response_time': response_time,
                                'success': 200 <= response.status < 300
                            })
                    except Exception as e:
                        response_time = time.time() - start_time
                        results.append({
                            'client_id': client_id,
                            'scenario': 'mixed_workload',
                            'request_type': 'health',
                            'request_id': request_id,
                            'status_code': 0,
                            'response_time': response_time,
                            'success': False,
                            'error': str(e)
                        })
                    request_id += 1
                    await asyncio.sleep(random.uniform(0.1, 0.5))
                
                # Status checks
                for i in range(pattern['status']):
                    start_time = time.time()
                    try:
                        async with session.get(f"{self.base_url}/index_status") as response:
                            response_time = time.time() - start_time
                            results.append({
                                'client_id': client_id,
                                'scenario': 'mixed_workload',
                                'request_type': 'status',
                                'request_id': request_id,
                                'status_code': response.status,
                                'response_time': response_time,
                                'success': 200 <= response.status < 300
                            })
                    except Exception as e:
                        response_time = time.time() - start_time
                        results.append({
                            'client_id': client_id,
                            'scenario': 'mixed_workload',
                            'request_type': 'status',
                            'request_id': request_id,
                            'status_code': 0,
                            'response_time': response_time,
                            'success': False,
                            'error': str(e)
                        })
                    request_id += 1
                    await asyncio.sleep(random.uniform(0.2, 1.0))
                
                # Search operations
                for i in range(pattern['search']):
                    start_time = time.time()
                    try:
                        query_class = random.randint(1, 100)
                        url = f"{self.base_url}/search_embeddings?query={query_class}&page=1&page_size=5"
                        async with session.get(url) as response:
                            response_time = time.time() - start_time
                            results.append({
                                'client_id': client_id,
                                'scenario': 'mixed_workload',
                                'request_type': 'search',
                                'request_id': request_id,
                                'status_code': response.status,
                                'response_time': response_time,
                                'success': 200 <= response.status < 300
                            })
                    except Exception as e:
                        response_time = time.time() - start_time
                        results.append({
                            'client_id': client_id,
                            'scenario': 'mixed_workload',
                            'request_type': 'search',
                            'request_id': request_id,
                            'status_code': 0,
                            'response_time': response_time,
                            'success': False,
                            'error': str(e)
                        })
                    request_id += 1
                    await asyncio.sleep(random.uniform(0.5, 2.0))
            
            return results
        
        tasks = [mixed_client(i) for i in range(num_clients)]
        all_results = await asyncio.gather(*tasks)
        
        for client_results in all_results:
            self.results.extend(client_results)
        
        return self.analyze_scenario_results('mixed_workload')
    
    def analyze_scenario_results(self, scenario_name: str) -> Dict[str, Any]:
        """Phân tích kết quả cho một scenario cụ thể"""
        scenario_results = [r for r in self.results if r.get('scenario') == scenario_name]
        
        if not scenario_results:
            return {"error": f"No results for scenario {scenario_name}"}
        
        total_requests = len(scenario_results)
        successful_requests = sum(1 for r in scenario_results if r.get('success', False))
        success_rate = (successful_requests / total_requests) * 100
        
        response_times = [r['response_time'] for r in scenario_results if r.get('success', False)]
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
            
            sorted_times = sorted(response_times)
            p95_idx = int(len(sorted_times) * 0.95)
            p95_time = sorted_times[p95_idx] if p95_idx < len(sorted_times) else sorted_times[-1]
        else:
            avg_time = min_time = max_time = p95_time = 0
        
        # Request type breakdown (for mixed workload)
        request_type_stats = {}
        for result in scenario_results:
            req_type = result.get('request_type', 'unknown')
            if req_type not in request_type_stats:
                request_type_stats[req_type] = {'total': 0, 'success': 0, 'avg_time': 0}
            
            request_type_stats[req_type]['total'] += 1
            if result.get('success', False):
                request_type_stats[req_type]['success'] += 1
        
        # Calculate success rates and avg times per request type
        for req_type, stats in request_type_stats.items():
            type_times = [r['response_time'] for r in scenario_results 
                         if r.get('request_type') == req_type and r.get('success', False)]
            if type_times:
                stats['avg_time'] = sum(type_times) / len(type_times)
            stats['success_rate'] = (stats['success'] / stats['total']) * 100
        
        return {
            'scenario': scenario_name,
            'summary': {
                'total_requests': total_requests,
                'successful_requests': successful_requests,
                'success_rate_percent': round(success_rate, 2),
                'avg_response_time_ms': round(avg_time * 1000, 2),
                'min_response_time_ms': round(min_time * 1000, 2),
                'max_response_time_ms': round(max_time * 1000, 2),
                'p95_response_time_ms': round(p95_time * 1000, 2)
            },
            'request_type_breakdown': request_type_stats
        }
    
    def create_performance_charts(self, results: List[Dict], save_path: str = "performance_charts.png"):
        """Tạo charts cho performance analysis"""
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            
            # Convert to DataFrame
            df = pd.DataFrame(results)
            
            # Create subplots
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Load Test Performance Analysis', fontsize=16)
            
            # 1. Response time distribution
            successful_results = df[df['success'] == True]
            if not successful_results.empty:
                axes[0, 0].hist(successful_results['response_time'] * 1000, bins=50, alpha=0.7)
                axes[0, 0].set_title('Response Time Distribution')
                axes[0, 0].set_xlabel('Response Time (ms)')
                axes[0, 0].set_ylabel('Frequency')
            
            # 2. Success rate by scenario
            scenario_success = df.groupby('scenario').agg({
                'success': ['count', 'sum']
            }).round(2)
            scenario_success.columns = ['total', 'successful']
            scenario_success['success_rate'] = (scenario_success['successful'] / scenario_success['total']) * 100
            
            axes[0, 1].bar(scenario_success.index, scenario_success['success_rate'])
            axes[0, 1].set_title('Success Rate by Scenario')
            axes[0, 1].set_ylabel('Success Rate (%)')
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # 3. Response time over time (if timestamp available)
            if 'timestamp' in df.columns:
                axes[1, 0].scatter(df['timestamp'], df['response_time'] * 1000, alpha=0.5)
                axes[1, 0].set_title('Response Time Over Time')
                axes[1, 0].set_xlabel('Time')
                axes[1, 0].set_ylabel('Response Time (ms)')
            else:
                axes[1, 0].text(0.5, 0.5, 'Timestamp data not available', 
                               ha='center', va='center', transform=axes[1, 0].transAxes)
            
            # 4. Average response time by request type (if available)
            if 'request_type' in df.columns:
                type_avg = successful_results.groupby('request_type')['response_time'].mean() * 1000
                axes[1, 1].bar(type_avg.index, type_avg.values)
                axes[1, 1].set_title('Average Response Time by Request Type')
                axes[1, 1].set_ylabel('Avg Response Time (ms)')
                axes[1, 1].tick_params(axis='x', rotation=45)
            else:
                axes[1, 1].text(0.5, 0.5, 'Request type data not available', 
                               ha='center', va='center', transform=axes[1, 1].transAxes)
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📈 Performance charts saved to: {save_path}")
            
        except ImportError:
            print("⚠️  matplotlib/pandas not available, skipping charts")
        except Exception as e:
            print(f"❌ Failed to create charts: {e}")

async def run_all_scenarios():
    """Chạy tất cả scenarios"""
    print("🚀 Advanced Load Testing - All Scenarios")
    print("="*60)
    
    tester = AdvancedLoadTester()
    all_analyses = []
    
    try:
        # Scenario 1: Health Check Storm
        print("\n1️⃣  Running Health Check Storm...")
        analysis1 = await tester.scenario_health_check_storm(num_clients=200)
        all_analyses.append(analysis1)
        print(f"✅ Health Storm: {analysis1['summary']['success_rate_percent']}% success rate")
        
        # Small delay between scenarios
        await asyncio.sleep(2)
        
        # Scenario 2: Face Query Stress Test
        print("\n2️⃣  Running Face Query Stress Test...")
        analysis2 = await tester.scenario_face_query_stress(num_clients=30)
        all_analyses.append(analysis2)
        print(f"✅ Face Query Stress: {analysis2['summary']['success_rate_percent']}% success rate")
        
        await asyncio.sleep(2)
        
        # Scenario 3: Mixed Workload
        print("\n3️⃣  Running Mixed Workload Simulation...")
        analysis3 = await tester.scenario_mixed_workload(num_clients=100)
        all_analyses.append(analysis3)
        print(f"✅ Mixed Workload: {analysis3['summary']['success_rate_percent']}% success rate")
        
        # Final analysis
        print("\n" + "="*60)
        print("📊 FINAL RESULTS SUMMARY")
        print("="*60)
        
        for analysis in all_analyses:
            scenario = analysis['scenario']
            summary = analysis['summary']
            print(f"\n🎯 {scenario.upper()}:")
            print(f"   Success Rate: {summary['success_rate_percent']}%")
            print(f"   Avg Response: {summary['avg_response_time_ms']}ms")
            print(f"   P95 Response: {summary['p95_response_time_ms']}ms")
            print(f"   Total Requests: {summary['total_requests']}")
        
        # Save detailed results
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_file = f"advanced_load_test_{timestamp}.json"
        
        final_report = {
            'test_timestamp': timestamp,
            'scenarios': all_analyses,
            'raw_results': tester.results
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed results saved to: {results_file}")
        
        # Create performance charts
        tester.create_performance_charts(tester.results, f"performance_charts_{timestamp}.png")
        
        # Overall assessment
        overall_success_rate = sum(a['summary']['successful_requests'] for a in all_analyses) / sum(a['summary']['total_requests'] for a in all_analyses) * 100
        overall_avg_time = sum(a['summary']['avg_response_time_ms'] * a['summary']['total_requests'] for a in all_analyses) / sum(a['summary']['total_requests'] for a in all_analyses)
        
        print(f"\n🎯 OVERALL SYSTEM ASSESSMENT:")
        print(f"   Overall Success Rate: {overall_success_rate:.1f}%")
        print(f"   Overall Avg Response: {overall_avg_time:.1f}ms")
        
        if overall_success_rate >= 95 and overall_avg_time < 500:
            print("🟢 EXCELLENT: System performs excellently under various loads!")
        elif overall_success_rate >= 90 and overall_avg_time < 1000:
            print("🟡 GOOD: System handles different workloads well")
        elif overall_success_rate >= 80:
            print("🟠 FAIR: System shows some performance issues under load")
        else:
            print("🔴 POOR: System needs optimization for production")
        
    except Exception as e:
        print(f"❌ Load testing failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_all_scenarios())

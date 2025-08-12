# ===== SIMPLE CONCURRENT TEST RUNNER =====
# File: face_api/test/run_concurrent_test.py
# Mục đích: Script đơn giản để chạy concurrent test

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def run_basic_concurrent_test():
    """Chạy test concurrent cơ bản"""
    print("🔥 STARTING CONCURRENT LOAD TEST")
    print("="*50)
    print("Testing Face Recognition API with 100 concurrent clients")
    print("Each client will make multiple requests to different endpoints")
    print("="*50)
    
    try:
        # Import and run the basic load test
        from load_test_concurrent import LoadTester
        
        # Create tester with reasonable settings
        tester = LoadTester(base_url="http://localhost:8000")
        
        # Configure for moderate load
        tester.num_clients = 100
        tester.requests_per_client = 3
        tester.concurrent_limit = 30
        
        print(f"📊 Configuration:")
        print(f"   Clients: {tester.num_clients}")
        print(f"   Requests per client: {tester.requests_per_client}")
        print(f"   Concurrent limit: {tester.concurrent_limit}")
        print(f"   Total requests: {tester.num_clients * tester.requests_per_client}")
        print()
        
        # Run the test
        analysis = await tester.run_load_test()
        
        # Print results
        tester.print_results(analysis)
        
        # Save results
        tester.save_results(analysis, "concurrent_test_results.json")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

async def run_advanced_scenarios():
    """Chạy advanced test scenarios"""
    print("\n🚀 STARTING ADVANCED SCENARIO TESTING")
    print("="*50)
    
    try:
        from load_test_scenarios import run_all_scenarios
        await run_all_scenarios()
        
    except Exception as e:
        print(f"❌ Advanced scenarios failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run concurrent load tests for Face Recognition API')
    parser.add_argument('--test-type', choices=['basic', 'advanced', 'both'], 
                       default='basic', help='Type of test to run')
    parser.add_argument('--server-url', default='http://localhost:8000', 
                       help='Base URL of the API server')
    
    args = parser.parse_args()
    
    print("🎯 Face Recognition API - Concurrent Load Testing")
    print(f"🌐 Server: {args.server_url}")
    print(f"🧪 Test Type: {args.test_type}")
    print()
    
    # Check if server is running
    import requests
    try:
        response = requests.get(f"{args.server_url}/health", timeout=5)
        print(f"✅ Server is running (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Server check failed: {e}")
        print("⚠️  Make sure the Face Recognition API server is running!")
        print("   Start it with: uvicorn app:app --reload")
        return
    
    async def run_tests():
        if args.test_type in ['basic', 'both']:
            print("\n" + "="*60)
            print("🔥 BASIC CONCURRENT TEST")
            print("="*60)
            await run_basic_concurrent_test()
        
        if args.test_type in ['advanced', 'both']:
            print("\n" + "="*60)
            print("🚀 ADVANCED SCENARIO TESTS") 
            print("="*60)
            await run_advanced_scenarios()
        
        print("\n🎉 All tests completed!")
    
    # Run the async tests
    asyncio.run(run_tests())

if __name__ == "__main__":
    main()

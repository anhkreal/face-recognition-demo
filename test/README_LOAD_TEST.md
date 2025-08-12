# ===== QUICK START GUIDE FOR LOAD TESTING =====
# File: face_api/test/README_LOAD_TEST.md

# 🚀 Face Recognition API - Concurrent Load Testing

## Mô tả
Hệ thống load testing để mô phỏng 100+ clients request đồng thời, kiểm tra hiệu suất và độ ổn định của Face Recognition API.

## 📁 Files
- `load_test_concurrent.py` - Basic concurrent load test (100 clients)
- `load_test_scenarios.py` - Advanced scenarios (health storm, face query stress, mixed workload)
- `run_concurrent_test.py` - Script chính để chạy tests
- `requirements_test.txt` - Dependencies cho testing

## 🚀 Quick Start

### 1. Cài đặt dependencies
```bash
pip install -r test/requirements_test.txt
```

### 2. Khởi động API server
```bash
cd face_api
uvicorn app:app --reload
```

### 3. Chạy concurrent load test

#### Basic Test (100 clients)
```bash
cd test
python run_concurrent_test.py --test-type basic
```

#### Advanced Scenarios  
```bash
python run_concurrent_test.py --test-type advanced
```

#### Chạy tất cả tests
```bash
python run_concurrent_test.py --test-type both
```

## 📊 Test Scenarios

### 1. Basic Concurrent Test
- **100 clients** đồng thời
- Mỗi client gửi **3-5 requests**
- Mix các endpoints: health, status, search, face query
- **Concurrent limit**: 30 requests đồng thời

### 2. Health Check Storm
- **200 clients** gửi health check requests
- Mỗi client: 10 requests liên tiếp
- Test khả năng xử lý lightweight requests

### 3. Face Query Stress Test  
- **50 clients** gửi face recognition requests
- Upload và analyze fake images
- Test heavy computation workload

### 4. Mixed Workload Simulation
- **100 clients** với patterns khác nhau:
  - 70% light users (health checks, status)
  - 20% medium users (search operations)
  - 10% heavy users (face queries)

## 📈 Kết quả và Metrics

### Response Time Metrics
- Average response time
- P50, P95, P99 percentiles
- Min/Max response times

### Throughput Metrics  
- Requests per second (RPS)
- Success rate percentage
- Error rate breakdown

### System Performance
- Concurrent handling capability
- Memory usage under load
- Error recovery assessment

## 🎯 Performance Targets

### Excellent Performance
- ✅ Success rate: ≥95%
- ✅ Average response time: <500ms
- ✅ P95 response time: <1000ms

### Good Performance
- 🟡 Success rate: ≥90%
- 🟡 Average response time: <1000ms
- 🟡 P95 response time: <2000ms

### Needs Optimization
- 🔴 Success rate: <90%
- 🔴 Average response time: >1000ms
- 🔴 High error rates

## 📄 Output Files

### Results Files
- `concurrent_test_results.json` - Basic test results
- `advanced_load_test_YYYYMMDD_HHMMSS.json` - Advanced scenarios
- `performance_charts_YYYYMMDD_HHMMSS.png` - Performance visualizations

### Sample Results Structure
```json
{
  "summary": {
    "total_requests": 300,
    "successful_requests": 285,
    "success_rate_percent": 95.0,
    "requests_per_second": 12.5,
    "concurrent_clients": 100
  },
  "response_times": {
    "average_ms": 245.67,
    "p95_ms": 890.12,
    "p99_ms": 1205.34
  },
  "endpoint_performance": {
    "/health": {
      "success_rate": 99.5,
      "avg_time": 0.089
    }
  }
}
```

## 🔧 Customization

### Modify Test Parameters
```python
# In run_concurrent_test.py
tester.num_clients = 200        # Number of concurrent clients
tester.requests_per_client = 5  # Requests per client
tester.concurrent_limit = 50    # Max concurrent requests
```

### Add Custom Endpoints
```python
# In load_test_concurrent.py
test_scenarios.append({
    "endpoint": "/your_custom_endpoint",
    "method": "GET"
})
```

## 🐛 Troubleshooting

### Server Connection Issues
```bash
# Check if server is running
curl http://localhost:8000/health

# Check server logs
tail -f face_api_logs.txt
```

### Memory Issues
- Reduce `num_clients` or `concurrent_limit`
- Monitor server memory usage
- Check for memory leaks in API

### Performance Issues
- Use performance monitoring endpoints:
  - `/performance/stats`
  - `/optimization/analysis`
- Check system resources (CPU, Memory, Disk I/O)

## 📞 Support
- Xem logs trong terminal khi chạy test
- Check API server logs để debug issues
- Monitor system resources during testing

## 🎉 Example Usage

```bash
# Terminal 1: Start API server
cd face_api
uvicorn app:app --reload

# Terminal 2: Run load test
cd test
python run_concurrent_test.py --test-type both

# Results will be displayed and saved to JSON files
```

Happy Load Testing! 🚀

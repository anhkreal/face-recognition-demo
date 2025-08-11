
import requests
import time
import os

BASE_URL = "http://127.0.0.1:8000"
add_url = f"{BASE_URL}/add_embedding"
vector_info_url = f"{BASE_URL}/vector_info"
get_ids_url = f"{BASE_URL}/get_image_ids_by_class?class_id=999"
delete_url = f"{BASE_URL}/delete_image"

NUM_ROUNDS = 50  # Số vòng lặp test

# Tạo file giả để test (nếu chưa có file test2.jpg)
if not os.path.exists("test2.jpg"):
    with open("test2.jpg", "wb") as f:
        f.write(os.urandom(1024))  # file ảnh giả 1KB


# Thống kê thời gian
add_times = []
vector_info_times = []
get_ids_times = []
delete_times = []
vector_info2_times = []

for round_idx in range(1, NUM_ROUNDS + 1):
    print(f"\n--- Vòng lặp {round_idx} ---")
    add_data = {
        "image_id": f"99999{round_idx}",
        "image_path": f"test2{round_idx}.jpg",
        "class_id": "999",
        "ten": f"Test User {round_idx}",
        "gioitinh": "true",
        "tuoi": 30,
        "noio": "Test City"
    }
    # 1. Thêm 1 ảnh
    with open("test2.jpg", "rb") as f:
        files = {"file": f}
        start = time.time()
        add_response = requests.post(add_url, data=add_data, files=files)
        add_time = time.time() - start
        add_times.append(add_time)
        print(f"[1] Thêm ảnh: {add_response.status_code}, thời gian: {add_time:.3f}s")

    # 2. Truy vấn vector_info
    start = time.time()
    vector_info_response = requests.get(vector_info_url)
    vector_info_time = time.time() - start
    vector_info_times.append(vector_info_time)
    print(f"[2] Truy vấn vector_info: {vector_info_response.status_code}, thời gian: {vector_info_time:.3f}s")

    # 3. Truy vấn get_image_ids_by_class
    start = time.time()
    get_ids_response = requests.get(get_ids_url)
    get_ids_time = time.time() - start
    get_ids_times.append(get_ids_time)
    print(f"[3] Truy vấn get_image_ids_by_class: {get_ids_response.status_code}, thời gian: {get_ids_time:.3f}s")

    # 4. Xóa 1 ảnh
    delete_data = {"image_id": f"99999{round_idx}"}
    start = time.time()
    delete_response = requests.post(delete_url, data=delete_data)
    delete_time = time.time() - start
    delete_times.append(delete_time)
    print(f"[4] Xóa ảnh: {delete_response.status_code}, thời gian: {delete_time:.3f}s")

    # 5. Truy vấn lại vector_info
    start = time.time()
    vector_info_response2 = requests.get(vector_info_url)
    vector_info_time2 = time.time() - start
    vector_info2_times.append(vector_info_time2)
    print(f"[5] Truy vấn lại vector_info: {vector_info_response2.status_code}, thời gian: {vector_info_time2:.3f}s")

# In thống kê trung bình

print("\n--- Thống kê thời gian trung bình ---")
print(f"[1] Thêm ảnh: {sum(add_times)/len(add_times):.3f}s")
print(f"[2] Truy vấn vector_info: {sum(vector_info_times)/len(vector_info_times):.3f}s")
print(f"[3] Truy vấn get_image_ids_by_class: {sum(get_ids_times)/len(get_ids_times):.3f}s")
print(f"[4] Xóa ảnh: {sum(delete_times)/len(delete_times):.3f}s")
print(f"[5] Truy vấn lại vector_info: {sum(vector_info2_times)/len(vector_info2_times):.3f}s")

# Vẽ boxplot thời gian các API
import matplotlib.pyplot as plt
plt.figure(figsize=(10,6))
data = [add_times, vector_info_times, get_ids_times, delete_times, vector_info2_times]
labels = [
    "Thêm ảnh",
    "Truy vấn vector_info",
    "get_image_ids_by_class",
    "Xóa ảnh",
    "Truy vấn lại vector_info"
]
plt.boxplot(data, labels=labels, showmeans=True)
plt.ylabel('Thời gian (s)')
plt.title('Boxplot thời gian các API qua nhiều vòng lặp')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('api_response_times_boxplot.png')
plt.show()

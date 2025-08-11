# Xuất danh sách class_id có trong image_class_labels.txt và có is_test==1 trong train_test_split.txt
import csv

IMAGE_CLASS_LABELS = './image_class_labels.txt'
TRAIN_TEST_SPLIT = './train_test_split.txt'
CSV_PATH = 'test_class_ids.csv'

if __name__ == '__main__':
    # 1. Đọc image_id có is_test==1 từ train_test_split.txt
    test_image_ids = set()
    with open(TRAIN_TEST_SPLIT, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[1] == '1':
                test_image_ids.add(parts[0])

    # 2. Tra cứu class_id tương ứng từ image_class_labels.txt
    class_ids = set()
    with open(IMAGE_CLASS_LABELS, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0] in test_image_ids:
                class_ids.add(parts[1])

    result_class_ids = sorted(class_ids, key=lambda x: int(x))
    print(f'Tổng số class_id thỏa mãn: {len(result_class_ids)}')

    # Ghi ra file test_class_ids.csv (chỉ class_id)
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['class_id'])
        for cid in result_class_ids:
            writer.writerow([cid])
    print(f'Đã ghi danh sách class_id test ra file {CSV_PATH}')

    # Sinh thông tin giả lập cho từng class_id và ghi ra file test_class_info.csv
    import random
    names = [
        'An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Hùng', 'Lan', 'Linh', 'Minh', 'Nam', 'Nga', 'Phong', 'Quân', 'Sơn', 'Thảo', 'Trang', 'Tuấn', 'Vân', 'Việt', 'Yến',
        'Phúc', 'Khánh', 'Hải', 'Tùng', 'Mai', 'Hạnh', 'Phương', 'Giang', 'Hương', 'Hòa', 'Đức', 'Tiến', 'Thịnh', 'Cường', 'Thu', 'Hằng', 'Hậu', 'Tâm', 'Tài', 'Bảo',
        'Diễm', 'Nhung', 'Trung', 'Kiên', 'Lộc', 'Quyên', 'Trúc', 'Uyên', 'Thúy', 'Hải Yến', 'Kim', 'Ngọc', 'Thanh', 'Tú', 'Hải Đăng', 'Đan', 'Vũ', 'Hải Nam', 'Hải Anh'
    ]
    gioitinh_list = ['Nam', 'Nữ']
    noio_list = [
        'Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Cần Thơ', 'Hải Phòng', 'Huế', 'Nghệ An', 'Quảng Ninh', 'Bắc Ninh', 'Thanh Hóa',
        'Bình Dương', 'Bình Định', 'Bình Thuận', 'Lâm Đồng', 'Vĩnh Phúc', 'Nam Định', 'Thái Bình', 'Phú Thọ', 'Hưng Yên', 'Hòa Bình',
        'Khánh Hòa', 'Quảng Nam', 'Quảng Ngãi', 'Gia Lai', 'Đắk Lắk', 'Đồng Nai', 'Long An', 'Tiền Giang', 'Bến Tre', 'Trà Vinh',
        'Sóc Trăng', 'Bạc Liêu', 'Cà Mau', 'Kiên Giang', 'An Giang', 'Tây Ninh', 'Bình Phước', 'Kon Tum', 'Hà Tĩnh', 'Quảng Bình',
        'Quảng Trị', 'Lào Cai', 'Yên Bái', 'Tuyên Quang', 'Cao Bằng', 'Bắc Kạn', 'Lạng Sơn', 'Hà Giang', 'Sơn La', 'Điện Biên',
        'Lai Châu', 'Bắc Giang', 'Bắc Ninh', 'Hà Nam', 'Ninh Bình', 'Thái Nguyên', 'Vĩnh Long', 'Đồng Tháp', 'Hậu Giang', 'Ninh Thuận'
    ]
    info_path = 'test_class_info.csv'
    with open(info_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['class_id', 'ten', 'tuoi', 'gioitinh', 'noio'])
        for cid in result_class_ids:
            ten = random.choice(names)
            tuoi = random.randint(18, 60)
            gioitinh = random.choice(gioitinh_list)
            noio = random.choice(noio_list)
            writer.writerow([cid, ten, tuoi, gioitinh, noio])
    print(f'Đã ghi thông tin giả lập cho class_id ra file {info_path}')

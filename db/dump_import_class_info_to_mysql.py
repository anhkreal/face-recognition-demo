import csv
import pymysql
from mysql_conn import get_connection

DB_NAME = 'face_db'
TABLE_NAME = 'nguoi'
CSV_PATH = 'face_api/db/class_info.csv'

CREATE_DB_SQL = f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
CREATE_TABLE_SQL = f'''
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    class_id INT PRIMARY KEY,
    ten VARCHAR(100),
    tuoi INT,
    gioitinh VARCHAR(10),
    noio VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''
INSERT_SQL = f"""
REPLACE INTO {TABLE_NAME} (class_id, ten, tuoi, gioitinh, noio)
VALUES (%s, %s, %s, %s, %s)
"""

def main():
    # Kết nối MySQL không chọn DB để tạo DB nếu chưa có
    conn = pymysql.connect(host='localhost', user='root', password='', charset='utf8mb4')
    with conn.cursor() as cursor:
        cursor.execute(CREATE_DB_SQL)
    conn.close()

    # Kết nối lại với DB
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(CREATE_TABLE_SQL)
        # Đọc file CSV và chèn dữ liệu
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = [(int(row['class_id']), row['ten'], int(row['tuoi']), row['gioitinh'], row['noio']) for row in reader]
            cursor.executemany(INSERT_SQL, rows)
        conn.commit()
    conn.close()
    print(f'Đã tạo DB, bảng và chèn {len(rows)} bản ghi từ {CSV_PATH} vào bảng {TABLE_NAME}')

if __name__ == '__main__':
    main()

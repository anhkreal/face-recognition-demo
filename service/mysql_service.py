import pymysql

def get_all_nguoi_service():
    # Kết nối tới MySQL, thay đổi các thông số cho phù hợp
    conn = pymysql.connect(
        host='localhost', user='root', password='your_password', db='your_db', charset='utf8mb4'
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, ten, tuoi, gioitinh, noio FROM nguoi")
            rows = cursor.fetchall()
            # Trả về danh sách dict
            result = []
            for row in rows:
                result.append({
                    "id": row[0],
                    "ten": row[1],
                    "tuoi": row[2],
                    "gioitinh": row[3],
                    "noio": row[4]
                })
            return result
    finally:
        conn.close()


from db.models import Nguoi
from db.connection_helper import ConnectionHelper

class NguoiRepository(ConnectionHelper):
    def search_nguoi_paged(self, query: str = "", page: int = 1, page_size: int = 15, sort_by: str = "ten_asc"):
        """
        Tìm kiếm danh sách người, trả về kết quả của một trang chỉ định (phân trang).
        page: số trang (bắt đầu từ 1)
        page_size: số lượng mỗi trang
        sort_by: sắp xếp theo (ten_asc, ten_desc, tuoi_asc, tuoi_desc, class_id_asc, class_id_desc, created_asc, created_desc, updated_asc, updated_desc)
        """
        import unicodedata
        def remove_accents(input_str):
            return ''.join(
                c for c in unicodedata.normalize('NFD', input_str)
                if unicodedata.category(c) != 'Mn'
            )
        
        # Parse sort_by
        sort_mapping = {
            'ten_asc': 'ten ASC',
            'ten_desc': 'ten DESC', 
            'tuoi_asc': 'tuoi ASC',
            'tuoi_desc': 'tuoi DESC',
            'class_id_asc': 'CAST(class_id AS UNSIGNED) ASC',
            'class_id_desc': 'CAST(class_id AS UNSIGNED) DESC'
        }
        order_clause = sort_mapping.get(sort_by, 'ten ASC')
        
        offset = (page - 1) * page_size
        sql = "SELECT * FROM nguoi"
        params = []
        where_clauses = []
        if query:
            query_no_accents = remove_accents(query.lower())
            where_clauses.append("(LOWER(ten) LIKE %s OR LOWER(noio) LIKE %s OR CAST(tuoi AS CHAR) LIKE %s OR CAST(gioitinh AS CHAR) LIKE %s)")
            params += [f"%{query.lower()}%", f"%{query.lower()}%", f"%{query.lower()}%", f"%{query.lower()}%"]
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
        sql += f" ORDER BY {order_clause} LIMIT %s OFFSET %s"
        params += [page_size, offset]
        with self as cursor:
            cursor.execute(sql, tuple(params))
            rows = cursor.fetchall()
            # Đếm tổng số kết quả phù hợp
            count_sql = "SELECT COUNT(*) as total FROM nguoi"
            count_params = []
            if where_clauses:
                count_sql += " WHERE " + " AND ".join(where_clauses)
                count_params = params[:-2]  # loại bỏ LIMIT/OFFSET
            cursor.execute(count_sql, tuple(count_params))
            total = cursor.fetchone()['total']
            # Lọc tiếng Việt không dấu nếu có query
            if query:
                filtered = []
                for row in rows:
                    ten_no_accents = remove_accents(row['ten'].lower()) if 'ten' in row else ''
                    noio_no_accents = remove_accents(row['noio'].lower()) if 'noio' in row else ''
                    tuoi_str = str(row.get('tuoi', '')).lower()
                    gioitinh_str = str(row.get('gioitinh', '')).lower()
                    if (
                        query_no_accents in ten_no_accents
                        or query_no_accents in noio_no_accents
                        or query.lower() in tuoi_str
                        or query.lower() in gioitinh_str
                    ):
                        filtered.append(Nguoi.from_row(row))
                return {
                    'nguoi_list': filtered,
                    'total': total
                }
            return {
                'nguoi_list': [Nguoi.from_row(row) for row in rows],
                'total': total
            }
    def search_nguoi(self, query: str = ""):
        """
        Tìm kiếm danh sách người với đầu vào là một chuỗi, tìm trên các trường: ten, noio, hỗ trợ tiếng Việt không dấu.
        Nếu query rỗng thì trả về toàn bộ.
        """
        import unicodedata
        def remove_accents(input_str):
            return ''.join(
                c for c in unicodedata.normalize('NFD', input_str)
                if unicodedata.category(c) != 'Mn'
            )
        sql = "SELECT * FROM nguoi"
        params = []
        if query:
            query_no_accents = remove_accents(query.lower())
            sql += " WHERE LOWER(ten) LIKE %s OR LOWER(noio) LIKE %s OR CAST(tuoi AS CHAR) LIKE %s OR CAST(gioitinh AS CHAR) LIKE %s"
            params = [f"%{query.lower()}%", f"%{query.lower()}%", f"%{query.lower()}%", f"%{query.lower()}%"]
        with self as cursor:
            cursor.execute(sql, tuple(params))
            rows = cursor.fetchall()
            if query:
                filtered = []
                for row in rows:
                    ten_no_accents = remove_accents(row['ten'].lower()) if 'ten' in row else ''
                    noio_no_accents = remove_accents(row['noio'].lower()) if 'noio' in row else ''
                    tuoi_str = str(row.get('tuoi', '')).lower()
                    gioitinh_str = str(row.get('gioitinh', '')).lower()
                    if (
                        query_no_accents in ten_no_accents
                        or query_no_accents in noio_no_accents
                        or query.lower() in tuoi_str
                        or query.lower() in gioitinh_str
                    ):
                        filtered.append(Nguoi.from_row(row))
                return filtered
            return [Nguoi.from_row(row) for row in rows]
    def get_total_and_examples(self, limit=5):
        """Trả về tổng số người và ví dụ một số người."""
        with self as cursor:
            cursor.execute('SELECT COUNT(*) as total FROM nguoi')
            total = cursor.fetchone()['total']
            cursor.execute('SELECT * FROM nguoi LIMIT %s', (limit,))
            examples = [row for row in cursor.fetchall()]
        return total, examples
    def truncate_all(self):
        """Xóa toàn bộ dữ liệu bảng nguoi, giữ lại cấu trúc."""
        with self as cursor:
            cursor.execute('TRUNCATE TABLE nguoi')
    def add(self, nguoi: Nguoi):
        sql = """
        REPLACE INTO nguoi (class_id, ten, tuoi, gioitinh, noio)
        VALUES (%s, %s, %s, %s, %s)
        """
        with self as cursor:
            cursor.execute(sql, (nguoi.class_id, nguoi.ten, nguoi.tuoi, nguoi.gioitinh, nguoi.noio))

    def delete_by_class_id(self, class_id):
        # Đảm bảo class_id là UUID hợp lệ
        # from uuid import UUID
        # if not isinstance(class_id, UUID):
        #     try:
        #         class_id = UUID(str(class_id))
        #     except Exception:
        #         raise ValueError('class_id phải là UUID hợp lệ')
        sql = "DELETE FROM nguoi WHERE class_id = %s"
        with self as cursor:
            cursor.execute(sql, (str(class_id),))

    def get_by_class_id(self, class_id):
        # from uuid import UUID
        # print(1)
        # if not isinstance(class_id, UUID):
        #     try:
        #         print(2)
        #         class_id = UUID(str(class_id))
        #         print(3, class_id, type(class_id))
        #     except Exception:
        #         raise ValueError('class_id phải là UUID hợp lệ')
        sql = "SELECT * FROM nguoi WHERE class_id = %s"
        # print("abc", class_id, type(class_id))
        with self as cursor:
            cursor.execute(sql, (str(class_id),))
            row = cursor.fetchone()
            if row:
                return Nguoi.from_row(row)
            return None

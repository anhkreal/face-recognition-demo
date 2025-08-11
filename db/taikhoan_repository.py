from db.models import TaiKhoan
from db.connection_helper import ConnectionHelper

class TaiKhoanRepository(ConnectionHelper):
    def add(self, taikhoan: TaiKhoan):
        sql = "INSERT INTO taikhoan (username, passwrd) VALUES (%s, %s)"
        with self as cursor:
            cursor.execute(sql, (taikhoan.username, taikhoan.passwrd))

    def get_by_username(self, username: str):
        sql = "SELECT * FROM taikhoan WHERE username = %s"
        with self as cursor:
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            if row:
                return TaiKhoan(username=row.get('username'), passwrd=row.get('passwrd'))
            return None

    def check_login(self, username: str, passwrd: str):
        sql = "SELECT * FROM taikhoan WHERE username = %s AND passwrd = %s"
        with self as cursor:
            cursor.execute(sql, (username, passwrd))
            row = cursor.fetchone()
            return row is not None

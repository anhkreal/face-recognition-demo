from dataclasses import dataclass
from uuid import UUID

@dataclass
class TaiKhoan:
    username: str
    passwrd: str

    @staticmethod
    def from_row(row):
        """
        Tạo đối tượng TaiKhoan từ dict (row) lấy từ MySQL (cursor trả về).
        """
        return TaiKhoan(
            username=row.get('username'),
            passwrd=row.get('passwrd')
        )
    
@dataclass
class Nguoi:
    class_id: int
    # class_id: UUID
    ten: str
    tuoi: int
    gioitinh: str
    noio: str

    @staticmethod
    def from_row(row):
        """
        Tạo đối tượng Nguoi từ dict (row) lấy từ MySQL (cursor trả về).
        """
        return Nguoi(
            class_id=row.get('class_id'),
            # class_id=UUID(str(row.get('class_id'))),
            ten=row.get('ten'),
            tuoi=row.get('tuoi'),
            gioitinh=row.get('gioitinh'),
            noio=row.get('noio')
        )

    def to_dict(self):
        return {
            'class_id': str(self.class_id),
            'ten': self.ten,
            'tuoi': self.tuoi,
            'gioitinh': self.gioitinh,
            'noio': self.noio
        }

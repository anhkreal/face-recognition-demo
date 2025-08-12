from pydantic import BaseModel, Field, constr, conint
from fastapi import APIRouter, Depends, File, UploadFile, Form

class AddEmbeddingInput(BaseModel):
    image_id: int = Field(..., description="ID duy nhất cho ảnh (số nguyên)")
    image_path: str = Field(..., description="Đường dẫn lưu trữ ảnh")
    class_id: int = Field(..., description="ID nhóm người (để nhóm nhiều ảnh của cùng 1 người)")
    ten: str = Field(..., description="Tên đầy đủ của người")
    gioitinh: bool = Field(..., description="Giới tính (true=Nam, false=Nữ)")
    tuoi: int = Field(..., description="Tuổi của người (số nguyên dương)")
    noio: str = Field(..., description="Nơi ở/địa chỉ của người")

    @classmethod
    def as_form(
        cls,
        image_id: int = Form(..., description="ID duy nhất cho ảnh"),
        image_path: str = Form(..., description="Đường dẫn lưu trữ ảnh"),
        class_id: int = Form(..., description="ID nhóm người"),
        ten: str = Form(..., description="Tên đầy đủ"),
        gioitinh: bool = Form(..., description="Giới tính (true=Nam, false=Nữ)"),
        tuoi: int = Form(..., description="Tuổi"),
        noio: str = Form(..., description="Nơi ở/địa chỉ")
    ):
        return cls(
            image_id=image_id,
            image_path=image_path,
            class_id=class_id,
            ten=ten,
            gioitinh=gioitinh,
            tuoi=tuoi,
            noio=noio
        )
class DeleteClassInput(BaseModel):
    class_id: int = Field(..., description="ID nhóm người cần xóa (sẽ xóa tất cả ảnh và thông tin của người này)")

    @classmethod
    def as_form(
        cls,
        class_id: int = Form(..., description="ID nhóm người cần xóa")
    ):
        return cls(
            class_id=class_id
        )
class DeleteImageInput(BaseModel):
    image_id: int = Field(..., description="ID ảnh cần xóa (chỉ xóa ảnh này, không ảnh hưởng ảnh khác cùng người)")

    @classmethod
    def as_form(
        cls,
        image_id: int = Form(..., description="ID ảnh cần xóa")
    ):
        return cls(
            image_id=image_id
        )
class EditEmbeddingInput(BaseModel):
    image_id: int = Field(..., description="ID ảnh cần chỉnh sửa (bắt buộc)")
    image_path: str = Field(None, description="Đường dẫn ảnh mới (tùy chọn)")

    @classmethod
    def as_form(cls,
                image_id: int = Form(..., description="ID ảnh cần chỉnh sửa"),
                image_path: str = Form(None, description="Đường dẫn ảnh mới (tùy chọn)")
                ):
        return cls(image_id=image_id, image_path=image_path)
    
class LoginRequest(BaseModel):
    username: str = Field(..., description="Tên đăng nhập (tối thiểu 6 ký tự)")
    passwrd: str = Field(..., description="Mật khẩu (tối thiểu 6 ký tự)")
    
    @classmethod
    def as_form(
        cls,
        username: str = Form(..., description="Tên đăng nhập"),
        passwrd: str = Form(..., description="Mật khẩu")
    ):
        return cls(
            username=username,
            passwrd=passwrd
        )

class LoginResponse(BaseModel):
    success: bool
    message: str
    @classmethod
    def as_response(
        cls,
        success: bool = Field(..., description="Kết quả đăng nhập thành công hay không"),
        message: str = Field(..., description="Thông báo kết quả đăng nhập")
    ):
        return cls(
            success=success,
            message=message
        )
        
class RegisterRequest(BaseModel):
    username: str = Field(..., description="Tên đăng nhập mới (tối thiểu 6 ký tự, phải duy nhất)")
    passwrd: str = Field(..., description="Mật khẩu mới (tối thiểu 6 ký tự)")
    
    @classmethod
    def as_form(
        cls,
        username: str = Form(..., description="Tên đăng nhập mới"),
        passwrd: str = Form(..., description="Mật khẩu mới")
    ):
        return cls(
            username=username,
            passwrd=passwrd
        )

class RegisterResponse(BaseModel):
    success: bool
    message: str
    
    @classmethod
    def as_response(
        cls,
        success: bool = Field(..., description="Kết quả đăng ký thành công hay không"),
        message: str = Field(..., description="Thông báo kết quả đăng ký")
    ):
        return cls(
            success=success,
            message=message
        )
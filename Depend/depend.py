from pydantic import BaseModel, Field, constr, conint
from fastapi import APIRouter, Depends, File, UploadFile, Form

class AddEmbeddingInput(BaseModel):
    image_id: int
    image_path: str
    class_id: int
    ten: str
    gioitinh: bool
    tuoi: int
    noio: str

    @classmethod
    def as_form(
        cls,
        image_id: int = Form(...),
        image_path: str = Form(...),
        class_id: int = Form(...),
        ten: str = Form(...),
        gioitinh: bool = Form(...),
        tuoi: int = Form(...),
        noio: str = Form(...)
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
    class_id: int

    @classmethod
    def as_form(
        cls,
        class_id: int = Form(...)
    ):
        return cls(
            class_id=class_id
        )
class DeleteImageInput(BaseModel):
    image_id: int

    @classmethod
    def as_form(
        cls,
        image_id: int = Form(...)
    ):
        return cls(
            image_id=image_id
        )
class EditEmbeddingInput(BaseModel):
    image_id: int
    image_path: str = None  # không required
    # Có thể bổ sung các trường khác nếu cần chỉnh sửa metadata

    @classmethod
    def as_form(cls,
                image_id: int = Form(...),
                image_path: str = Form(None),  # default None
                ):
        return cls(image_id=image_id, image_path=image_path)
    
class LoginRequest(BaseModel):
    username: str
    passwrd: str
    
    @classmethod
    def as_form(
        cls,
        username: constr(min_length=6) = Form(...),
        passwrd: constr(min_length=6) = Form(...)
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
    username: str
    passwrd: str
    
    @classmethod
    def as_form(
        cls,
        username: constr(min_length=6) = Form(...),
        passwrd: constr(min_length=6) = Form(...)
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
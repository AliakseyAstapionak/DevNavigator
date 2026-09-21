from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

class RegistrateUserSchema(BaseModel):

    username: str = Field(min_length=3, max_length=50, description="Имя пользователя")
    password: str = Field(min_length=6, max_length=20, description="Пароль")

    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str):
        if not value.replace('_', '').isalnum():
            raise ValueError("Имя пользователя может содержать только буквы, цифры и _")
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str):
        if not any(c.isalpha() for c in value):
            print("Ошибка регистрации: Пароль должен содержать хотя-бы одну букву")
            raise ValueError("Пароль должен содержать хотя-бы одну букву")
        if all(c.isalnum() for c in value):
            print("Ошибка регистрации: Пароль должен содержать хотя-бы один спецсимвол(напр. '!@#$%^&*')")
            raise ValueError("Пароль должен содержать хотя-бы один спецсимвол(напр. '!@#$%^&*')")
        return value

        
class LoginUserSchema(BaseModel):
    username: str = Field(description="Имя пользователя")
    password: str = Field(description="Пароль")

class UserResponseSchema(BaseModel):
    id: int
    username: str
    registrated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserActionResponseSchema(BaseModel):
    success: bool
    user: UserResponseSchema

class StatusResponseSchema(BaseModel):
    success: bool
    message: str

class UserPayload(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)

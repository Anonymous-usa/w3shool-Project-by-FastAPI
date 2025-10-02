from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import List, Optional, Annotated
from datetime import datetime


from validators import *


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: PasswordStr


class UserRegistrationSchema(UserLoginSchema):
    confirm_password: PasswordStr

    @model_validator(mode="before")
    def validate_password(cls, values):
        if values.get("password") != values.get("confirm_password"):
            raise ValueError("Passwords don't match!")
        return values


class UserCreateSchema(BaseModel):
    email: EmailStr = Field(..., title="Email пользователя")
    password: PasswordStr = Field(..., title="Пароль")
    is_active: bool = Field(False, title="Активен ли пользователь")
    roles: Optional[List[int]] = Field(default=None, title="ID ролей")
    permissions: Optional[List[int]] = Field(default=None, title="ID прав")



class PermissionSchema(BaseModel):
    id: int
    name: NameStr
    description: DescriptionStr_auth

    class Config:
        from_attributes = True



class RoleSchema(BaseModel):
    id: int
    name: NameStr
    description: DescriptionStr_auth
    permissions: List[PermissionSchema]

    class Config:
        from_attributes = True



class UserSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    roles: List[RoleSchema]
    permissions: List[PermissionSchema]

    class Config:
        from_attributes = True



class PermissionCreateSchema(BaseModel):
    name: NameStr
    description: DescriptionStr_auth


class RoleCreateSchema(BaseModel):
    name: NameStr
    description: DescriptionStr_auth
    permissions: Annotated[List[int], Field(min_length=1)]


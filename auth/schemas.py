from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Optional
from datetime import datetime


class UserLoginSchema(BaseModel):
    email: EmailStr 
    password: str


class UserRegistrationSchema(UserLoginSchema):
    confirm_password: str

    @model_validator(mode="before")
    def validate_password(cls, values):
        if values["password"] != values["confirm_password"]:
            raise ValueError("Passwords don't match!")
        return values


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    is_active: Optional[bool] = False
    roles: Optional[List[int]] = None
    permissions: Optional[List[int]] = None


class PermissionSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True


class RoleSchema(BaseModel):
    id: int
    name: str
    description: str
    permissions: List[PermissionSchema]

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    roles: List[RoleSchema]
    permissions: List[PermissionSchema]

    class Config:
        orm_mode = True

class PermissionCreateSchema(BaseModel):
    name: str
    description: str


class RoleCreateSchema(BaseModel):
    name: str
    description: str
    permissions: List[int]  

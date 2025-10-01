from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from auth.schemas import UserSchema



class ContentVersionCreateSchema(BaseModel):
    content_id: int
    version: int
    locale: str
    title: str
    body_md: str
    changelog: Optional[str] = None
    status: Optional[str] = "draft"
    created_by: Optional[int] = None


class ContentVersionSchema(BaseModel):
    id: int
    version: int
    locale: str
    title: str
    body_md: str
    changelog: Optional[str]
    status: str
    created_at: datetime
    author: Optional[UserSchema]

    class Config:
        orm_mode = True

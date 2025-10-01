from pydantic import BaseModel
from typing import Optional


class CategoryCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    slug: str


class CategorySchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    slug: str

    class Config:
        orm_mode = True

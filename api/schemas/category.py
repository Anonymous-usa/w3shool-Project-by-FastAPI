from pydantic import BaseModel
from typing import Optional, List

from api.schemas.content import ContentSchema
from api.schemas.lesson import LessonSchema


class CategoryCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    slug: str

class CategoryUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None

class CategorySchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    slug: str

    class Config:
        orm_mode = True


class CategoryWithRelationsSchema(CategorySchema):
    content: List[ContentSchema]
    lessons: List[LessonSchema]
    children: List[CategorySchema]
    parent: Optional[CategorySchema]

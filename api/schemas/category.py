from pydantic import BaseModel, Field
from typing import Optional, List, Annotated, TYPE_CHECKING
from validators import *

if TYPE_CHECKING:
    from api.schemas.content import ContentSchema
    from api.schemas.lesson import LessonSchema


class CategoryCreateSchema(BaseModel):
    title: TitleStr
    description: Optional[Annotated[str, Field(max_length=500)]] = None
    slug: SlugStr


class CategoryUpdateSchema(BaseModel):
    title: Optional[TitleStr] = None
    description: Optional[Annotated[str, Field(max_length=500)]] = None
    slug: Optional[SlugStr] = None


class CategorySchema(BaseModel):
    id: int
    title: TitleStr
    description: Optional[str]
    slug: SlugStr

    class Config:
        from_attributes = True


class CategoryWithRelationsSchema(CategorySchema):
    content: List["ContentSchema"]
    lessons: List["LessonSchema"]
    children: List["CategorySchema"]
    parent: Optional["CategorySchema"]




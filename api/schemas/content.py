from pydantic import BaseModel
from typing import Optional, List
from .category import CategorySchema
from .content_version import ContentVersionSchema
from .example import ExampleSchema


class ContentCreateSchema(BaseModel):
    category_id: int
    slug: str
    default_locale: str = "en"
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = False


class ContentSchema(BaseModel):
    id: int
    slug: str
    default_locale: str
    tags: Optional[List[str]]
    is_published: bool
    category: CategorySchema
    versions: List[ContentVersionSchema]
    examples: List[ExampleSchema]

    class Config:
        orm_mode = True

class ContentUpdateSchema(BaseModel):
    slug: Optional[str] = None
    default_locale: Optional[str] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None
    category_id: Optional[int] = None

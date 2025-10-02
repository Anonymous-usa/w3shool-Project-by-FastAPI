from pydantic import BaseModel, Field
from typing import Optional, List, Annotated, TYPE_CHECKING
from validators import *

if TYPE_CHECKING:
    from api.schemas.category import CategorySchema
    from api.schemas.content_version import ContentVersionSchema
    from api.schemas.example import ExampleSchema


class ContentCreateSchema(BaseModel):
    category_id: Annotated[int, Field(gt=0, description="ID категории, должен быть > 0")]
    slug: SlugStr = Field(..., description="Уникальный slug (латиница, цифры, дефис)")
    default_locale: LocaleStr = Field("en", description="Язык по умолчанию (ISO-код)")
    tags: Optional[Annotated[List[TagStr], Field(min_length=1, max_length=20)]] = Field(
        None, description="Список тегов (до 20)"
    )
    is_published: bool = Field(False, description="Флаг публикации")


class ContentSchema(BaseModel):
    id: int
    slug: SlugStr
    default_locale: LocaleStr
    tags: Optional[List[TagStr]]
    is_published: bool
    category: "CategorySchema"
    versions: List["ContentVersionSchema"]
    examples: List["ExampleSchema"]

    class Config:
        from_attributes = True


class ContentUpdateSchema(BaseModel):
    slug: Optional[SlugStr] = None
    default_locale: Optional[LocaleStr] = None
    tags: Optional[Annotated[List[TagStr], Field(min_length=1, max_length=20)]] = None
    is_published: Optional[bool] = None
    category_id: Optional[Annotated[int, Field(gt=0)]] = None




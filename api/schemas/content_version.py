from pydantic import BaseModel, Field
from typing import Optional, Literal, Annotated
from datetime import datetime
from auth.schemas import UserSchema


from validators import *


class ContentVersionCreateSchema(BaseModel):
    content_id: Annotated[int, Field(gt=0)]
    version: Annotated[int, Field(ge=1, description="Номер версии, начиная с 1")]
    locale: LocaleStr
    title: TitleStr
    body_md: BodyStr
    changelog: Optional[ChangelogStr] = None
    status: Literal["draft", "published", "archived"] = "draft"
    created_by: Optional[int] = Field(None, description="ID пользователя-автора")


class ContentVersionSchema(BaseModel):
    id: int
    version: Annotated[int, Field(ge=1)]
    locale: LocaleStr
    title: TitleStr
    body_md: BodyStr
    changelog: Optional[str]
    status: Literal["draft", "published", "archived"]
    created_at: datetime
    author: Optional[UserSchema]

    class Config:
        from_attributes = True



class ContentVersionUpdateSchema(BaseModel):
    version: Optional[Annotated[int, Field(ge=1)]] = None
    locale: Optional[LocaleStr] = None
    title: Optional[TitleStr] = None
    body_md: Optional[BodyStr] = None
    changelog: Optional[ChangelogStr] = None
    status: Optional[Literal["draft", "published", "archived"]] = None

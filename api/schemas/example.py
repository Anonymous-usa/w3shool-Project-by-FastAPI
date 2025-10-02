from pydantic import BaseModel, Field
from typing import Optional, Annotated
from .content import ContentSchema


from validators import *


class ExampleCreateSchema(BaseModel):
    content_id: Annotated[int, Field(gt=0, description="ID контента, должен быть > 0")]
    language: LangStr = Field(..., description="Язык примера (например, python, js)")
    title: TitleStr = Field(..., description="Название примера")
    code: CodeStr = Field(..., description="Кодовый фрагмент")
    runnable: bool = Field(True, description="Можно ли запускать пример")


class ExampleSchema(BaseModel):
    id: int
    language: LangStr
    title: TitleStr
    code: CodeStr
    runnable: bool
    content: ContentSchema

    class Config:
        from_attributes = True



class ExampleUpdateSchema(BaseModel):
    language: Optional[LangStr] = None
    title: Optional[TitleStr] = None
    code: Optional[CodeStr] = None
    runnable: Optional[bool] = None
    content_id: Optional[Annotated[int, Field(gt=0)]] = None

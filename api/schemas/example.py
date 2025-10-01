from pydantic import BaseModel
from typing import Optional
from .content import ContentSchema


class ExampleCreateSchema(BaseModel):
    content_id: int
    language: str
    title: str
    code: str
    runnable: Optional[bool] = True


class ExampleSchema(BaseModel):
    id: int
    language: str
    title: str
    code: str
    runnable: bool
    content: ContentSchema

    class Config:
        orm_mode = True

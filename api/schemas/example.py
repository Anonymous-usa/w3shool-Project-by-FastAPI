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

class ExampleUpdateSchema(BaseModel):
    language: Optional[str] = None
    title: Optional[str] = None
    code: Optional[str] = None
    runnable: Optional[bool] = None
    content_id: Optional[int] = None

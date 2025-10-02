from pydantic import BaseModel
from typing import Optional, List
from .category import CategorySchema
from .quiz import QuizSchema


class LessonCreateSchema(BaseModel):
    category_id: int
    title: str
    description: Optional[str] = None
    order_index: int


class LessonSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    order_index: int
    category: CategorySchema
    quizzes: List[QuizSchema]

    class Config:
        orm_mode = True

class LessonUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
    category_id: Optional[int] = None

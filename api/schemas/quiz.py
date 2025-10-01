from pydantic import BaseModel
from typing import Optional, List
from .lesson import LessonSchema


class QuizCreateSchema(BaseModel):
    lesson_id: int
    title: str
    description: Optional[str] = None
    questions: List[dict]


class QuizSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    questions: List[dict]
    lesson: LessonSchema

    class Config:
        orm_mode = True

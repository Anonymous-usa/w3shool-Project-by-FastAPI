from pydantic import BaseModel, Field
from typing import Optional, List, Annotated, TYPE_CHECKING
from validators import *

if TYPE_CHECKING:
    from .lesson import LessonSchema


class QuestionSchema(BaseModel):
    text: Annotated[str, Field(min_length=1, max_length=500)]
    options: Annotated[List[str], Field(min_length=2, max_length=10)]
    answer: Annotated[int, Field(ge=0, description="Индекс правильного ответа в options")]


class QuizCreateSchema(BaseModel):
    lesson_id: Annotated[int, Field(gt=0, description="ID урока, должен быть > 0")]
    title: TitleStr = Field(..., description="Название теста (3-200 символов)")
    description: Optional[DescriptionStr] = Field(None, description="Описание теста, до 1000 символов")
    questions: Annotated[List[QuestionSchema], Field(min_length=1)] = Field(..., description="Список вопросов")


class QuizSchema(BaseModel):
    id: int
    title: TitleStr
    description: Optional[str]
    questions: List[QuestionSchema]
    lesson: "LessonSchema"

    class Config:
        from_attributes = True


class QuizUpdateSchema(BaseModel):
    title: Optional[TitleStr] = None
    description: Optional[DescriptionStr] = None
    questions: Optional[Annotated[List[QuestionSchema], Field(min_length=1)]] = None
    lesson_id: Optional[Annotated[int, Field(gt=0)]] = None



from pydantic import BaseModel, Field
from typing import Optional, List, Annotated, TYPE_CHECKING
from validators import *

if TYPE_CHECKING:
    from .quiz import QuizSchema
    from .category import CategorySchema


class LessonCreateSchema(BaseModel):
    category_id: Annotated[int, Field(gt=0, description="ID категории, должен быть > 0")]
    title: TitleStr = Field(..., description="Название урока (3-200 символов)")
    description: Optional[DescriptionStr] = Field(None, description="Описание урока, до 1000 символов")
    order_index: Annotated[int, Field(ge=0, description="Порядковый номер урока (>=0)")]


class LessonSchema(BaseModel):
    id: int
    title: TitleStr
    description: Optional[str]
    order_index: Annotated[int, Field(ge=0)]
    category: "CategorySchema"
    quizzes: List["QuizSchema"]

    class Config:
        from_attributes = True


class LessonUpdateSchema(BaseModel):
    title: Optional[TitleStr] = None
    description: Optional[DescriptionStr] = None
    order_index: Optional[Annotated[int, Field(ge=0)]] = None
    category_id: Optional[Annotated[int, Field(gt=0)]] = None



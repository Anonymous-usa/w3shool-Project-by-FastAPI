from sqlalchemy import Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import BaseModel

class Quiz(BaseModel):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    questions: Mapped[list[dict]] = mapped_column(JSON)

    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="quizzes")

    @property
    def _get_models(self):
        from api.models.lessons import Lesson
        return Lesson
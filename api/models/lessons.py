from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import BaseModel

class Lesson(BaseModel):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship("Category", back_populates="lessons")
    
    quizzes: Mapped[list["Quiz"]] = relationship("Quiz", back_populates="lesson", cascade="all, delete")

    @property
    def _get_models(self):
        from api.models.category import Category
        from api.models.quiz import Quiz
        return Category, Quiz

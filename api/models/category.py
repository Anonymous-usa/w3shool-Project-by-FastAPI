from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    
    slug: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str ] = mapped_column(Text)

    parent: Mapped["Category" ] = relationship("Category", remote_side=[id])
    children: Mapped[list["Category"]] = relationship("Category", back_populates="parent", cascade="all, delete")

    content: Mapped[list["Content"]] = relationship("Content", back_populates="category", cascade="all, delete")

    lessons: Mapped[list["Lesson"]] = relationship("Lesson", back_populates="category", cascade="all, delete")
    @property
    def _get_models(self):
        from api.models.content import Content
        from api.models.lessons import Lesson
        return Content, Lesson


from sqlalchemy import Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import BaseModel
class Content(BaseModel):
    __tablename__ = "content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


    slug: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    default_locale: Mapped[str] = mapped_column(String(8), default="en")
    tags: Mapped[list[dict] | None] = mapped_column(JSON)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship("Category", back_populates="content")
    
    versions: Mapped[list["ContentVersion"]] = relationship("ContentVersion", back_populates="content", cascade="all, delete")
    
    examples: Mapped[list["Example"]] = relationship("Example", back_populates="content", cascade="all, delete")

    @property
    def _get_models(self):
        from api.models.category import Category
        from api.models.example import Example
        from api.models.content_version import ContentVersion
        return Category, Example, ContentVersion
from sqlalchemy import Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import BaseModel

class Example(BaseModel):
    __tablename__ = "examples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    language: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    runnable: Mapped[bool] = mapped_column(Boolean, default=True)

    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), nullable=False)
    content: Mapped["Content"] = relationship("Content", back_populates="examples")
    
    @property
    def _get_models(self):
        from api.models.content import Content
        return Content

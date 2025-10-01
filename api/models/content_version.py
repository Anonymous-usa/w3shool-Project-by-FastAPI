from datetime import datetime
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import BaseModel

class ContentVersion(BaseModel):
    __tablename__ = "content_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    version: Mapped[int] = mapped_column(Integer, nullable=False)
    locale: Mapped[str] = mapped_column(String(8), default="en")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body_md: Mapped[str] = mapped_column(Text, nullable=False)
    changelog: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(16), default="draft")
    
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), nullable=False)
    content: Mapped["Content"] = relationship("Content", back_populates="versions")
    
    author: Mapped["User"] = relationship("User")

    @property
    def _get_user_model(self):
        from auth.models import User  
        from api.models.content import Content
        return User, Content
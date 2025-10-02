from database import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Boolean, DateTime, Table, Column, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime


user_permissions = Table(
    "user_permissions",
    BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key = True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key = True)
)

role_permissions = Table(
    "role_permissions",
    BaseModel.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key = True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key = True)
)

user_roles = Table(
    "user_roles",
    BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key = True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key = True)
)


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)

    email: Mapped[str] = mapped_column(String(100), unique = True, nullable = False)
    password_hash: Mapped[str] = mapped_column(String, nullable = False)
    
    permissions: Mapped[list["Permission"]] = relationship("Permission", secondary = user_permissions, back_populates="users")
    roles: Mapped[list["Role"]] = relationship("Role", secondary = user_roles, back_populates="users")

    is_active: Mapped[bool] = mapped_column(Boolean, default = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.now())


class Permission(BaseModel):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)

    name: Mapped[str] = mapped_column(String, nullable = False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    users: Mapped[list["User"]] = relationship("User", secondary = user_permissions, back_populates="permissions")
    roles: Mapped[list["Role"]] = relationship("Role", secondary = role_permissions, back_populates="permissions")


class Role(BaseModel):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)

    name: Mapped[str] = mapped_column(String, unique = True, nullable = False)
    description: Mapped[str] = mapped_column(Text, nullable = False)

    users: Mapped[list["User"]] = relationship("User", secondary = user_roles, back_populates="roles")
    permissions: Mapped[list["Permission"]] = relationship("Permission", secondary = role_permissions, back_populates="roles")


class BlackListToken(BaseModel):
    __tablename__ = "blacklist_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)

    token: Mapped[str] = mapped_column(String, nullable = False)


class EmailVerification(BaseModel):
    __tablename__ = "email_verifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now() + timedelta(minutes=10))

    user: Mapped["User"] = relationship("User")
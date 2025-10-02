from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth.schemas import *
from auth.models import User, BlackListToken
from auth.utils import *
from fastapi.responses import JSONResponse
from permissions import has_permission
from .models import Permission
auth_router = APIRouter(prefix="/auth", tags=["Authentication endpoints"])

@auth_router.post("/login", status_code=status.HTTP_200_OK, summary="Authenticate user and return access token")
def login(data: UserLoginSchema):
    user = is_authenticated(data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return generate_token(user.id)

@auth_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema, summary="Register a new user")
def register(data: UserRegistrationSchema, db: Session = Depends(get_db)):
    existing = is_authenticated(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        is_active=True
    )

    learner_role = db.query(Role).filter(Role.name == "learner").first()
    if learner_role:
        user.roles.append(learner_role)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@auth_router.post("/logout", summary="Invalidate current token by adding it to blacklist")
def logout(token: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db.add(BlackListToken(token=token))
    db.commit()
    return JSONResponse(content={"detail": "Logged out successfully"}, status_code=200)

@auth_router.get("/me", response_model=UserSchema, summary="Get current authenticated user")
def me(user: User = Depends(get_current_user)):
    return user


@auth_router.post("/add-role-to-user", status_code=status.HTTP_200_OK)
async def add_role_to_user(user_id:int, role_id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    if user and role:
        user.roles.append(role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"messege":"Role added to user"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User or role not found")

@auth_router.post("/add_role",  status_code=status.HTTP_201_CREATED)
async def create_role(role_data: RoleCreateSchema, db:Session = Depends(get_db)):
    role = db.query(Role).filter(Role.name == role_data.name).first()
    if not role:
        role = Role(name = role_data.name, description = role_data.description)
    permissions = db.query(Permission).filter(Permission.id.in_(role_data.permissions)).all()
    role.permissions.extend(permissions)
    db.add(role)
    db.commit()
    db.refresh(role)
    return {"message": "Role added successfully!"} 
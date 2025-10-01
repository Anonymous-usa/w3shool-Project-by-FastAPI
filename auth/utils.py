from passlib.hash import bcrypt
from decouple import config
import time
import jwt
from database import SessionLocal
from .models import User, BlackListToken, Role
from sqlalchemy.orm import selectinload
from fastapi import Request, HTTPException, Depends

SECRET_KEY = config("SECRET_KEY")
AUTH_ALGORITHM = config("AUTH_ALGORITHM")
 

def hash_password(password: str):
    return bcrypt.hash(password)

def verify_password(password:str, hashed_password:str):
    return bcrypt.verify(password, hashed_password)

def is_authenticated(email):
    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    try:
        if user:
            return user
        return None
    finally:
        db.close()





def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=AUTH_ALGORITHM )
    return response_token(token)

def response_token(token:str):
    return {"access_token": token}

def decode_jwt(token:str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[AUTH_ALGORITHM])
    return payload if payload["expires"] >= time.time() else None


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials





class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid
    
 


def get_current_user(token = Depends(JWTBearer())):
    db = SessionLocal()
    payload = decode_jwt(token)
    if payload:
        user = db.query(User).options(selectinload(User.permissions), selectinload(User.roles).selectinload(Role.permissions)).filter(User.id  == payload["user_id"]).first()
        if user:
            return user


def is_token_blocked(token:str):
    db = SessionLocal()
    black_list_token = db.query(BlackListToken).filter(BlackListToken.token == token).first()
    if black_list_token:
        return True
    return False

    
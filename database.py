from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///./w3school_db.db")

SessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit = False )

class BaseModel(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


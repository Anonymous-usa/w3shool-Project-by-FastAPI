from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from api.models.lessons import Lesson
from api.schemas.lesson import LessonCreateSchema, LessonUpdateSchema, LessonSchema
from permissions import has_permission

router = APIRouter(prefix="/lesson", tags=["Lesson endpoints"])

@router.post("/create", response_model=LessonSchema, status_code=201, summary="Create a new lesson", dependencies=[Depends(has_permission("CREATE_LESSONS"))])
def create_lesson(data: LessonCreateSchema, db: Session = Depends(get_db)):
    lesson = Lesson(
        category_id=data.category_id,
        title=data.title,
        description=data.description,
        order_index=data.order_index
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson

@router.put("/update/{id}", response_model=LessonSchema, summary="Update a lesson by ID", dependencies=[Depends(has_permission("UPDATE_LESSONS"))])
def update_lesson(id: int, data: LessonUpdateSchema, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if data.title is not None:
        lesson.title = data.title
    if data.description is not None:
        lesson.description = data.description
    if data.order_index is not None:
        lesson.order_index = data.order_index
    if data.category_id is not None:
        lesson.category_id = data.category_id

    db.commit()
    db.refresh(lesson)
    return lesson

@router.delete("/delete/{id}", status_code=204, summary="Delete a lesson by ID", dependencies=[Depends(has_permission("DELETE_LESSONS"))])
def delete_lesson(id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.delete(lesson)
    db.commit()
    return

@router.get("/get-all", response_model=list[LessonSchema], summary="Get all lessons", dependencies=[Depends(has_permission("READ_LESSONS"))])
def get_all_lessons(db: Session = Depends(get_db)):
    return db.query(Lesson).options(
        joinedload(Lesson.category),
        joinedload(Lesson.quizzes)
    ).all()

@router.get("/{id}", response_model=LessonSchema, summary="Get a lesson by ID", dependencies=[Depends(has_permission("READ_LESSONS"))])
def get_lesson_by_id(id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).options(
        joinedload(Lesson.category),
        joinedload(Lesson.quizzes)
    ).filter(Lesson.id == id).first()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

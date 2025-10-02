from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from api.models.quiz import Quiz
from api.schemas.quiz import QuizCreateSchema, QuizUpdateSchema, QuizSchema
from permissions import has_permission

quiz_router = APIRouter(prefix="/quiz", tags=["Quiz endpoints"])

@quiz_router.post("/create", response_model=QuizSchema, status_code=201, summary="Create a new quiz", dependencies=[Depends(has_permission("CREATE_QUIZ"))])
def create_quiz(data: QuizCreateSchema, db: Session = Depends(get_db)):
    quiz = Quiz(
        lesson_id=data.lesson_id,
        title=data.title,
        description=data.description,
        questions=data.questions
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz

@quiz_router.put("/update/{id}", response_model=QuizSchema, summary="Update a quiz by ID", dependencies=[Depends(has_permission("UPDATE_QUIZ"))])
def update_quiz(id: int, data: QuizUpdateSchema, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if data.title is not None:
        quiz.title = data.title
    if data.description is not None:
        quiz.description = data.description
    if data.questions is not None:
        quiz.questions = data.questions
    if data.lesson_id is not None:
        quiz.lesson_id = data.lesson_id

    db.commit()
    db.refresh(quiz)
    return quiz

@quiz_router.delete("/delete/{id}", status_code=204, summary="Delete a quiz by ID", dependencies=[Depends(has_permission("DELETE_QUIZ"))])
def delete_quiz(id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    db.delete(quiz)
    db.commit()
    return

@quiz_router.get("/get-all", response_model=list[QuizSchema], summary="Get all quizzes", dependencies=[Depends(has_permission("READ_QUIZ"))])
def get_all_quizzes(db: Session = Depends(get_db)):
    return db.query(Quiz).options(joinedload(Quiz.lesson)).all()

@quiz_router.get("/{id}", response_model=QuizSchema, summary="Get a quiz by ID", dependencies=[Depends(has_permission("READ_QUIZ"))])
def get_quiz_by_id(id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).options(joinedload(Quiz.lesson)).filter(Quiz.id == id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

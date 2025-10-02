from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from api.models.example import Example
from api.schemas.example import ExampleCreateSchema, ExampleUpdateSchema, ExampleSchema
from permissions import has_permission

example_router = APIRouter(prefix="/example", tags=["Example endpoints"])

@example_router.post("/create", response_model=ExampleSchema, status_code=201, summary="Create a new example", dependencies=[Depends(has_permission("CREATE_EXAMPLES"))])
def create_example(data: ExampleCreateSchema, db: Session = Depends(get_db)):
    example = Example(
        content_id=data.content_id,
        language=data.language,
        title=data.title,
        code=data.code,
        runnable=data.runnable
    )
    db.add(example)
    db.commit()
    db.refresh(example)
    return example

@example_router.put("/update/{id}", response_model=ExampleSchema, summary="Update an example by ID", dependencies=[Depends(has_permission("UPDATE_EXAMPLES"))])
def update_example(id: int, data: ExampleUpdateSchema, db: Session = Depends(get_db)):
    example = db.query(Example).filter(Example.id == id).first()
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")

    if data.language is not None:
        example.language = data.language
    if data.title is not None:
        example.title = data.title
    if data.code is not None:
        example.code = data.code
    if data.runnable is not None:
        example.runnable = data.runnable
    if data.content_id is not None:
        example.content_id = data.content_id

    db.commit()
    db.refresh(example)
    return example

@example_router.delete("/delete/{id}", status_code=204, summary="Delete an example by ID", dependencies=[Depends(has_permission("DELETE_EXAMPLES"))])
def delete_example(id: int, db: Session = Depends(get_db)):
    example = db.query(Example).filter(Example.id == id).first()
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")
    db.delete(example)
    db.commit()
    return

@example_router.get("/get-all", response_model=list[ExampleSchema], summary="Get all examples", dependencies=[Depends(has_permission("READ_EXAMPLES"))])
def get_all_examples(db: Session = Depends(get_db)):
    return db.query(Example).options(joinedload(Example.content)).all()

@example_router.get("/{id}", response_model=ExampleSchema, summary="Get an example by ID", dependencies=[Depends(has_permission("READ_EXAMPLES"))])
def get_example_by_id(id: int, db: Session = Depends(get_db)):
    example = db.query(Example).options(joinedload(Example.content)).filter(Example.id == id).first()
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")
    return example

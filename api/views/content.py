from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from api.models.content import Content
from api.schemas.content import ContentCreateSchema, ContentUpdateSchema, ContentSchema
from permissions import has_permission

content_router = APIRouter(prefix="/content", tags=["Content endpoints"])

@content_router.post("/create", response_model=ContentSchema, status_code=201, summary="Create new content", dependencies=[Depends(has_permission("CREATE_CONTENT"))])
def create_content(data: ContentCreateSchema, db: Session = Depends(get_db)):
    content = Content(
        category_id=data.category_id,
        slug=data.slug,
        default_locale=data.default_locale,
        tags=[{"tag": tag} for tag in data.tags] if data.tags else None,
        is_published=data.is_published
    )
    db.add(content)
    db.commit()
    db.refresh(content)
    return content

@content_router.put("/update/{id}", response_model=ContentSchema, summary="Update content by ID", dependencies=[Depends(has_permission("UPDATE_CONTENT"))])
def update_content(id: int, data: ContentUpdateSchema, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if data.slug is not None:
        content.slug = data.slug
    if data.default_locale is not None:
        content.default_locale = data.default_locale
    if data.tags is not None:
        content.tags = [{"tag": tag} for tag in data.tags]
    if data.is_published is not None:
        content.is_published = data.is_published
    if data.category_id is not None:
        content.category_id = data.category_id

    db.commit()
    db.refresh(content)
    return content

@content_router.delete("/delete/{id}", status_code=204, summary="Delete content by ID", dependencies=[Depends(has_permission("DELETE_CONTENT"))])
def delete_content(id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    db.delete(content)
    db.commit()
    return

@content_router.get("/get-all", response_model=list[ContentSchema], summary="Get all content", dependencies=[Depends(has_permission("READ_CONTENT"))])
def get_all_content(db: Session = Depends(get_db)):
    return db.query(Content).options(
        joinedload(Content.category),
        joinedload(Content.versions),
        joinedload(Content.examples)
    ).all()

@content_router.get("/{id}", response_model=ContentSchema, summary="Get content by ID", dependencies=[Depends(has_permission("READ_CONTENT"))])
def get_content_by_id(id: int, db: Session = Depends(get_db)):
    content = db.query(Content).options(
        joinedload(Content.category),
        joinedload(Content.versions),
        joinedload(Content.examples)
    ).filter(Content.id == id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from api.models.content_version import ContentVersion
from api.schemas.content_version import ContentVersionCreateSchema, ContentVersionUpdateSchema, ContentVersionSchema
from permissions import has_permission

content_version_router = APIRouter(prefix="/content-version", tags=["ContentVersion endpoints"])

@content_version_router.post("/create", response_model=ContentVersionSchema, status_code=201, summary="Create a new content version", dependencies=[Depends(has_permission("CREATE_CONTENT_VERSIONS"))])
def create_content_version(data: ContentVersionCreateSchema, db: Session = Depends(get_db)):
    version = ContentVersion(
        content_id=data.content_id,
        version=data.version,
        locale=data.locale,
        title=data.title,
        body_md=data.body_md,
        changelog=data.changelog,
        status=data.status,
        created_by=data.created_by
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return version

@content_version_router.put("/update/{id}", response_model=ContentVersionSchema, summary="Update a content version by ID", dependencies=[Depends(has_permission("UPDATE_CONTENT_VERSIONS"))])
def update_content_version(id: int, data: ContentVersionUpdateSchema, db: Session = Depends(get_db)):
    version = db.query(ContentVersion).filter(ContentVersion.id == id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Content version not found")

    if data.version is not None:
        version.version = data.version
    if data.locale is not None:
        version.locale = data.locale
    if data.title is not None:
        version.title = data.title
    if data.body_md is not None:
        version.body_md = data.body_md
    if data.changelog is not None:
        version.changelog = data.changelog
    if data.status is not None:
        version.status = data.status

    db.commit()
    db.refresh(version)
    return version

@content_version_router.delete("/delete/{id}", status_code=204, summary="Delete a content version by ID", dependencies=[Depends(has_permission("DELETE_CONTENT_VERSIONS"))])
def delete_content_version(id: int, db: Session = Depends(get_db)):
    version = db.query(ContentVersion).filter(ContentVersion.id == id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Content version not found")
    db.delete(version)
    db.commit()
    return

@content_version_router.get("/get-all", response_model=list[ContentVersionSchema], summary="Get all content versions", dependencies=[Depends(has_permission("READ_CONTENT_VERSIONS"))])
def get_all_content_versions(db: Session = Depends(get_db)):
    return db.query(ContentVersion).options(joinedload(ContentVersion.author)).all()

@content_version_router.get("/{id}", response_model=ContentVersionSchema, summary="Get a content version by ID", dependencies=[Depends(has_permission("READ_CONTENT_VERSIONS"))])
def get_content_version_by_id(id: int, db: Session = Depends(get_db)):
    version = db.query(ContentVersion).options(joinedload(ContentVersion.author)).filter(ContentVersion.id == id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Content version not found")
    return version

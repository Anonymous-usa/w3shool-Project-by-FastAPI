from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from api.models.category import Category
from api.schemas.category import CategoryCreateSchema, CategoryUpdateSchema, CategorySchema, CategoryWithRelationsSchema
from permissions import has_permission

category_router = APIRouter(prefix="/category", tags=["Category endpoints"])

@category_router.post("/create", response_model=CategorySchema, status_code=201, summary="Create a new category", dependencies=[Depends(has_permission("CREATE_CATEGORIES"))])
def create_category(data: CategoryCreateSchema, db: Session = Depends(get_db)):
    category = Category(
        title=data.title,
        description=data.description,
        slug=data.slug
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@category_router.put("/update/{id}", response_model=CategorySchema, summary="Update an existing category by ID", dependencies=[Depends(has_permission("UPDATE_CATEGORIES"))])
def update_category(id: int, data: CategoryUpdateSchema, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if data.title is not None:
        category.title = data.title
    if data.description is not None:
        category.description = data.description
    if data.slug is not None:
        category.slug = data.slug

    db.commit()
    db.refresh(category)
    return category

@category_router.delete("/delete/{id}", status_code=204, summary="Delete a category by ID", dependencies=[Depends(has_permission("DELETE_CATEGORIES"))])
def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return

@category_router.get("/get-all", response_model=list[CategorySchema], summary="Get all categories", dependencies=[Depends(has_permission("READ_CATEGORIES"))])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@category_router.get("/{id}", response_model=CategoryWithRelationsSchema, summary="Get a category by ID", dependencies=[Depends(has_permission("READ_CATEGORIES"))])
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    category = db.query(Category).options(
        joinedload(Category.content),
        joinedload(Category.lessons),
        joinedload(Category.children),
        joinedload(Category.parent)
    ).filter(Category.id == id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

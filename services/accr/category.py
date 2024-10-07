from typing import Optional
from sqlalchemy.orm import Session
from models.accr import (
    Category,
)  # Предполагается, что у вас есть модель Category в models.py
from schemas import (
    CategoryCreate,
    CategoryUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class CategoryService(ServiceBase[Category, CategoryCreate, CategoryUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Category]:
        return db.query(Category).filter(Category.name == name).first()


category_service = CategoryService(Category)

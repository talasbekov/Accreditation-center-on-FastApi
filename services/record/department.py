from typing import Optional
from sqlalchemy.orm import Session

from models import Department  # Предполагается, что у вас есть модель Department в models.py
from schemas import (
    DepartmentCreate,
    DepartmentUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий

from services.base import ServiceBase


class DepartmentService(ServiceBase[Department, DepartmentCreate, DepartmentUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Department]:
        return db.query(Department).filter(Department.name == name).first()


department_service = DepartmentService(Department)

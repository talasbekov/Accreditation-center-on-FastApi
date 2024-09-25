from typing import Type
from sqlalchemy.orm import Session
from models import (
    Employer,
)  # Предполагается, что у вас есть модель Employer в models.py
from schemas import (
    EmployerCreate,
    EmployerUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class EmployerService(ServiceBase[Employer, EmployerCreate, EmployerUpdate]):

    def get_by_status(self, db: Session, status: str) -> list[Type[Employer]]:
        return db.query(Employer).filter(Employer.status == status).all()


employer_service = EmployerService(Employer)

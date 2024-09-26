from typing import Type
from sqlalchemy.orm import Session
from models import (
    Employer,
    Record
)  # Предполагается, что у вас есть модель Employer в models.py
from schemas import (
    EmployerCreate,
    EmployerUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class EmployerService(ServiceBase[Employer, EmployerCreate, EmployerUpdate]):

    # Количество сотрудников по штату всего департамента
    def get_count_emp_by_state(self):
        return 136

    # Количество сотрудников по списку всего департамента
    def get_count_emp_by_list(self, db: Session):
        return db.query(self.model).count()

    # Количество вакантных мест в департаменте
    def get_count_vacant(self):
        return self.get_count_emp_by_state - self.get_count_emp_by_list

    # Количество сотрудников по статусу всего департамента
    def get_count_emp_by_status(self, db: Session, status: str):
        return db.query(self.model).filter(self.model.status == status).count()

    # Количество сотрудников которые в строю всего департамента
    def get_count_emp_in_service(self):
        return self.get_count_emp_by_list - self.get_count_emp_by_status

    # Все сотрудники по статусу, например: на больничном, и т.д.
    def get_emp_by_status(self, db: Session, status: str) -> list[Type[Employer]]:
        return db.query(self.model).filter(self.model.status == status).all()

    # Количество сотрудников по штату в управлении
    def get_count_emp_by_state_from_directorate(self, db: Session, record_id: int):
        directorate = db.query(Record).filter(Record.id == record_id).first()
        return directorate.count_state

    # Количество сотрудников по списку в управлении
    def get_count_emp_by_list_from_directorate(self, db: Session, record_id: int):
        return db.query(self.model).filter(self.model.record_id == record_id).count()

    # Количество сотрудников которые в строю в управлении
    def get_count_emp_in_service_from_directorate(self):
        return self.get_count_emp_by_list_from_directorate - self.get_emp_by_status_from_directorate

    # Количество вакантных мест в управлении
    def get_count_vacant_in_directorate(self):
        return self.get_count_emp_by_state_from_directorate - self.get_count_emp_by_list_from_directorate

    # Все сотрудники по статусу в управлении
    def get_emp_by_status_from_directorate(self, db: Session, status: str, record_id: int):
        return db.query(self.model).filter(
            self.model.status == status, self.model.record_id == record_id
        ).all()


employer_service = EmployerService(Employer)

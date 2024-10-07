from typing import Type
from sqlalchemy.orm import Session
from models import (
    Employer,
    Division,
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
    def get_count_vacant(self, db: Session):
        state_count = self.get_count_emp_by_state()
        list_count = self.get_count_emp_by_list(db)

        if not isinstance(state_count, int):
            raise ValueError(
                f"get_count_emp_by_state() returned {type(state_count)}, expected int."
            )

        if not isinstance(list_count, int):
            raise ValueError(
                f"get_count_emp_by_list() returned {type(list_count)}, expected int."
            )

        return state_count - list_count

    # Количество сотрудников по статусу всего департамента
    def get_count_emp_by_status(self, db: Session, status: str):
        return db.query(self.model).filter(self.model.status == status).count()

    # # Количество сотрудников по статусу всего департамента
    # def get_count_emp_by_all_status(self, db: Session):
    #     statuses = []
    #     for status in EmpStatusEnum:
    #         emp_count_by_all_status = (
    #             db.query(self.model).filter(self.model.status == status).count()
    #         )
    #         statuses.append(emp_count_by_all_status)
    #     return sum(statuses)

    # Количество сотрудников которые в строю всего департамента
    def get_count_emp_in_service(self, db: Session):
        return self.get_count_emp_by_list(db) - self.get_count_emp_by_all_status(db)

    # Все сотрудники по статусу, например: на больничном, и т.д.
    def get_emp_by_status(self, db: Session, status: str) -> list[Type[Employer]]:
        return db.query(self.model).filter(self.model.status == status).all()

    # Количество сотрудников по штату в управлении
    def get_count_emp_by_state_from_directorate(self, db: Session, division_id: int):
        directorate = db.query(Division).filter(Division.id == division_id).first()
        return int(directorate.count_state)

    # Количество сотрудников по списку в управлении
    def get_count_emp_by_list_from_directorate(self, db: Session, division_id: int):
        return db.query(self.model).filter(self.model.division_id == division_id).count()

    # Количество вакантных мест в управлении
    def get_count_vacant_in_directorate(self, db: Session, division_id: int):
        return self.get_count_emp_by_state_from_directorate(
            db, division_id
        ) - self.get_count_emp_by_list_from_directorate(db, division_id)

    # # Количество сотрудников по статусу всего департамента
    # def get_count_emp_by_all_status_from_directorate(self, db: Session, division_id: int):
    #     statuses = []
    #     for status in EmpStatusEnum:
    #         emp_count_by_all_status = (
    #             db.query(self.model)
    #             .filter(self.model.status == status, self.model.division_id == division_id)
    #             .count()
    #         )
    #         statuses.append(emp_count_by_all_status)
    #     return sum(statuses)

    # Количество сотрудников по статусу в управлении
    def get_count_emp_by_status_from_directorate(
        self, db: Session, status: str, division_id: int
    ):
        return (
            db.query(self.model)
            .filter(self.model.status == status, self.model.division_id == division_id)
            .count()
        )

    # Количество сотрудников которые в строю в управлении
    def get_count_emp_in_service_from_directorate(self, db: Session, division_id: int):
        return self.get_count_emp_by_list_from_directorate(
            db, division_id
        ) - self.get_count_emp_by_all_status_from_directorate(db, division_id)

    # Все сотрудники по статусу в управлении
    def get_emp_by_status_from_directorate(
        self, db: Session, status: str, division_id: int
    ):
        return (
            db.query(self.model)
            .filter(self.model.status == status, self.model.division_id == division_id)
            .all()
        )


employer_service = EmployerService(Employer)

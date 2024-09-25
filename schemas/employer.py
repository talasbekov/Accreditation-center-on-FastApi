from datetime import date
from typing import Optional

from schemas import Model


class EmployerBase(Model):
    surname: Optional[str]
    firstname: Optional[str]
    patronymic: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    status: Optional[str]
    record_id: Optional[str]


class EmployerCreate(EmployerBase):
    pass


class EmployerUpdate(EmployerBase):
    pass


class EmployerRead(EmployerBase, Model):
    id: int
    pass
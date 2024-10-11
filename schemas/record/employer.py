from typing import Optional

from schemas import Model
from schemas.record import DivisionRead, RankRead, StatusRead


class EmployerBase(Model):
    surname: Optional[str]
    firstname: Optional[str]
    patronymic: Optional[str]
    sort: Optional[int]
    status_id: Optional[int]
    rank_id: Optional[int]
    division_id: Optional[int]

    class Config:
        orm_mode = True


class EmployerCreate(EmployerBase):
    pass


class EmployerUpdate(EmployerBase):
    pass


class EmployerRead(EmployerBase, Model):
    id: int
    divisions: Optional[DivisionRead]

    class Config:
        orm_mode = True

class EmployerStateRead(Model):
    id: int
    surname: Optional[str]
    firstname: Optional[str]
    patronymic: Optional[str]
    sort: Optional[int]
    statuses: Optional[StatusRead]
    ranks: Optional[RankRead]

    class Config:
        orm_mode = True


class EmployerRandomCreate(Model):
    surname: Optional[str]
    firstname: Optional[str]
    patronymic: Optional[str]
    sort: Optional[int]
    rank_id: Optional[int]
    position_id: Optional[int]
    status_id: Optional[int]
    division_id: Optional[int]


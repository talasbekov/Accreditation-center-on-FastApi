from typing import Optional

from schemas import Model
from schemas.record import DepartmentRead


class StateBase(Model):
    department_id: Optional[int]
    management_id: Optional[int]
    division_id: Optional[int]
    position_id: Optional[int]
    employer_id: Optional[int]

    class Config:
        orm_mode = True


class StateCreate(StateBase):
    pass


class StateUpdate(StateBase):
    pass


class StateRead(StateBase, Model):
    id: int
    departments: Optional[DepartmentRead]

    class Config:
        orm_mode = True

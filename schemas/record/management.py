from typing import Optional

from schemas import NamedModel
from schemas.record import DivisionRead


class ManagementBase(NamedModel):
    department_id: Optional[int]

    class Config:
        orm_mode = True


class ManagementCreate(ManagementBase):
    pass


class ManagementUpdate(ManagementBase):
    pass


class ManagementRead(ManagementBase, NamedModel):
    id: int
    divisions: Optional[list[DivisionRead]]

    class Config:
        orm_mode = True

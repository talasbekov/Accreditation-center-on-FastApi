from typing import Optional

from schemas import NamedModel, Model
from schemas.record import DepartmentRead


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
    departments: Optional[DepartmentRead]

    class Config:
        orm_mode = True


class ManagementStateRead(Model):
    id: int
    name: Optional[str]

    class Config:
        orm_mode = True

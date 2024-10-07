from typing import Optional

from schemas import NamedModel
from schemas.record import ManagementRead


class DepartmentBase(NamedModel):
    name: Optional[str]


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(DepartmentBase):
    pass


class DepartmentRead(DepartmentBase, NamedModel):
    id: int
    managements: Optional[list[ManagementRead]]

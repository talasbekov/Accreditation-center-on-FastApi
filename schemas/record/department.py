from typing import Optional

from schemas import NamedModel, Model


class DepartmentBase(NamedModel):

    class Config:
        orm_mode = True


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(DepartmentBase):
    pass


class DepartmentRead(DepartmentBase, NamedModel):
    id: int

    class Config:
        orm_mode = True


class DepartmentStateRead(Model):
    id: int
    name: Optional[str]

    class Config:
        orm_mode = True

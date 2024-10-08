from typing import Optional
from schemas import NamedModel, Model
from schemas.record import ManagementRead


class DivisionBase(NamedModel):
    management_id: Optional[int]

    class Config:
        orm_mode = True


class DivisionCreate(DivisionBase):
    pass


class DivisionUpdate(DivisionBase):
    pass


class DivisionRead(DivisionBase, NamedModel):
    id: int
    managements: Optional[ManagementRead]

    class Config:
        orm_mode = True


class DivisionStateRead(Model):
    id: int
    name: Optional[str]

    class Config:
        orm_mode = True

from typing import Optional
from schemas import NamedModel
from schemas.record import EmployerRead


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
    employers: Optional[list[EmployerRead]]

    class Config:
        orm_mode = True

from typing import Optional
from schemas import NamedModel
from schemas.record import EmployerRead


class DivisionBase(NamedModel):
    name: Optional[str]
    management_id: Optional[str]


class DivisionCreate(DivisionBase):
    pass


class DivisionUpdate(DivisionBase):
    pass


class DivisionRead(DivisionBase, NamedModel):
    id: int
    employers: Optional[list[EmployerRead]]

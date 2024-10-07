from typing import Optional

from schemas import NamedModel
from schemas.record import DivisionRead


class ManagementBase(NamedModel):
    name: Optional[str]


class ManagementCreate(ManagementBase):
    pass


class ManagementUpdate(ManagementBase):
    pass


class ManagementRead(ManagementBase, NamedModel):
    id: int
    divisions: Optional[list[DivisionRead]]

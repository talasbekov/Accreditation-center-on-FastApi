from typing import Optional

from schemas import NamedModel


class PositionBase(NamedModel):
    category: Optional[str]


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionRead(PositionBase, NamedModel):
    id: int

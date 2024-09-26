from typing import Optional

from schemas import EmployerRead, Model


class RecordBase(Model):
    name: Optional[str]
    count_state: Optional[int]


class RecordCreate(RecordBase):
    pass


class RecordUpdate(RecordBase):
    pass


class RecordRead(RecordBase, Model):
    id: int
    employers: Optional[list[EmployerRead]]

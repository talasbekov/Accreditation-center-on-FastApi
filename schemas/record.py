from typing import Optional

from schemas import UserRead, Model


class RecordBase(Model):
    name: Optional[str]
    pass


class RecordCreate(RecordBase):
    pass


class RecordUpdate(RecordBase):
    pass


class RecordRead(RecordBase, Model):
    users: Optional[list[UserRead]]

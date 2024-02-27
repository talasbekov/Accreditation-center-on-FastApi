from typing import Optional
from schemas import ReadNamedModel, NamedModel


class SexBase(NamedModel):
    sex_code: Optional[str]


class SexCreate(SexBase):
    pass


class SexUpdate(SexBase):
    pass


class SexRead(SexBase, ReadNamedModel):
    pass

from typing import Optional
from schemas import ReadNamedModel


class SexBase(ReadNamedModel):
    sex_code: Optional[str]


class SexCreate(SexBase):
    pass


class SexUpdate(SexBase):
    pass


class SexRead(SexBase):
    pass

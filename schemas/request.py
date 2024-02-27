from typing import Optional

from schemas import ReadModel


# Схема для Operator
class RequestBase(ReadModel):
    user_id: Optional[str] = None
    patronymic: Optional[str] = None
    phone_number: Optional[str] = None
    workplace: Optional[str] = None
    is_accreditator: Optional[bool] = False


class RequestCreate(RequestBase):
    pass


class RequestUpdate(RequestBase):
    pass


class RequestRead(RequestBase, ReadModel):
    pass

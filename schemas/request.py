from typing import Optional

from schemas import Model, ReadModel


# Схема для Operator
class RequestBase(Model):
    name: Optional[str]
    event_id: Optional[str]
    created_by_id: Optional[str]
    status: Optional[str]


class RequestCreate(RequestBase):
    pass


class RequestUpdate(RequestBase):
    pass


class RequestRead(RequestBase, ReadModel):
    pass

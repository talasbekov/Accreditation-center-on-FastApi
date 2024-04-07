from typing import Optional, List

from schemas import Model, ReadModel
from .attendee import AttendeeRead


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
    attendees: Optional[List[AttendeeRead]]

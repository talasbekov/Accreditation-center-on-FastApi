from datetime import datetime
from typing import Optional, List
from pydantic import Field
from schemas import Model, ReadModel
from .attendee import AttendeeRead


def current_datetime_str():
    return datetime.now().strftime("%M%H%d%m%Y")


# Схема для Operator
class RequestBase(Model):
    name: Optional[str]
    event_id: Optional[str]
    created_by_id: Optional[str]
    status: Optional[str]


class RequestCreate(RequestBase):
    name: str = Field(default_factory=current_datetime_str)
    status: str = Field(default="Новое")


class RequestUpdate(RequestBase):
    pass


class RequestRead(RequestBase, ReadModel):
    attendees: Optional[List[AttendeeRead]]


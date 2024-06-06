from typing import Optional, List
from datetime import date
from schemas import ReadNamedModel, NamedModel, NamesModel
from .request import RequestRead
from .attendee import AttendeeRead
from .user import UserRead


# Схема для Event
class EventBase(NamedModel):
    event_code: Optional[str]
    date_start: Optional[date]
    date_end: Optional[date]
    city_id: Optional[str]
    lead: Optional[str]
    users: Optional[List[UserRead | None]] = []


class EventCreate(EventBase):
    is_for_gov: Optional[bool]
    pass


class EventUpdate(EventBase):
    is_for_gov: Optional[bool]


class EventRead(EventBase, ReadNamedModel):
    requests: Optional[List[RequestRead]]


class EventReadWithAttendies(EventBase):
    attendees: Optional[List[AttendeeRead]]


class GovEventRead(NamesModel):
    pass

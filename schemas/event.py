from typing import Optional
from datetime import date
from schemas import ReadNamedModel, NamedModel, UserRead, RequestRead, AttendeeRead
from typing import List


# Схема для Event
class EventBase(NamedModel):
    event_code: Optional[str]
    date_start: Optional[date]
    date_end: Optional[date]
    city_id: Optional[str]
    lead: Optional[str]
    user_id: Optional[List[UserRead]]


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventRead(EventBase, ReadNamedModel):
    requests: Optional[List[RequestRead]]


class EventReadWithAttendies(EventBase):
    attendees: Optional[List[AttendeeRead]]

from typing import Optional
from datetime import date
from schemas import ReadModel


# Схема для Event
class EventBase(ReadModel):
    name_kaz: Optional[str]
    name: Optional[str]
    name_eng: Optional[str]
    event_code: Optional[str]
    date_start: Optional[date]
    date_end: Optional[date]
    city_code: Optional[str]


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventRead(EventBase):
    pass

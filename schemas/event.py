from typing import Optional
from datetime import date
from schemas import ReadNamedModel, NamedModel


# Схема для Event
class EventBase(NamedModel):
    event_code: Optional[str]
    date_start: Optional[date]
    date_end: Optional[date]
    city_id: Optional[str]


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventRead(EventBase, ReadNamedModel):
    pass

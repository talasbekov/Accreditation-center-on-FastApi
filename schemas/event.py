from typing import Optional
from datetime import date
from schemas import ReadNamedModel, NamedModel
from .request import RequestRead
from typing import List


# Схема для Event
class EventBase(NamedModel):
    event_code: Optional[str]
    date_start: Optional[date]
    date_end: Optional[date]
    city_id: Optional[str]
    number: Optional[int]


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventRead(EventBase, ReadNamedModel):
    requests: Optional[List[RequestRead]]

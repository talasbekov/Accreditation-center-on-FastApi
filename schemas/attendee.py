from typing import Optional
from datetime import date
from schemas import ReadModel


class AttendeeBase(ReadModel):
    surname: str
    firstname: str
    patronymic: Optional[str]
    birth_date: Optional[date]
    post: Optional[str]
    country_id: Optional[str]
    doc_type_id: Optional[str]
    iin: Optional[str]


class AttendeeCreate(AttendeeBase):
    pass


class AttendeeUpdate(AttendeeBase):
    pass


class AttendeeRead(AttendeeBase, ReadModel):
    pass

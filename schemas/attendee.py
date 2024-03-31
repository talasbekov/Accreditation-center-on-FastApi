from typing import Optional
from datetime import date
from schemas import Model, ReadModel


class AttendeeBase(Model):
    surname: str
    firstname: str
    patronymic: Optional[str]
    birth_date: Optional[date]
    post: Optional[str]
    country_id: Optional[str]
    doc_type_id: Optional[str]
    sex_id: Optional[str]
    request_id: Optional[str]
    iin: Optional[str]
    doc_number: Optional[str]
    doc_begin: Optional[date]
    doc_end: Optional[date]
    doc_issue: Optional[str]
    photo: Optional[str]
    doc_scan: Optional[str]
    visit_object: Optional[str]
    transcription: Optional[str]


class AttendeeCreate(AttendeeBase):
    pass


class AttendeeUpdate(AttendeeBase):
    pass


class AttendeeRead(AttendeeBase, ReadModel):
    pass

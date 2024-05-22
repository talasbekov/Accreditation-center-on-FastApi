from typing import Optional
from datetime import date
from fastapi import UploadFile
from schemas import Model, ReadModel


class AttendeeBase(Model):
    surname: Optional[str]
    firstname: Optional[str]
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
    visit_object: Optional[str]
    transcription: Optional[str]
    photo: Optional[UploadFile]  # Field to store the file path of the photo
    doc_scan: Optional[UploadFile]  # Field to store the file path of the document scan


class AttendeeCreate(AttendeeBase):
    surname: str
    firstname: str
    patronymic: str
    birth_date: date
    post: str
    country_id: str
    doc_type_id: str
    sex_id: str
    iin: str
    doc_number: str
    doc_begin: date
    doc_end: date
    doc_issue: str
    visit_object: str
    transcription: str


class AttendeeUpdate(AttendeeBase):
    pass


class AttendeeRead(AttendeeBase, ReadModel):
    pass

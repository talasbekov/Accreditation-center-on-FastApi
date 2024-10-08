from typing import Optional
from datetime import date
from fastapi import UploadFile
from schemas import Model


class KazintechBase(Model):
    surname: Optional[str]
    firstname: Optional[str]
    patronymic: Optional[str]
    birth_date: Optional[date]
    post: Optional[str]
    country_id: Optional[int]
    doc_type_id: Optional[str]
    sex: Optional[bool]
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


class KazintechCreate(Model):
    surname: str
    firstname: str
    patronymic: str
    birth_date: date
    post: str
    country_id: int
    doc_type_id: int
    sex: bool
    iin: str
    doc_number: str
    doc_begin: date
    doc_end: date
    doc_issue: str
    visit_object: str
    transcription: str
    photo: str
    doc_scan: str


class KazintechUpdate(Model):
    surname: str
    firstname: str
    patronymic: str
    birth_date: date
    post: str
    country_id: int
    doc_type_id: int
    sex: bool
    iin: str
    doc_number: str
    doc_begin: date
    doc_end: date
    doc_issue: str
    visit_object: str
    transcription: str
    photo: str
    doc_scan: str

class KazintechRead(Model, KazintechBase):
    id: int

    class Config:
        orm_mode = True

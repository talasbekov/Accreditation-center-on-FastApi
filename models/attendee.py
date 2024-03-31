from sqlalchemy import String, Column, ForeignKey, Date
from sqlalchemy.orm import relationship

from .base import Model


class Attendee(Model):
    __tablename__ = "attendees"

    surname = Column(String(128))
    firstname = Column(String(128))
    patronymic = Column(String(128))
    birth_date = Column(Date, nullable=True)
    post = Column(String(1024))
    doc_series = Column(String(128))
    iin = Column(String(12), index=True)
    doc_number = Column(String(20))
    doc_begin = Column(Date, nullable=True)
    doc_end = Column(Date, nullable=True)
    doc_issue = Column(String(50))
    photo = Column(String, nullable=True)  # Путь к файлу вместо ImageField
    doc_scan = Column(String, nullable=True)  # Путь к файлу вместо ImageField
    visit_object = Column(String(1024))
    transcription = Column(String(128))

    sex_id = Column(String(), ForeignKey("sexes.id"), nullable=True)
    country_id = Column(String(), ForeignKey("countries.id"), nullable=True)
    request_id = Column(String(), ForeignKey("requests.id", ondelete="CASCADE"), nullable=True)
    doc_type_id = Column(String(), ForeignKey("document_types.id"), nullable=True)

    sexes = relationship("Sex", back_populates="attendees")
    countries = relationship("Country", back_populates="attendees")
    requests = relationship("Request", back_populates="attendees")
    document_types = relationship("DocumentType", back_populates="attendees")

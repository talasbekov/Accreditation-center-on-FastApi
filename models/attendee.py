from datetime import datetime

from sqlalchemy import String, Column, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship

from .base import Model


class Attendee(Model):
	__tablename__ = 'attendees'

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
	photo = Column(String)  # Путь к файлу вместо ImageField
	doc_scan = Column(String)  # Путь к файлу вместо ImageField
	date_add = Column(DateTime, default=datetime.utcnow)
	visit_objects = Column(String(1024))
	transcription = Column(String(128))
	date_end = Column(Date, nullable=True)
	stick_id = Column(String(20), default="")

	sex_id = Column(String(), ForeignKey('sexes.id'))
	country_id = Column(String(), ForeignKey('countries.id'))
	request_id = Column(String(), ForeignKey('requests.id'))
	doc_type_id = Column(String(), ForeignKey('document_types.id'))

	sex = relationship("Sex", back_populates="attendees")
	country = relationship("Country", back_populates="attendees")
	request = relationship("Request", back_populates="attendees")
	document_type = relationship("DocumentType", back_populates="attendees")

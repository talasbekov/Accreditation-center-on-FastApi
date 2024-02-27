from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from models import NamedModel
from models.association import user_event_association


class Event(NamedModel):
	__tablename__ = 'events'

	event_code = Column(String(20), unique=True, index=True)
	date_start = Column(Date)
	date_end = Column(Date)
	city = Column(String(), ForeignKey('cities.id'), nullable=True)

	cities = relationship("City", back_populates="events")
	requests = relationship("Request", back_populates="events")
	users = relationship("User", secondary=user_event_association, back_populates="events")

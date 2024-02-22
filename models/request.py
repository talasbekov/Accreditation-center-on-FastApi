from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .base import Model


class Request(Model):
	__tablename__ = 'requests'

	name = Column(String(128), index=True)
	event_id = Column(String, ForeignKey('events.id'))
	status = Column(String(20), nullable=True)
	date_created = Column(DateTime, default=datetime.utcnow)
	created_by_id = Column(String, ForeignKey('users.id'))
	registration_time = Column(DateTime, default=datetime.utcnow)

	event = relationship("Event", back_populates="requests")

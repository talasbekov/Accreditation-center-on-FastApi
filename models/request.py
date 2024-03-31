from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Model


class Request(Model):
    __tablename__ = "requests"

    name = Column(String(128), index=True)
    event_id = Column(String, ForeignKey("events.id", ondelete="CASCADE"))
    status = Column(String(20), nullable=True)
    created_by_id = Column(String, ForeignKey("users.id"))

    events = relationship("Event", back_populates="requests")
    users = relationship("User", back_populates="requests")
    attendees = relationship("Attendee", back_populates="requests")

from sqlalchemy import Column, String, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from models import NamedModel
from models.association import user_event_association


class Event(NamedModel):
    __tablename__ = "events"

    number = Column(Integer, autoincrement=True)
    event_code = Column(String(20), unique=True, index=True)
    date_start = Column(Date)
    date_end = Column(Date)
    city_id = Column(String(), ForeignKey("cities.id"), nullable=True)
    lead = Column(String(length=30))

    cities = relationship("City", back_populates="events")
    requests = relationship("Request", back_populates="events")
    users = relationship(
        "User", secondary=user_event_association, back_populates="events"
    )

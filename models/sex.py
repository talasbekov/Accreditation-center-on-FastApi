from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import NamedModel


# Определите ваши модели здесь
class Sex(NamedModel):
    __tablename__ = "sexes"

    sex_code = Column(String(20), unique=True)

    attendees = relationship("Attendee", back_populates="sexes")

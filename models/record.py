from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from models import Model


class Record(Model):
    __tablename__ = "records"

    name = Column(String(128))
    count_state = Column(Integer)
    employers = relationship("Employer", back_populates="records")

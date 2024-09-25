from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import Model


class Record(Model):
    __tablename__ = "records"

    name = Column(String(128))
    employers = relationship("Employer", back_populates="records")

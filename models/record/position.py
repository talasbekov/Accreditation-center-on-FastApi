from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import NamedModel


class Position(NamedModel):
    __tablename__ = "positions"

    category = Column(String(250))

    employers = relationship("Employer", back_populates="positions")
    states = relationship("State", back_populates="positions")

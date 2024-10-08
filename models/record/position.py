from sqlalchemy.orm import relationship

from models import NamedModel


class Position(NamedModel):
    __tablename__ = "positions"

    employers = relationship("Employer", back_populates="positions")
    states = relationship("State", back_populates="positions")

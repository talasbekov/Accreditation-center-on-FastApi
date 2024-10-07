from sqlalchemy import Column, String, ForeignKey, Date, Integer
from sqlalchemy.orm import relationship
from models import Model


class Employer(Model):
    __tablename__ = "employers"

    surname = Column(String(128))
    firstname = Column(String(128))
    patronymic = Column(String(128))
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    rank_id = Column(Integer, ForeignKey("ranks.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))
    division_id = Column(Integer, ForeignKey("divisions.id"))

    divisions = relationship("Division", back_populates="employers")
    states = relationship("State", back_populates="employers")
    positions = relationship("Position", back_populates="employers")
    ranks = relationship("Rank", back_populates="employers")

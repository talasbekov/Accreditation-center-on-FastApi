from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models import Model


class Employer(Model):
    __tablename__ = "employers"

    surname = Column(String(128))
    firstname = Column(String(128))
    patronymic = Column(String(128))
    sort = Column(Integer, nullable=False)
    photo = Column(String, nullable=True)

    rank_id = Column(Integer, ForeignKey("ranks.id"))
    division_id = Column(Integer, ForeignKey("divisions.id"), nullable=True)
    status_id = Column(Integer, ForeignKey("statuses.id"))

    divisions = relationship("Division", back_populates="employers")
    states = relationship("State", back_populates="employers")
    ranks = relationship("Rank", back_populates="employers")
    statuses = relationship("Status", back_populates="employers")

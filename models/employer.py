from sqlalchemy import Column, String, ForeignKey, Date, Integer, Enum as SqlEnum
from sqlalchemy.orm import relationship
from enum import Enum  # Используем чистое Enum для SQLAlchemy
from models import Model

# Определяем перечисление без наследования от str
class EmpStatusEnum(str, Enum):
    IN_SERVICE = "в строю"
    ON_LEAVE = "в отпуске"
    ON_SICK_LEAVE = "на больничном"
    BUSINESS_TRIP = "в командировке"
    SECONDED_IN = "прикомандирован"
    SECONDED_OUT = "откомандирован"
    ON_DUTY = "на дежурстве"
    AFTER_ON_DUTY = "после дежурства"
    AT_THE_COMPETITION = "на соревновании"


class Employer(Model):
    __tablename__ = "employers"

    surname = Column(String(128))
    firstname = Column(String(128))
    patronymic = Column(String(128))
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    # Используем SqlEnum для SQLAlchemy Enum
    status = Column(SqlEnum(EmpStatusEnum), default=EmpStatusEnum.IN_SERVICE, nullable=False)
    record_id = Column(Integer, ForeignKey("records.id"), nullable=True)

    records = relationship("Record", back_populates="employers")

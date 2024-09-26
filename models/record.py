from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from models import Model


class Record(Model):
    __tablename__ = "records"

    name = Column(String(128))
    count_state = Column(Integer)
    count_list = Column(Integer)
    count_on_leave = Column(Integer)
    count_on_sick_leave = Column(Integer)
    count_business_trip = Column(Integer)
    count_seconded_in = Column(Integer)
    count_seconded_out = Column(Integer)
    count_on_duty = Column(Integer)
    count_after_on_duty = Column(Integer)
    count_at_the_competition = Column(Integer)

    employers = relationship("Employer", back_populates="records")

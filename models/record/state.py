from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models import Model


class State(Model):
    __tablename__ = "states"

    department_id = Column(Integer, ForeignKey("departments.id"))
    management_id = Column(Integer, ForeignKey("managements.id"))
    division_id = Column(Integer, ForeignKey("divisions.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))
    employer_id = Column(Integer, ForeignKey("employers.id"), nullable=True)

    departments = relationship("Department", back_populates="states")
    managements = relationship("Management", back_populates="states")
    divisions = relationship("Division", back_populates="states")
    positions = relationship("Position", back_populates="states")
    employers = relationship("Employer", back_populates="states", lazy="joined")

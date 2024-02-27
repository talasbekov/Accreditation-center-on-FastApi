from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import NamedModel


# Определите ваши модели здесь
class City(NamedModel):
    __tablename__ = "cities"

    city_code = Column(String(20), unique=True)
    index = Column(String(20))

    events = relationship("Event", back_populates="cities")

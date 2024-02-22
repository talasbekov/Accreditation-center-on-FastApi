from sqlalchemy import Column, String
from models import NamedModel


# Определите ваши модели здесь
class City(NamedModel):
    __tablename__ = "cities"

    city_code = Column(String(20), unique=True)
    index = Column(String(20))

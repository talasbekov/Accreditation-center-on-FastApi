from sqlalchemy import Column, String, Boolean
from models import NamedModel


# Определите ваши модели здесь
class Country(NamedModel):
    __tablename__ = "countries"

    country_code = Column(String(20), unique=True)
    cis_flag = Column(Boolean, default=False)
    country_iso = Column(String(20))

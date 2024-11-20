from typing import Optional
from sqlalchemy.orm import Session
from models import Country  # Предполагается, что у вас есть модель Country в models.py
from schemas import (
    CountryCreate,
    CountryUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class CountryService(ServiceBase[Country, CountryCreate, CountryUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Country]:
        return db.query(Country).filter(Country.name == name).first()




country_service = CountryService(Country)

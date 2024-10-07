from typing import Optional
from sqlalchemy.orm import Session
from models.accr import City  # Предполагается, что у вас есть модель City в models.py
from schemas import (
    CityCreate,
    CityUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class CityService(ServiceBase[City, CityCreate, CityUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[City]:
        return db.query(City).filter(City.name == name).first()


city_service = CityService(City)

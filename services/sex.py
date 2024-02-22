from typing import Optional
from sqlalchemy.orm import Session
from models import Sex  # Предполагается, что у вас есть модель Sex в models.py
from schemas import SexCreate, SexUpdate  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class SexService(ServiceBase[Sex, SexCreate, SexUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Sex]:
        return db.query(Sex).filter(Sex.name == name).first()


sex_service = SexService(Sex)

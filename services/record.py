from typing import Optional
from sqlalchemy.orm import Session
from models import (
    Record,
)  # Предполагается, что у вас есть модель Record в models.py
from schemas import (
    RecordCreate,
    RecordUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class RecordService(ServiceBase[Record, RecordCreate, RecordUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Record]:
        return db.query(Record).filter(Record.name == name).first()


record_service = RecordService(Record)

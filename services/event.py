from typing import Optional
from sqlalchemy.orm import Session
from models import Event  # Предполагается, что у вас есть модель Event в models.py
from schemas import (
    EventCreate,
    EventUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class EventService(ServiceBase[Event, EventCreate, EventUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Event]:
        return db.query(Event).filter(Event.name == name).first()


event_service = EventService(Event)

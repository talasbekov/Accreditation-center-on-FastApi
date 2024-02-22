from typing import Optional
from sqlalchemy.orm import Session
from models import Attendee  # Предполагается, что у вас есть модель Attendee в models.py
from schemas import AttendeeCreate, AttendeeUpdate  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class AttendeeService(ServiceBase[Attendee, AttendeeCreate, AttendeeUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Attendee]:
        return db.query(Attendee).filter(Attendee.name == name).first()


attendee_service = AttendeeService(Attendee)

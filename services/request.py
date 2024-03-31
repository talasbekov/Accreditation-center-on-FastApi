from typing import Optional
from sqlalchemy.orm import Session
from models import Request  # Предполагается, что у вас есть модель Request в models.py
from schemas import (
    RequestCreate,
    RequestUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class RequestService(ServiceBase[Request, RequestCreate, RequestUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Request]:
        return db.query(Request).filter(Request.name == name).first()


request_service = RequestService(Request)

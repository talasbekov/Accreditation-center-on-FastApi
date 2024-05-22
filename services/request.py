from typing import Optional
from sqlalchemy.orm import Session
from models import Request  # Предполагается, что у вас есть модель Request в models.py
from schemas import (
    RequestCreate,
    RequestUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class RequestService(ServiceBase[Request, RequestCreate, RequestUpdate]):

    def get_by_id(self, db: Session, request_id: str):
        return db.query(self.model).filter(self.model.id == request_id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[Request]:
        return db.query(Request).filter(Request.name == name).first()

    def get_by_event_id(self, db: Session, event_id: str, skip: int, limit: int):
        return db.query(Request).filter(Request.event_id == event_id).offset(skip).limit(limit).all()

    # def get_all_att_by_req(self, db: Session, event_id: str):
    #     return db.query(Request).filter(Request.event_id == event_id).all()


request_service = RequestService(Request)

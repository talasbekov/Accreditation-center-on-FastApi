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

    # Количество сотрудников по штату всего департамента
    def get_count_emp_by_state(self):
        return 136

    # Количество сотрудников по штату управления
    def get_count_state(self, db: Session, record_id: int):
        rec = db.query(Record).filter(Record.id == record_id).first()

        if rec is None:
            return {"error": "Record not found"}

        count_vacant = rec.count_state - rec.count_list
        count_in_service = rec.count_list - (rec.count_on_leave + rec.count_on_sick_leave + rec.count_business_trip + rec.count_seconded_in + rec.count_seconded_out + rec.count_on_duty + rec.count_after_on_duty + rec.count_at_the_competition)
        return {
            "Количество сотрудников по штату в управлении": rec.count_state,
            "Количество сотрудников по списку в управлении": rec.count_list,
            "Количество вакантных мест в управлении": count_vacant,
            "Количество сотрудников которые в строю в управлении": count_in_service,
            "В отпуске": rec.count_on_leave,
            "На больничном": rec.count_on_sick_leave,
            "В командировке": rec.count_business_trip,
            "Прикомандирован": rec.count_seconded_in,
            "Откомандирован": rec.count_seconded_out,
            "На дежурстве": rec.count_on_duty,
            "После дежурства": rec.count_after_on_duty,
            "на соревнованиях": rec.count_at_the_competition
        }

record_service = RecordService(Record)

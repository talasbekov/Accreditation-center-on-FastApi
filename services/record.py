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
    def get_count_state(self, db: Session):
        records = db.query(self.model).all()

        if records is None:
            return {"error": "Records not found"}

        recs = []
        for r in records:
            rec = db.query(Record).filter(Record.id == r.id).first()

            if rec is None:
                return {"error": "Record not found"}

            # Приведение всех значений к int с заменой None на 0
            count_state = int(rec.count_state or 0)
            print(count_state)
            count_list = int(rec.count_list or 0)
            count_on_leave = int(rec.count_on_leave or 0)
            count_on_sick_leave = int(rec.count_on_sick_leave or 0)
            count_business_trip = int(rec.count_business_trip or 0)
            count_seconded_in = int(rec.count_seconded_in or 0)
            count_seconded_out = int(rec.count_seconded_out or 0)
            count_on_duty = int(rec.count_on_duty or 0)
            count_after_on_duty = int(rec.count_after_on_duty or 0)
            count_at_the_competition = int(rec.count_at_the_competition or 0)

            # Рассчитываем количество вакантных мест и сотрудников "в строю"
            count_vacant = count_state - count_list
            print(count_vacant, " vacant+++")
            count_in_service = count_list - (
                    count_on_leave
                    + count_on_sick_leave
                    + count_business_trip
                    + count_seconded_in
                    + count_seconded_out
                    + count_on_duty
                    + count_after_on_duty
                    + count_at_the_competition
            )
            print(count_in_service, " vstroiu+++")

            recs.append( {
                "id": rec.id,
                "name": rec.name,
                "count_state": count_state,
                "count_list": count_list,
                "count_vacant": count_vacant,
                "count_in_service": count_in_service,
                "count_on_leave": count_on_leave,
                "count_on_sick_leave": count_on_sick_leave,
                "count_business_trip": count_business_trip,
                "count_seconded_in": count_seconded_in,
                "count_seconded_out": count_seconded_out,
                "count_on_duty": count_on_duty,
                "count_after_on_duty": count_after_on_duty,
                "count_at_the_competition": count_at_the_competition,
            }
            )
        return recs


record_service = RecordService(Record)

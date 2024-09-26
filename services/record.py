import os
from typing import Optional
from sqlalchemy.orm import Session
from docx import Document

from io import BytesIO
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

    def create_word_report_from_template(self, recs: list):
        """
        Функция для создания отчета на основе шаблона Word с подстановкой данных
        """
        file_path = './test.docx'
        # Проверка на существование файла
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден. Пожалуйста, проверьте путь к файлу.")

        # Открываем заранее подготовленный шаблон Word
        doc = Document(file_path)

        # Проходим по каждому управлению и подставляем информацию
        for rec in recs:
            # Ищем плейсхолдеры по ключевым словам и заменяем их на реальные данные в таблицах
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if "{{ id }}" in cell.text:
                            cell.text = cell.text.replace("{{ id }}", str(rec.get('id', '')))
                        if "{{ name }}" in cell.text:
                            cell.text = cell.text.replace("{{ name }}", rec.get('name', ''))
                        if "{{ count_state }}" in cell.text:
                            cell.text = cell.text.replace("{{ count_state }}", str(rec.get('count_state', 0)))
                        if "{{ count_list }}" in cell.text:
                            cell.text = cell.text.replace("{{ count_list }}", str(rec.get('count_list', 0)))
                        if "{{ count_in_service }}" in cell.text:
                            cell.text = cell.text.replace("{{ count_in_service }}", str(rec.get('count_in_service', 0)))
                        if "{{ count_vacant }}" in cell.text:
                            cell.text = cell.text.replace("{{ count_vacant }}", str(rec.get('count_vacant', 0)))
                        if "{{ count_on_leave }}" in cell.text:
                            cell.text = cell.text.replace("{{ count_on_leave }}", str(rec.get('count_on_leave', 0)))
                        if "{{ count_business_trip }}" in cell.text:
                            cell.text = cell.text.replace("{{ count_business_trip }}",
                                                          str(rec.get('count_business_trip', 0)))
                        if "{{ count_on_sick_leave }}" in cell.text:
                            cell.text = cell.text.replace("{{ count_on_sick_leave }}",
                                                          str(rec.get('count_on_sick_leave', 0)))
                        if "{{ count_on_duty }}" in cell.text:
                            cell.text = cell.text.replace("{{ count_on_duty }}", str(rec.get('count_on_duty', 0)))
                        if "{{ count_after_on_duty }}" in cell.text:
                            cell.text = cell.text.replace("{{ count_after_on_duty }}",
                                                          str(rec.get('count_after_on_duty', 0)))
                        if "{{ count_at_the_competition }}" in cell.text:
                            cell.text = cell.text.replace("{{ count_at_the_competition }}",
                                                          str(rec.get('count_at_the_competition', 0)))
                        if "{{ count_seconded_in }}" in cell.text:
                            cell.text = cell.text.replace("{{ count_seconded_in }}",
                                                          str(rec.get('count_seconded_in', 0)))
                        if "{{ count_seconded_out }}" in cell.text:
                            cell.text = cell.text.replace("{{ count_seconded_out }}",
                                                          str(rec.get('count_seconded_out', 0)))


        # Сохраняем измененный документ во временный буфер
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        # Возвращаем документ для выгрузки
        return buffer


record_service = RecordService(Record)

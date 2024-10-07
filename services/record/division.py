# import os
from typing import Optional
from sqlalchemy.orm import Session
# from docx import Document
# from docx.shared import Pt
# from docx.enum.text import WD_ALIGN_PARAGRAPH
# from docx.oxml.ns import qn
# from docx.oxml import OxmlElement

# from io import BytesIO
from models import (
    Division,
)  # Предполагается, что у вас есть модель Division в models.py
from schemas import (
    DivisionCreate,
    DivisionUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class DivisionService(ServiceBase[Division, DivisionCreate, DivisionUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Division]:
        return db.query(Division).filter(Division.name == name).first()

    # Количество сотрудников по штату всего департамента
    def get_count_emp_by_state(self):
        return 136

    # # Количество сотрудников по штату управления
    # def get_count_state(self, db: Session):
    #     divisions = db.query(self.model).all()
    #
    #     if divisions is None:
    #         return {"error": "Divisions not found"}
    #
    #     # Инициализация переменных для хранения общих значений
    #     total_count_state = 0
    #     total_count_list = 0
    #     total_count_vacant = 0
    #     total_count_in_service = 0
    #     total_count_on_leave = 0
    #     total_count_on_sick_leave = 0
    #     total_count_business_trip = 0
    #     total_count_seconded_in = 0
    #     total_count_seconded_out = 0
    #     total_count_on_duty = 0
    #     total_count_after_on_duty = 0
    #     total_count_at_the_competition = 0
    #
    #     recs = []
    #     for d in divisions:
    #         rec = db.query(self.model).filter(self.model.id == d.id).first()
    #
    #         if rec is None:
    #             return {"error": "Division not found"}
    #
    #         # Приведение всех значений к int с заменой None на 0
    #         count_state = int(rec.count_state or 0)
    #         count_list = int(rec.count_list or 0)
    #         count_on_leave = int(rec.count_on_leave or 0)
    #         count_on_sick_leave = int(rec.count_on_sick_leave or 0)
    #         count_business_trip = int(rec.count_business_trip or 0)
    #         count_seconded_in = int(rec.count_seconded_in or 0)
    #         count_seconded_out = int(rec.count_seconded_out or 0)
    #         count_on_duty = int(rec.count_on_duty or 0)
    #         count_after_on_duty = int(rec.count_after_on_duty or 0)
    #         count_at_the_competition = int(rec.count_at_the_competition or 0)
    #
    #         # Рассчитываем количество вакантных мест и сотрудников "в строю"
    #         count_vacant = count_state - count_list
    #         count_in_service = count_list - (
    #                 count_on_leave
    #                 + count_on_sick_leave
    #                 + count_business_trip
    #                 + count_seconded_in
    #                 + count_seconded_out
    #                 + count_on_duty
    #                 + count_after_on_duty
    #                 + count_at_the_competition
    #         )
    #
    #         # Добавляем значения в общий счет
    #         total_count_state += count_state
    #         total_count_list += count_list
    #         total_count_vacant += count_vacant
    #         total_count_in_service += count_in_service
    #         total_count_on_leave += count_on_leave
    #         total_count_on_sick_leave += count_on_sick_leave
    #         total_count_business_trip += count_business_trip
    #         total_count_seconded_in += count_seconded_in
    #         total_count_seconded_out += count_seconded_out
    #         total_count_on_duty += count_on_duty
    #         total_count_after_on_duty += count_after_on_duty
    #         total_count_at_the_competition += count_at_the_competition
    #
    #         recs.append({
    #             "id": rec.id,
    #             "name": rec.name,
    #             "count_state": count_state,
    #             "count_list": count_list,
    #             "count_vacant": count_vacant,
    #             "count_in_service": count_in_service,
    #             "count_on_leave": count_on_leave,
    #             "count_on_sick_leave": count_on_sick_leave,
    #             "count_business_trip": count_business_trip,
    #             "count_seconded_in": count_seconded_in,
    #             "count_seconded_out": count_seconded_out,
    #             "count_on_duty": count_on_duty,
    #             "count_after_on_duty": count_after_on_duty,
    #             "count_at_the_competition": count_at_the_competition,
    #         })
    #
    #     # Добавляем общий итог в конец списка
    #     recs.append({
    #         "id": 8,
    #         "name": "Всего",
    #         "count_state": total_count_state,
    #         "count_list": total_count_list,
    #         "count_vacant": total_count_vacant,
    #         "count_in_service": total_count_in_service,
    #         "count_on_leave": total_count_on_leave,
    #         "count_on_sick_leave": total_count_on_sick_leave,
    #         "count_business_trip": total_count_business_trip,
    #         "count_seconded_in": total_count_seconded_in,
    #         "count_seconded_out": total_count_seconded_out,
    #         "count_on_duty": total_count_on_duty,
    #         "count_after_on_duty": total_count_after_on_duty,
    #         "count_at_the_competition": total_count_at_the_competition,
    #     })
    #
    #     return recs
    #
    # def create_word_report_from_template(self, recs: list):
    #     """
    #     Функция для создания отчета на основе шаблона Word с подстановкой данных
    #     """
    #     file_path = './test.docx'
    #     if not os.path.exists(file_path):
    #         raise FileNotFoundError(f"Файл {file_path} не найден. Пожалуйста, проверьте путь к файлу.")
    #
    #     doc = Document(file_path)
    #
    #     for table in doc.tables:
    #         row_idx = 4  # Начинаем с третьей строки
    #
    #         for rec_idx, rec in enumerate(recs, start=1):  # Здесь rec_idx начинает с 1
    #             row = table.rows[row_idx]
    #
    #             # Пример заполнения ячеек и применения форматирования
    #             for cell_idx, value in enumerate([
    #                 str(rec_idx),
    #                 rec.get('name', ''),
    #                 str(rec.get('count_state', 0)),
    #                 str(rec.get('count_list', 0)),
    #                 str(rec.get('count_in_service', 0)),
    #                 str(rec.get('count_vacant', 0)),
    #                 str(rec.get('count_on_leave', 0)),
    #                 str(rec.get('count_business_trip', 0)),
    #                 str(rec.get('count_on_sick_leave', 0)),
    #                 str(rec.get('count_on_duty', 0)),
    #                 str(rec.get('count_after_on_duty', 0)),
    #                 str(rec.get('count_at_the_competition', 0)),
    #                 str(rec.get('count_seconded_in', 0)),
    #                 str(rec.get('count_seconded_out', 0))
    #             ]):
    #                 cell = row.cells[cell_idx]
    #                 cell.text = value
    #
    #                 # Применение выравнивания по центру (горизонтально и вертикально)
    #                 paragraph = cell.paragraphs[0]
    #                 paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER  # Горизонтальное выравнивание
    #
    #                 # Применение стиля к тексту
    #                 run = paragraph.runs[0]
    #
    #                 # Применение жирного шрифта для rec_idx и name
    #                 if cell_idx == 0 or cell_idx == 1:  # rec_idx и name
    #                     run.bold = True
    #
    #                 run.font.size = Pt(12)  # Размер шрифта
    #                 run.font.name = 'Times New Roman'  # Имя шрифта
    #
    #                 # Применение вертикального выравнивания
    #                 tc = cell._element
    #                 tcPr = tc.get_or_add_tcPr()
    #                 tcVAlign = OxmlElement('w:vAlign')
    #                 tcVAlign.set(qn('w:val'), 'bottom')
    #                 tcPr.append(tcVAlign)
    #
    #             row_idx += 1
    #
    #     buffer = BytesIO()
    #     doc.save(buffer)
    #     buffer.seek(0)
    #
    #     return buffer


division_service = DivisionService(Division)

import base64
import io
from datetime import datetime
from pathlib import Path
from typing import Optional, Type, Union, Dict, Any

from fastapi import UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from PIL import Image
from io import BytesIO

import aiofiles
import hashlib
import requests
from sqlalchemy.orm import Session

from models import Attendee, Request
from schemas import AttendeeCreate, AttendeeUpdate
from services.base import ServiceBase
from core.config import configs


class AttendeeService(ServiceBase[Attendee, AttendeeCreate, AttendeeUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Attendee]:
        return db.query(Attendee).filter(Attendee.name == name).first()

    def get_attendees_by_event_id(
        self, db: Session, event_id: str, skip: int, limit: int
    ):
        requests = (
            db.query(Request)
            .filter(Request.event_id == event_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        attendees = []
        for req in requests:
            for attendee in req.attendees:
                attendees.append(attendee)
        print(attendees)
        return attendees

    async def get_by_request(self, db: Session, req_id: str) -> Optional[Attendee]:
        return db.query(self.model).filter(self.model.request_id == req_id).first()

    async def upload_photo(
        self, db: Session, attendee_id: str, photo: UploadFile
    ) -> Type[Attendee]:
        attendee = db.query(Attendee).filter(
            Attendee.id == attendee_id).first()
        if not attendee.requests:
            event_number = "default"
        else:
            event_number = attendee.requests.events.id

        file_location = Path(
            f"media/event_{event_number}/attendee_photos/{attendee_id}.png"
        )
        file_location.parent.mkdir(
            parents=True, exist_ok=True
        )  # Create directories if they do not exist

        # Read the file contents and save it as an image using PIL
        file_contents = await photo.read()
        image = Image.open(BytesIO(file_contents))
        image.save(file_location)

        photo_location = Path(f"event_{event_number}/attendee_photos/{attendee_id}.png")
        attendee.photo = str(photo_location)
        db.commit()
        db.refresh(attendee)

        return attendee

    async def upload_doc_scan(
        self, db: Session, attendee_id: str, doc_scan: UploadFile
    ) -> Type[Attendee]:
        attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()

        if not attendee.requests:
            event_number = "default"
        else:
            event_number = attendee.requests.events.id

        file_location = Path(
            f"media/event_{event_number}/attendee_documents/{doc_scan.filename}"
        )
        file_location.parent.mkdir(
            parents=True, exist_ok=True
        )  # Создаем директории, если они не существуют

        async with aiofiles.open(file_location, "wb") as file_object:
            # Assuming 'photo.file' supports async read
            file_contents = doc_scan.file.read()
            await file_object.write(file_contents)

        doc_scan_location = Path(
            f"event_{event_number}/attendee_documents/{doc_scan.filename}"
        )
        attendee.doc_scan = str(doc_scan_location)
        db.commit()
        db.refresh(attendee)

        return attendee

    async def upload_photo_base64(
        self, db: Session, attendee_id: str, photo: Image.Image
    ) -> Type[Attendee]:
        attendee = db.query(Attendee).filter(
            Attendee.id == attendee_id).first()
        if not attendee.requests:
            event_number = "default"
        else:
            event_number = attendee.requests.events.id

        file_location = Path(
            f"media/event_{event_number}/attendee_photos/{attendee_id}.png"
        )
        file_location.parent.mkdir(
            parents=True, exist_ok=True
        )  # Create directories if they do not exist

        # Save the PIL image
        photo.save(file_location)

        photo_location = Path(f"event_{event_number}/attendee_photos/{attendee_id}.png")
        attendee.photo = str(photo_location)
        db.commit()
        db.refresh(attendee)

        return attendee

    async def upload_doc_scan_base64(
        self, db: Session, attendee_id: str, doc_scan: Image.Image
    ) -> Type[Attendee]:
        attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()

        if not attendee.requests:
            event_number = "default"
        else:
            event_number = attendee.requests.events.id

        file_location = Path(
            f"media/event_{event_number}/attendee_documents/{attendee_id}.png"
        )
        file_location.parent.mkdir(
            parents=True, exist_ok=True
        )  # Create directories if they do not exist

        # Save the PIL image
        doc_scan.save(file_location)

        doc_scan_location = Path(
            f"event_{event_number}/attendee_documents/{attendee_id}.png"
        )
        attendee.doc_scan = str(doc_scan_location)
        db.commit()
        db.refresh(attendee)

        return attendee

    def create(
        self, db: Session, obj_in: Union[AttendeeCreate, Dict[str, Any]], **kwargs
    ) -> Attendee:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["birth_date"] = datetime.strptime(
            obj_in_data["birth_date"], "%Y-%m-%d"
        )
        obj_in_data["doc_begin"] = datetime.strptime(
            obj_in_data["doc_begin"], "%Y-%m-%d"
        )
        obj_in_data["doc_end"] = datetime.strptime(obj_in_data["doc_end"], "%Y-%m-%d")
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj

    # Создаем Токен для интеграции с Аккредитационным центром Игр Кочевников
    async def _get_token(self):
        password = configs.SERVICE_PASSWORD
        date = datetime.now().strftime("%d.%m.%y")
        combined_string = f"{password}{date}"
        md5_hash = hashlib.md5(combined_string.encode()).hexdigest()
        print(md5_hash, "hash ACCR")
        return md5_hash

    # Функция для сохранения Base64 фото
    def save_base64_image(self, base64_string, image_path):
        try:
            # Декодирование Base64
            image_data = base64.b64decode(base64_string)
            image = Image.open(io.BytesIO(image_data))
            # Сохранение изображения
            image.save(image_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Cannot decode or save image: {str(e)}")

    # Загрузка список всех участников с сервера АЦ Игр Кочевников
    async def reload(self, db: Session):
        token = await self._get_token()
        url_pages = f"https://accreditation.wng.kz:8444/api/wng/sgo/visitors/pages?token={token}"
        count = requests.get(url_pages).text
        count = int(float(count))

        for i in range(1, count + 1):
            url = f"https://accreditation.wng.kz:8444/api/wng/sgo/visitors?token={token}&page={i}"
            response = requests.get(url)
            data = response.json()

            for item in data:
                # Преобразование поля sex в числовое значение
                sex_id = True if item["sex"] == "М" else False if item["sex"] == "Ж" else None

                # Проверка наличия фото
                if item.get("photo"):
                    # Генерация пути для сохранения изображения
                    photo_filename = f"{item['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                    photo_path = Path(f"media/event_1/attendee_photos/{photo_filename}")
                    photo_path.parent.mkdir(parents=True, exist_ok=True)
                    photo_path_for_save = Path(f"event_1/attendee_photos/{photo_filename}")
                    # Сохранение изображения
                    self.save_base64_image(item["photo"], photo_path)

                # Создание записи для базы данных
                item_data = {
                    "surname": item["surname"],
                    "firstname": item["firstname"],
                    "patronymic": item["patronymic"],
                    "birth_date": datetime.strptime(item["birthDate"], "%d.%m.%Y").date() if item[
                        "birthDate"] else None,
                    "post": item["post"],
                    "doc_series": item["docSeries"],
                    "iin": item["iin"],
                    "doc_number": str(item["docNumber"]),
                    "doc_begin": datetime.strptime(item["docBegin"], "%Y-%m-%d").date() if item["docBegin"] else None,
                    "doc_end": datetime.strptime(item["docEnd"], "%Y-%m-%d").date() if item["docEnd"] else None,
                    "doc_issue": item["docIssue"],
                    "photo": str(photo_path_for_save) if item.get("photo") else "",  # Сохраняем путь к фото
                    "doc_scan": "",
                    "visit_object": item["visitObjects"],
                    "transcription": item["transcription"],
                    "sex": sex_id,
                    "country_id": 1,  # Можно изменить в зависимости от значений
                    "request_id": 1,
                    "doc_type_id": 1,
                    "id": int(item["id"]),
                }

                # Проверка на существование записи
                attendee = db.query(Attendee).filter(Attendee.id == str(item["id"])).first()

                if not attendee:
                    # Создание новой записи
                    attendee = Attendee(**item_data)
                    db.add(attendee)
                else:
                    # Обновление существующей записи
                    for key, value in item_data.items():
                        setattr(attendee, key, value)
                    db.commit()
            db.commit()
        return count


    # async def reload(self, db: Session):
    #     token = await self._get_token()
    #     url_pages = f"https://accreditation.wng.kz:8444/api/wng/sgo/visitors/pages?token={token}"
    #     count = requests.get(url_pages).text
    #     count = int(float(count))
    #
    #     for i in range(1, count + 1):
    #         url = f"https://accreditation.wng.kz:8444/api/wng/sgo/visitors?token={token}&page={i}"
    #         response = requests.get(url)
    #         data = response.json()
    #
    #         for item in data:
    #             # Проверяем значение пола и устанавливаем соответствующее значение в поле sex_id
    #             sex_id = 1 if item["sex"] == "М" else 2 if item["sex"] == "Ж" else None
    #
    #             # Correct base64 padding and validate
    #             photo_data_str = correct_base64_padding(item.photo)
    #             doc_scan_data_str = correct_base64_padding(item.doc_scan)
    #             print(photo_data_str)
    #
    #             if not is_valid_base64(photo_data_str):
    #                 raise BadRequestException(detail="Invalid base64 data for photo")
    #             if not is_valid_base64(doc_scan_data_str):
    #                 raise BadRequestException(
    #                     detail="Invalid base64 data for document scan"
    #                 )
    #
    #             try:
    #                 # Decode base64 photo and document scan
    #                 photo_data = base64.b64decode(photo_data_str)
    #                 doc_scan_data = base64.b64decode(doc_scan_data_str)
    #             except base64.binascii.Error:
    #                 raise BadRequestException(detail="Error decoding base64 data")
    #
    #             try:
    #                 # Convert the decoded data to PIL images
    #                 photo_image = Image.open(io.BytesIO(photo_data))
    #                 doc_scan_image = Image.open(io.BytesIO(doc_scan_data))
    #             except IOError as e:
    #                 raise BadRequestException(detail=f"Cannot identify image file: {e}")
    #
    #             # Save the images to appropriate locations or services
    #             await attendee_service.upload_photo_base64(db, item.id, photo_image)
    #             await attendee_service.upload_doc_scan_base64(db, item.id, doc_scan_image)
    #
    #             for key, value in item.items():
    #                 if isinstance(value, int):
    #                     item[key] = str(value)
    #
    #             item = {
    #                 "surname": item["surname"],
    #                 "firstname": item["firstname"],
    #                 "patronymic": item["patronymic"],
    #                 "birth_date": datetime.strptime(item["birthDate"], "%d.%m.%Y").date() if item["birthDate"] else None,
    #                 "post": item["post"],
    #                 "doc_series": item["docSeries"],
    #                 "iin": item["iin"],
    #                 "doc_number": str(item["docNumber"]),
    #                 "doc_begin": datetime.strptime(item["docBegin"], "%Y-%m-%d").date() if item["docBegin"] else None,
    #                 "doc_end": datetime.strptime(item["docEnd"], "%Y-%m-%d").date() if item["docEnd"] else None,
    #                 "doc_issue": item["docIssue"],
    #                 "photo": "",  # Assuming no photo path provided
    #                 "doc_scan": item["docScan"],
    #                 "visit_object": item["visitObjects"],
    #                 "transcription": item["transcription"],
    #                 "sex_id": sex_id,
    #                 "country_id": 1,
    #                 "request_id": 1,
    #                 "doc_type_id": 1,
    #                 "id": str(item["id"]),
    #             }
    #             attendee = db.query(Attendee).filter(Attendee.id == str(item["id"])).first()
    #
    #             if not attendee:
    #                 attendee = Attendee(**item)
    #                 db.add(attendee)
    #             else:
    #                 for key, value in item.items():
    #                     setattr(attendee, key, value)
    #                 db.commit()
    #     db.commit()
    #     return count

attendee_service = AttendeeService(Attendee)

import base64
import io
import json

from datetime import datetime
from pathlib import Path
from typing import Optional, Type, Union, Dict, Any

import aiohttp
from fastapi import UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from PIL import Image
from io import BytesIO
import fitz  # PyMuPDF

import aiofiles
import hashlib
import requests
from sqlalchemy.orm import Session

from models import Attendee, Request
from schemas import AttendeeCreate, AttendeeUpdate
from services.base import ServiceBase
from core.config import configs
from utils import correct_base64_padding, is_valid_base64


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
    async def save_base64_image(self, base64_string, image_path: Path, image_path_for_save: Path):
        try:
            base64_string = correct_base64_padding(base64_string)
            if not is_valid_base64(base64_string):
                raise ValueError("Invalid Base64 string")

            image_data = base64.b64decode(base64_string)
            image = Image.open(io.BytesIO(image_data))

            image.save(image_path)
            return str(image_path_for_save)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Cannot decode or save image: {str(e)}")

    # Функция для сохранения PDF как JPG
    async def save_pdf_as_jpg(self, base64_string: str, image_path: Path, image_path_for_save: Path):
        try:
            if not base64_string:
                print("Base64 строка для PDF отсутствует или пуста")
                return None

            pdf_data = base64.b64decode(base64_string)
            pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

            if not pdf_document.page_count:
                print("Предоставленный PDF пуст.")
                return None

            image_filenames = []
            for i in range(pdf_document.page_count):
                page = pdf_document.load_page(i)
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes()))

                image_filename = image_path.with_name(f"{image_path_for_save.stem}_{i + 1}.jpg")
                async with aiofiles.open(image_filename, "wb") as f:
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG')
                    await f.write(img_byte_arr.getvalue())

                # Преобразуем путь, удаляя 'media/' из начала
                image_filenames.append(str(image_filename)[len('media/'):])

            # Если список содержит только один элемент, возвращаем строку
            if len(image_filenames) == 1:
                return image_filenames[0]

            return image_filenames

        except Exception as e:
            print(f"Не удалось декодировать PDF или конвертировать в JPG: {str(e)}")
            return None

    # Загрузка списка всех участников с сервера АЦ Игр Кочевников
    async def reload_doc_scan(self, extern_id: str, doc_name: str, token: str):
        url = f"https://accreditation.wng.kz:8444/api/wng/sgo/visitors/doc?externId={extern_id}&docName={doc_name}&token={token}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content_type = response.headers.get('Content-Type')
                    print(f"Content-Type: {content_type}")

                    base64_data = await response.text()
                    if not base64_data.strip():
                        raise ValueError(f"Пустой ответ для документа {doc_name}")

                    if "application/json" in content_type:
                        doc_filename = f"{extern_id}_{doc_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                        doc_path = Path(f"media/event_1/attendee_documents/{doc_filename}")
                        doc_path.parent.mkdir(parents=True, exist_ok=True)
                        doc_path_for_save = Path(f"event_1/attendee_documents/{doc_filename}")
                        saved_paths = await self.save_pdf_as_jpg(base64_data, doc_path, doc_path_for_save)
                        return saved_paths

                    if "application/pdf" in content_type:
                        doc_filename = f"{extern_id}_{doc_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                        doc_path = Path(f"media/event_1/attendee_documents/{doc_filename}")
                        doc_path.parent.mkdir(parents=True, exist_ok=True)
                        # doc_path_for_save = Path(f"event_1/attendee_documents/{doc_filename}")
                        saved_paths = await self.save_pdf_as_jpg(base64_data, doc_path)
                        return saved_paths

                    elif "image/gif" in content_type or "image/jpeg" in content_type or "image/png" in content_type:
                        image_filename = f"{extern_id}_{doc_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                        image_path = Path(f"media/event_1/attendee_documents/{image_filename}")
                        image_path.parent.mkdir(parents=True, exist_ok=True)
                        # image_path_for_save = Path(f"event_1/attendee_documents/{image_filename}")
                        saved_image_path = await self.save_pdf_as_jpg(base64_data, image_path)
                        return saved_image_path

                    else:
                        raise ValueError(f"Некорректный тип содержимого для документа {doc_name}: {content_type}")
                else:
                    raise ValueError(f"Не удалось получить документ {doc_name}. Статус: {response.status}")

    # Основная функция обработки данных
    async def reload(self, db: Session):
        token = await self._get_token()
        url_pages = f"https://accreditation.wng.kz:8444/api/wng/sgo/visitors/pages?token={token}"
        count = int(float(requests.get(url_pages).text))

        for i in range(1, count + 1):
            url = f"https://accreditation.wng.kz:8444/api/wng/sgo/visitors?token={token}&page={i}"
            response = requests.get(url)
            data = response.json()

            for item in data:
                try:
                    sex_id = True if item["sex"] == "М" else False if item["sex"] == "Ж" else None
                    country_id = 1 if item["country"] == "Казахстан" else 2 if  item["country"] == "Узбекистан" else 1
                    doc_id = 1 if item["docType"] == "Документ, удостоверяющий личность " else 2 if item["docType"] == "Заграничный паспорт" else None

                    photo_paths = ""
                    if item.get("photo"):
                        photo_filename = f"{item['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                        photo_path = Path(f"media/event_1/attendee_photos/{photo_filename}")
                        photo_path.parent.mkdir(parents=True, exist_ok=True)
                        photo_path_for_save = Path(f"event_1/attendee_photos/{photo_filename}")
                        photo_paths = await self.save_base64_image(item["photo"], photo_path, photo_path_for_save)

                    doc_scan_files = item.get("docScan", "").split(", ")
                    doc_scans = []
                    extern_id = str(item["id"])[5:]

                    for doc_name in doc_scan_files:
                        try:
                            doc_scan_base64 = await self.reload_doc_scan(extern_id, doc_name, token)
                            if doc_scan_base64:
                                doc_scans.append(doc_scan_base64)
                        except ValueError as e:
                            print(f"Ошибка при получении документа {doc_name}: {str(e)}")

                    # Преобразование doc_scan: если одна запись, сохраняем как строку, иначе как список JSON
                    if len(doc_scans) == 1:
                        doc_scan_json = doc_scans[0]  # Сохраняем одну запись как строку
                    elif doc_scans:
                        doc_scan_json = json.dumps(doc_scans)  # Сохраняем список как JSON
                    else:
                        doc_scan_json = None  # Если пусто, присваиваем None

                    item_data = {
                        "surname": item["surname"],
                        "firstname": item["firstname"],
                        "patronymic": item["patronymic"],
                        "birth_date": datetime.strptime(item["birthDate"], "%d.%m.%Y").date() if item[
                            "birthDate"] else "1992-12-12",
                        "post": item["company"],
                        "doc_series": item["docSeries"][:12] if item["docSeries"] else None,
                        "iin": item["iin"][:12] if item["iin"] else None,
                        "doc_number": str(item["docNumber"]),
                        "doc_begin": "2023-12-12",
                        "doc_end": "2033-12-12",
                        "doc_issue": item["docIssue"],
                        "photo": photo_paths if item.get("photo") else "",
                        "doc_scan": doc_scan_json,
                        "visit_object": item["visitObjects"],
                        "transcription": item["transcription"],
                        "sex": sex_id,
                        "country_id": country_id,
                        "request_id": 1,
                        "doc_type_id": doc_id,
                        "id": int(item["id"]),
                    }

                    try:
                        # Поиск существующего участника
                        attendee = db.query(Attendee).filter(Attendee.id == item["id"]).first()

                        if not attendee:
                            # Создание новой записи
                            attendee = Attendee(**item_data)
                            db.add(attendee)
                        else:
                            # Обновление существующей записи
                            for key, value in item_data.items():
                                setattr(attendee, key, value)

                        # Применение изменений для текущей записи
                        db.commit()

                    except Exception as e:
                        print(f"Ошибка при сохранении записи {item['id']}: {str(e)}")
                        db.rollback()  # Откат транзакции для конкретной записи

                except Exception as e:
                    # Логирование ошибки для текущего участника
                    print(f"Ошибка при обработке записи {item['id']}: {str(e)}")

        return count


attendee_service = AttendeeService(Attendee)

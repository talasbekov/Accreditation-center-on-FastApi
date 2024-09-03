from pathlib import Path

from fastapi import UploadFile
from typing import Optional, Type
from sqlalchemy.orm import Session

# from exceptions import NotFoundException
from models import Attendee
from schemas import AttendeeCreate, AttendeeUpdate
from services.base import ServiceBase
import hashlib
import requests
from core.config import configs
import aiofiles
from datetime import datetime


class AttendeeService(ServiceBase[Attendee, AttendeeCreate, AttendeeUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Attendee]:
        return db.query(Attendee).filter(Attendee.name == name).first()

    async def upload_photo(self, db: Session, attendee_id: str, photo: UploadFile) -> Type[Attendee]:
        attendee = db.query(Attendee).filter(
            Attendee.id == attendee_id).first()
        events = attendee.requests.events.id
        print(events)
        if not attendee.requests:
            event_number = 'default'
        else:
            event_number = attendee.requests.events.id

        print(photo.filename)
        # for req in attendee.requests:
        #     print(req)
        file_location = Path(
            f"media/event_{event_number}/attendee_photos/{photo.filename}")
        # Создаем директории, если они не существуют
        file_location.parent.mkdir(parents=True, exist_ok=True)

        # with photo.file as file_like:
        #     file_contents = file_like.read()  # This is now a blocking call
        #     with open(file_location, "wb") as file_object:
        #         file_object.write(file_contents)

        async with aiofiles.open(file_location, "wb") as file_object:
            # Assuming 'photo.file' supports async read
            file_contents = photo.file.read()
            await file_object.write(file_contents)

        attendee.photo = str(file_location)
        db.commit()
        db.refresh(attendee)

        return attendee

    async def upload_photo_scan(self, db: Session, attendee_id: str, photo: UploadFile) -> Type[Attendee]:
        attendee = db.query(Attendee).filter(
            Attendee.id == attendee_id).first()
        events = attendee.requests.events.id
        print(events)
        if not attendee.requests:
            event_number = 'default'
        else:
            event_number = attendee.requests.events.id

        print(photo.filename)
        # for req in attendee.requests:
        #     print(req)
        file_location = Path(
            f"media/event_{event_number}/attendee_documents/{photo.filename}")
        # Создаем директории, если они не существуют
        file_location.parent.mkdir(parents=True, exist_ok=True)

        # with photo.file as file_like:
        #     file_contents = file_like.read()  # This is now a blocking call
        #     with open(file_location, "wb") as file_object:
        #         file_object.write(file_contents)

        async with aiofiles.open(file_location, "wb") as file_object:
            # Assuming 'photo.file' supports async read
            file_contents = photo.file.read()
            await file_object.write(file_contents)

        attendee.doc_scan = str(file_location)
        db.commit()
        db.refresh(attendee)

        return attendee

    async def _get_token(self):
        password = configs.SERVICE_PASSWORD
        date = datetime.now().strftime("%d.%m.%y")
        combined_string = f"{password}{date}"
        md5_hash = hashlib.md5(combined_string.encode()).hexdigest()
        return md5_hash

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
                for key, value in item.items():
                    if isinstance(value, int):
                        item[key] = str(value)
                item = {
                    "surname": item["surname"],
                    "firstname": item["firstname"],
                    "patronymic": item["patronymic"],
                    "birth_date": datetime.strptime(item["birthDate"], "%d.%m.%Y").date() if item["birthDate"] else None,
                    "post": item["post"],
                    "doc_series": item["docSeries"],
                    "iin": item["iin"],
                    "doc_number": str(item["docNumber"]),
                    "doc_begin": datetime.strptime(item["docBegin"], "%Y-%m-%d").date() if item["docBegin"] else None,
                    "doc_end": datetime.strptime(item["docEnd"], "%Y-%m-%d").date() if item["docEnd"] else None,
                    "doc_issue": item["docIssue"],
                    "photo": "",  # Assuming no photo path provided
                    "doc_scan": item["docScan"],
                    "visit_object": item["visitObjects"],
                    "transcription": item["transcription"],
                    "sex_id": item["sexId"],
                    "country_id": item["countryId"],
                    "request_id": item["request"],
                    "doc_type_id": item["docTypeId"],
                    "created_at": item["dateAdd"],
                    "id": str(item["id"]),
                }
                attendee = db.query(Attendee).filter(Attendee.id == str(item["id"])).first()
                if not attendee:
                    attendee = Attendee(**item)
                    db.add(attendee)
                else:
                    for key, value in item.items():
                        setattr(attendee, key, value)
                    db.commit()
        db.commit()
        return count

attendee_service = AttendeeService(Attendee)

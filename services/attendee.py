from datetime import datetime
from pathlib import Path
from typing import Optional, Type, Union, Dict, Any

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

# from exceptions import NotFoundException
from models import Attendee
from schemas import AttendeeCreate, AttendeeUpdate
from services.base import ServiceBase

import aiofiles


class AttendeeService(ServiceBase[Attendee, AttendeeCreate, AttendeeUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Attendee]:
        return db.query(Attendee).filter(Attendee.name == name).first()

    async def get_by_request(self, db: Session, req_id: str) -> Optional[Attendee]:
        return db.query(self.model).filter(self.model.request_id == req_id).first()

    async def upload_photo(self, db: Session, attendee_id: str, photo: UploadFile) -> Type[Attendee]:
        attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
        events = attendee.requests.events.id
        print(events)
        if not attendee.requests:
            event_number = 'default'
        else:
            event_number = attendee.requests.events.id

        print(photo.filename)
        # for req in attendee.requests:
        #     print(req)
        file_location = Path(f"media/event_{event_number}/attendee_photos/{photo.filename}")
        file_location.parent.mkdir(parents=True, exist_ok=True)  # Создаем директории, если они не существуют

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
        attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
        events = attendee.requests.events.id
        print(events)
        if not attendee.requests:
            event_number = 'default'
        else:
            event_number = attendee.requests.events.id

        print(photo.filename)
        # for req in attendee.requests:
        #     print(req)
        file_location = Path(f"media/event_{event_number}/attendee_documents/{photo.filename}")
        file_location.parent.mkdir(parents=True, exist_ok=True)  # Создаем директории, если они не существуют

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

    def create(self, db: Session, obj_in: Union[AttendeeCreate, Dict[str, Any]], **kwargs) -> Attendee:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['assignment_date'] = datetime.strptime(obj_in_data['assignment_date'], '%Y-%m-%d')
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj


attendee_service = AttendeeService(Attendee)

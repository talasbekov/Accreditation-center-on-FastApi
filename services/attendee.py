from datetime import datetime
from pathlib import Path
from typing import Optional, Type, Union, Dict, Any

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from PIL import Image
from io import BytesIO


from sqlalchemy.orm import Session

from models import Attendee, Request
from schemas import AttendeeCreate, AttendeeUpdate
from services.base import ServiceBase

import aiofiles


class AttendeeService(ServiceBase[Attendee, AttendeeCreate, AttendeeUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Attendee]:
        return db.query(Attendee).filter(Attendee.name == name).first()

    def get_attendees_by_event_id(self, db: Session, event_id: str, skip: int, limit: int):
        requests = db.query(Request).filter(Request.event_id == event_id).offset(skip).limit(limit).all()
        attendees = []
        for req in requests:
            for attendee in req.attendees:
                attendees.append(attendee)
        print(attendees)
        return attendees

    async def get_by_request(self, db: Session, req_id: str) -> Optional[Attendee]:
        return db.query(self.model).filter(self.model.request_id == req_id).first()

    async def upload_photo(self, db: Session, attendee_id: str, photo: UploadFile) -> Type[Attendee]:
        attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()

        if not attendee.requests:
            event_number = 'default'
        else:
            event_number = attendee.requests.events.id

        file_location = Path(f"media/event_{event_number}/attendee_photos/{attendee_id}.png")
        file_location.parent.mkdir(parents=True, exist_ok=True)  # Create directories if they do not exist

        # Read the file contents and save it as an image using PIL
        file_contents = await photo.read()
        image = Image.open(BytesIO(file_contents))
        image.save(file_location)

        photo_location = Path(f"event_{event_number}/attendee_photos/{attendee_id}.png")
        attendee.photo = str(photo_location)
        db.commit()
        db.refresh(attendee)

        return attendee

    async def upload_doc_scan(self, db: Session, attendee_id: str, doc_scan: UploadFile) -> Type[Attendee]:
        attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()

        if not attendee.requests:
            event_number = 'default'
        else:
            event_number = attendee.requests.events.id

        file_location = Path(f"media/event_{event_number}/attendee_documents/{doc_scan.filename}")
        file_location.parent.mkdir(parents=True, exist_ok=True)  # Создаем директории, если они не существуют

        async with aiofiles.open(file_location, "wb") as file_object:
            # Assuming 'photo.file' supports async read
            file_contents = doc_scan.file.read()
            await file_object.write(file_contents)

        doc_scan_location = Path(f"event_{event_number}/attendee_documents/{doc_scan.filename}")
        attendee.doc_scan = str(doc_scan_location)
        db.commit()
        db.refresh(attendee)

        return attendee
    
    async def upload_photo_base64(self, db: Session, attendee_id: str, photo: Image.Image) -> Type[Attendee]:
        attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()

        if not attendee.requests:
            event_number = 'default'
        else:
            event_number = attendee.requests.events.id

        file_location = Path(f"media/event_{event_number}/attendee_photos/{attendee_id}.png")
        file_location.parent.mkdir(parents=True, exist_ok=True)  # Create directories if they do not exist

        # Save the PIL image
        photo.save(file_location)

        photo_location = Path(f"event_{event_number}/attendee_photos/{attendee_id}.png")
        attendee.photo = str(photo_location)
        db.commit()
        db.refresh(attendee)

        return attendee

    async def upload_doc_scan_base64(self, db: Session, attendee_id: str, doc_scan: Image.Image) -> Type[Attendee]:
        attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()

        if not attendee.requests:
            event_number = 'default'
        else:
            event_number = attendee.requests.events.id

        file_location = Path(f"media/event_{event_number}/attendee_documents/{attendee_id}.png")
        file_location.parent.mkdir(parents=True, exist_ok=True)  # Create directories if they do not exist

        # Save the PIL image
        doc_scan.save(file_location)

        doc_scan_location = Path(f"event_{event_number}/attendee_documents/{attendee_id}.png")
        attendee.doc_scan = str(doc_scan_location)
        db.commit()
        db.refresh(attendee)

        return attendee

    def create(self, db: Session, obj_in: Union[AttendeeCreate, Dict[str, Any]], **kwargs) -> Attendee:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['birth_date'] = datetime.strptime(obj_in_data['birth_date'], '%Y-%m-%d')
        obj_in_data['doc_begin'] = datetime.strptime(obj_in_data['doc_begin'], '%Y-%m-%d')
        obj_in_data['doc_end'] = datetime.strptime(obj_in_data['doc_end'], '%Y-%m-%d')
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj


attendee_service = AttendeeService(Attendee)

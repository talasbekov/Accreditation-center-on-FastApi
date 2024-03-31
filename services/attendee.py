from pathlib import Path

from fastapi import UploadFile
from typing import Optional, Type
from sqlalchemy.orm import Session

# from exceptions import NotFoundException
from models import Attendee
from schemas import AttendeeCreate, AttendeeUpdate
from services.base import ServiceBase


class AttendeeService(ServiceBase[Attendee, AttendeeCreate, AttendeeUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Attendee]:
        return db.query(Attendee).filter(Attendee.name == name).first()

    async def upload_photo(self, db: Session, attendee_id: str, photo: UploadFile) -> Type[Attendee]:
        attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
        # if not attendee:
        #     raise NotFoundException(detail="Attendee not found")

        for req in attendee.requests:
            for event_number in req.events:
                print(event_number)

        file_location = Path(f"media/event_{event_number}/attendee_photos/{photo.filename}")
        file_location.parent.mkdir(parents=True, exist_ok=True)  # Создаем директории, если они не существуют

        async with photo.file as file_like:
            file_contents = await file_like.read()
            with open(file_location, "wb") as file_object:
                file_object.write(file_contents)

        attendee.photo_path = str(file_location)
        db.commit()
        db.refresh(attendee)

        return attendee


attendee_service = AttendeeService(Attendee)

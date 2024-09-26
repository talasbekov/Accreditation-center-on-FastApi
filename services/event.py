from typing import Optional, Type

from sqlalchemy.orm import Session

from models import Event  # Предполагается, что у вас есть модель Event в models.py
from schemas import (
    EventCreate,
    EventUpdate,
    EventReadWithAttendies,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase
from fastapi.responses import FileResponse, JSONResponse
from fastapi import HTTPException
import shutil
import os
from .request import request_service


def model_to_dict(model_instance):
    """Convert an SQLAlchemy model instance into a dictionary."""
    return {
        attr: getattr(model_instance, attr)
        for attr in dir(model_instance)
        if not attr.startswith("_") and not callable(getattr(model_instance, attr))
    }


class EventService(ServiceBase[Event, EventCreate, EventUpdate]):

    def get_by_id(self, db: Session, event_id: int) -> Type[Event] | None:
        return db.query(self.model).filter(self.model.id == event_id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[Event]:
        return db.query(Event).filter(Event.name == name).first()

    def download_event(self, db: Session, event_id: int) -> FileResponse:
        folder_path = os.path.join("media", f"event_{event_id}")

        # Check if the event folder exists
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail="Event folder not found")

        # Create a ZIP archive of the event folder
        archive_name = os.path.join("media", f"event_{event_id}")
        shutil.make_archive(archive_name, "zip", folder_path)

        # Send the ZIP file as a response
        zip_file_path = f"{archive_name}.zip"
        if not os.path.exists(zip_file_path):
            raise HTTPException(status_code=404, detail="Zip file not found")

        return FileResponse(
            path=zip_file_path,
            filename=os.path.basename(zip_file_path),
            media_type="application/octet-stream",
        )

    def download_event_json(self, db: Session, event_id: int) -> JSONResponse:
        # Fetch the event data from the database
        event = db.query(self.model).filter(self.model.id == event_id).first()
        event_name_eng = self.transliterate(event.name)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        # Convert event data to a dictionary
        event_data = {
            "attendees": [
                {
                    "birthDate": (
                        attendee.birth_date.isoformat()
                        if attendee.birth_date
                        else "1992-12-12"
                    ),
                    "countryId": "1000000105",
                    "dateAdd": (
                        attendee.created_at.isoformat() if attendee.created_at else None
                    ),
                    "dateEnd": (
                        attendee.created_at.isoformat() if attendee.created_at else None
                    ),
                    "docBegin": (
                        attendee.doc_begin.isoformat() if attendee.doc_begin else None
                    ),
                    "docEnd": (
                        attendee.doc_end.isoformat() if attendee.doc_end else None
                    ),
                    "docIssue": attendee.doc_issue,
                    "docNumber": attendee.doc_number,
                    "docScan": attendee.doc_scan,
                    "docSeries": "1",
                    "docTypeId": "1000000003",
                    "firstname": attendee.firstname,
                    "id": str(attendee.id),
                    "iin": attendee.iin,
                    "patronymic": attendee.patronymic,
                    "photo": attendee.photo,
                    "post": attendee.post,
                    "request": str(attendee.request_id),
                    "sex": (
                        "10101"
                        if attendee.sex
                        else "10000102" if attendee.sex is not None else None
                    ),
                    "surname": attendee.surname,
                    "stickId": "1100000022",
                    "transcription": attendee.transcription,
                    "visitObjects": attendee.visit_object,
                }
                for request in event.requests
                for attendee in request.attendees
            ],
            "city_code": event.city_id,
            "date_end": event.date_end.isoformat(),
            "date_start": event.date_start.isoformat(),
            "event_code": event.event_code,
            "id": event.id,
            "name_eng": event_name_eng,
            "name_kaz": event.name if hasattr(event, "name") else None,
            "name": event.name if hasattr(event, "name") else None,
        }

        # Return the JSON response
        return JSONResponse(content=event_data, media_type="application/json")

    def get_event_with_attendees(
        self, db: Session, event_id: int
    ) -> EventReadWithAttendies:
        # Fetch the event by ID
        event = self.get_by_id(db, event_id)
        if event:  # Ensure event is not None
            event_dict = model_to_dict(event)
        else:
            # Handle the case where the event is not found
            return None

        # Initialize an empty list for attendees
        all_attendees = []

        # Fetch requests associated with the event
        requests = request_service.get_by_event_id(db, event_id)

        for request in requests:
            # For each request, fetch associated attendees
            attendees = request.attendees
            all_attendees.extend(attendees)

        # Construct the EventRead object with attendees
        event_read = EventReadWithAttendies(
            **event_dict,  # Assuming event is a Pydantic model or similar
            attendees=all_attendees,
        )

        return event_read


event_service = EventService(Event)

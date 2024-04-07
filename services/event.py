from typing import Optional
from sqlalchemy.orm import Session
from models import Event  # Предполагается, что у вас есть модель Event в models.py
from schemas import (
    EventCreate,
    EventUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase
from fastapi.responses import FileResponse
from fastapi import HTTPException
import shutil
import os


class EventService(ServiceBase[Event, EventCreate, EventUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[Event]:
        return db.query(Event).filter(Event.name == name).first()

    def download_event(self, db: Session, event_id: str) -> FileResponse:
        # Retrieve the attendee from the database
        # if not attendee:
        #     raise HTTPException(status_code=404, detail="Attendee not found")
        #
        # file_path = attendee.photo
        # if not os.path.exists(file_path):
        #     raise HTTPException(status_code=404, detail="File not found")
        #
        # return FileResponse(path=file_path, filename=os.path.basename(file_path))
        folder_path = os.path.join("media", f"event_{event_id}")

        # Check if the event folder exists
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail="Event folder not found")

        # Create a ZIP archive of the event folder
        archive_name = os.path.join("media", f"event_{event_id}")
        shutil.make_archive(archive_name, 'zip', folder_path)

        # Send the ZIP file as a response
        zip_file_path = f"{archive_name}.zip"
        if not os.path.exists(zip_file_path):
            raise HTTPException(status_code=404, detail="Zip file not found")

        return FileResponse(path=zip_file_path, filename=os.path.basename(zip_file_path),
                            media_type='application/octet-stream')


event_service = EventService(Event)

import base64
import io
from typing import List

from PIL import Image
from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from core import get_db
from exceptions import BadRequestException
from schemas import (
    GovAttendeeCreate,
    GovAttendeeRequest,
    RequestCreate,
    AttendeeCreate,
)
from services import (
    attendee_service,
    request_service,
    event_service,
    country_service,
    document_service,
)
from utils import is_valid_base64, correct_base64_padding

router = APIRouter(prefix="/gov", tags=["GovAttendees"])


@router.get(
    "/data",
    response_model=List[GovAttendeeRequest],
    summary="Get all Attendees by request",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all necessary data
    """
    events = event_service.get_multi(db, skip, limit)
    countries = country_service.get_multi(db, skip, limit)
    doc_types = document_service.get_multi(db, skip, limit)
    attendees = []
    for event, country, doc_type in zip(events, countries, doc_types):
        attendee = GovAttendeeRequest(
            events=[event], countries=[country], doc_types=[doc_type]
        )
        attendees.append(attendee)

    return attendees


@router.post(
    "/create/attendee",
    status_code=status.HTTP_201_CREATED,
    summary="Create Attendee",
    response_model=GovAttendeeCreate,
)
async def create_attendee(
    *,
    db: Session = Depends(get_db),
    body: GovAttendeeRequest,
):

    try:
        # Create a request for attendees
        request_for_attendees = request_service.create(
            db, obj_in=RequestCreate(event_id=body.event_id, created_by_id=1)
        )

        for attendee in body.attendees:
            # Correct base64 padding and validate
            photo_data_str = correct_base64_padding(attendee.photo)
            doc_scan_data_str = correct_base64_padding(attendee.doc_scan)
            print(photo_data_str)

            if not is_valid_base64(photo_data_str):
                raise BadRequestException(detail="Invalid base64 data for photo")
            if not is_valid_base64(doc_scan_data_str):
                raise BadRequestException(
                    detail="Invalid base64 data for document scan"
                )

            try:
                # Decode base64 photo and document scan
                photo_data = base64.b64decode(photo_data_str)
                doc_scan_data = base64.b64decode(doc_scan_data_str)
            except base64.binascii.Error:
                raise BadRequestException(detail="Error decoding base64 data")

            try:
                # Convert the decoded data to PIL images
                photo_image = Image.open(io.BytesIO(photo_data))
                doc_scan_image = Image.open(io.BytesIO(doc_scan_data))
            except IOError as e:
                raise BadRequestException(detail=f"Cannot identify image file: {e}")

            # Create the attendee object in the database
            db_obj = attendee_service.create(
                db,
                obj_in=AttendeeCreate(
                    request_id=request_for_attendees.id,
                    **attendee.dict(exclude={"photo", "doc_scan"}),
                ),
            )

            # Save the images to appropriate locations or services
            await attendee_service.upload_photo_base64(db, db_obj.id, photo_image)
            await attendee_service.upload_doc_scan_base64(db, db_obj.id, doc_scan_image)

        db.commit()  # Commit the transaction
        return db_obj
    except BadRequestException as e:
        db.rollback()  # Roll back the transaction on error
        raise e  # Re-raise the exception to return the error response
    except Exception as e:
        db.rollback()
        raise BadRequestException(detail=str(e))

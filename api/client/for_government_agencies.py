import base64
import io
from PIL import Image
from fastapi import Depends, status, APIRouter
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from core import get_db
from exceptions import BadRequestException
from schemas import GovAttendeeCreate, GovAttendeeRequest, RequestCreate, AttendeeCreate
from services import attendee_service, request_service


router = APIRouter(
    prefix="/gov", tags=["GovAttendees"]
)

def correct_base64_padding(data: str) -> str:
    """Add padding to Base64 string if necessary."""
    return data + '=' * (-len(data) % 4)

@router.post(
    "/create/attendee",
    status_code=status.HTTP_201_CREATED,
    summary="Create Attendee",
    response_model=GovAttendeeCreate
)
async def create_attendee(
    *, db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    body: GovAttendeeRequest,
):
    Authorize.jwt_required()

    try:
        # Create a request for attendees
        request_for_attendees = request_service.create(
            db, obj_in=RequestCreate(event_id=body.event_id, created_by_id=1)
        )

        for attendee in body.attendees:
            # Correct base64 padding
            photo_data_str = correct_base64_padding(attendee.photo)
            doc_scan_data_str = correct_base64_padding(attendee.doc_scan)

            # Decode base64 photo and document scan
            photo_data = base64.b64decode(photo_data_str)
            doc_scan_data = base64.b64decode(doc_scan_data_str)
            print(1)

            # Convert the decoded data to PIL images
            photo_image = Image.open(io.BytesIO(photo_data))
            print(type(photo_image))
            doc_scan_image = Image.open(io.BytesIO(doc_scan_data))

            # Create the attendee object in the database
            db_obj = attendee_service.create(
                db, obj_in=AttendeeCreate(request_id=request_for_attendees.id, **attendee.dict(exclude={"photo", "doc_scan"}))
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

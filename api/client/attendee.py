# from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File, Request
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from core import get_db
# from exceptions import NotFoundException
# from models import Attendee

from schemas import AttendeeRead, AttendeeUpdate, AttendeeCreate
from services import attendee_service

router = APIRouter(
    prefix="/attendee", tags=["Attendees"], dependencies=[Depends(HTTPBearer())]
)

templates = Jinja2Templates(directory='templates')


@router.post("/{attendee_id}/upload-photo/", dependencies=[Depends(HTTPBearer())],
             summary="Upload Image File")
async def upload_attendee_photo(
    attendee_id: str,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    attendee = await attendee_service.upload_photo(db, attendee_id, photo)
    return attendee


@router.post("/{attendee_id}/upload-photo-scan/", dependencies=[Depends(HTTPBearer())],
             summary="Upload Image File")
async def upload_attendee_photo_scan(
    attendee_id: str,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    attendee = await attendee_service.upload_photo_scan(db, attendee_id, photo)
    return attendee


@router.get(
    "",
    summary="Get all Attendees",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    request: Request,
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all Attendees

    """

    all_attendees = attendee_service.get_multi(db, skip, limit)
    return templates.TemplateResponse(
        request=request, name='all_attendees.html', context={'all_attendees': all_attendees}
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(HTTPBearer())],
    response_model=AttendeeRead,
    summary="Create Position",
)
async def create(
    *,
    db: Session = Depends(get_db),
    body: AttendeeCreate,
    Authorize: AuthJWT = Depends()
):
    """
    Create Attendee

    - **name**: required
    """
    Authorize.jwt_required()
    return attendee_service.create(db, body)


@router.get(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=AttendeeRead,
    summary="Get Attendee by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Get Attendee by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return attendee_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=AttendeeRead,
    summary="Update Attendee",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: AttendeeUpdate,
    Authorize: AuthJWT = Depends()
):
    """
    Update Attendee

    """
    Authorize.jwt_required()
    return attendee_service.update(
        db, db_obj=attendee_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(HTTPBearer())],
    summary="Delete Attendee",
)
async def delete(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Delete Attendee

    - **id**: UUId - required
    """
    Authorize.jwt_required()
    attendee_service.remove(db, str(id))
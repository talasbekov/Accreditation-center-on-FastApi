from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File, Request

from fastapi.responses import HTMLResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from core import get_db, configs

from schemas import AttendeeRead, AttendeeUpdate, AttendeeCreate
from services import attendee_service

router = APIRouter(
    prefix="/attendee", tags=["Attendees"]
)

templates = Jinja2Templates(directory='templates')


@router.post("/{attendee_id}/upload-photo/",
             summary="Upload Image File")
async def upload_attendee_photo(
    attendee_id: str,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    attendee = await attendee_service.upload_photo(db, attendee_id, photo)
    return attendee


@router.post("/{attendee_id}/upload-photo-scan/",
             summary="Upload Image File")
async def upload_attendee_photo_scan(
    attendee_id: str,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    attendee = await attendee_service.upload_photo_scan(db, attendee_id, photo)
    return attendee


@router.get(
    "/all",
    response_model=List[AttendeeRead],
    summary="Get all Attendees by request",
    response_class=HTMLResponse
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    request: Request,
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Requests
    """
    Authorize.jwt_required()
    user_email = Authorize.get_raw_jwt()['email']
    attendees = attendee_service.get_multi(db, skip, limit)
    return configs.templates.TemplateResponse(
        "all_attendees.html",
        {
            "request": request,
            "attendees": attendees,
            "user_email": user_email
        }
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AttendeeRead,
    summary="Create Position",
    response_class=HTMLResponse
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
    attendee = attendee_service.create(db, body)
    return attendee


@router.get(
    "/{id}/",
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
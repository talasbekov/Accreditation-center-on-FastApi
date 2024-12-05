from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from fastapi_jwt import JwtAccessBearer

from core import get_db, configs

from schemas import AttendeeRead, AttendeeUpdate, AttendeeCreate
from services import attendee_service

# Инициализируем JwtAccessBearer с вашим секретным ключом
auth = JwtAccessBearer(secret_key=configs.SECRET_KEY)

router = APIRouter(prefix="/attendee", tags=["Attendees"])

@router.post(
    "/{attendee_id}/upload-photo/",
    summary="Upload Image File",
)
async def upload_attendee_photo(
    attendee_id: str,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    credentials=Depends(auth),
):
    attendee = await attendee_service.upload_photo(db, attendee_id, photo)
    return attendee

@router.post(
    "/{attendee_id}/upload-photo-scan/",
    summary="Upload Image File",
)
async def upload_attendee_photo_scan(
    attendee_id: str,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    credentials=Depends(auth),
):
    attendee = await attendee_service.upload_photo_scan(db, attendee_id, photo)
    return attendee

@router.get(
    "",
    response_model=List[AttendeeRead],
    summary="Get all Attendees",
)
async def get_all(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    credentials=Depends(auth),
):
    """
    Get all Attendees
    """
    return attendee_service.get_multi(db, skip, limit)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AttendeeRead,
    summary="Create Attendee",
)
async def create(
    body: AttendeeCreate,
    db: Session = Depends(get_db),
    credentials=Depends(auth),
):
    """
    Create Attendee

    - **name**: required
    """
    return attendee_service.create(db, body)

@router.get(
    "/{id}/",
    response_model=AttendeeRead,
    summary="Get Attendee by id",
)
async def get_by_id(
    id: str,
    db: Session = Depends(get_db),
    credentials=Depends(auth),
):
    """
    Get Attendee by id

    - **id**: String - required.
    """
    return attendee_service.get_by_id(db, id)

@router.put(
    "/{id}/",
    response_model=AttendeeRead,
    summary="Update Attendee",
)
async def update(
    id: str,
    body: AttendeeUpdate,
    db: Session = Depends(get_db),
    credentials=Depends(auth),
):
    """
    Update Attendee
    """
    attendee = attendee_service.get_by_id(db, id)
    return attendee_service.update(db, db_obj=attendee, obj_in=body)

@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Attendee",
)
async def delete(
    id: str,
    db: Session = Depends(get_db),
    credentials=Depends(auth),
):
    """
    Delete Attendee

    - **id**: String - required
    """
    attendee_service.remove(db, id)

@router.post("/reload/", summary="Reload Attendees")
async def reload(db: Session = Depends(get_db)):
    return await attendee_service.reload(db)

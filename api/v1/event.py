from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import EventRead, EventUpdate, EventCreate
from services import event_service

router = APIRouter(
    prefix="/events", tags=["Events"], dependencies=[Depends(HTTPBearer())]
)


@router.get(
    "",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[EventRead],
    summary="Get all Events",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Events

    """
    Authorize.jwt_required()
    return event_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(HTTPBearer())],
    response_model=EventRead,
    summary="Create Event",
)
async def create(
    *, db: Session = Depends(get_db), body: EventCreate, Authorize: AuthJWT = Depends()
):
    """
    Create Event

    - **name**: required
    """
    Authorize.jwt_required()
    return event_service.create(db, body)


@router.get(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=EventRead,
    summary="Get Event by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Get Event by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return event_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=EventRead,
    summary="Update Event",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: EventUpdate,
    Authorize: AuthJWT = Depends()
):
    """
    Update Event

    """
    Authorize.jwt_required()
    return event_service.update(
        db, db_obj=event_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(HTTPBearer())],
    summary="Delete Event",
)
async def delete(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Delete Event

    - **id**: UUId - required
    """
    Authorize.jwt_required()
    event_service.remove(db, str(id))

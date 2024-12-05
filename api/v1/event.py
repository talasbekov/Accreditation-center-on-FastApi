from typing import List

from fastapi import APIRouter, Depends, status, Request
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db, configs


from schemas import EventRead, EventUpdate, EventCreate, EventReadWithAttendies
from services import event_service


router = APIRouter(
    prefix="/events", tags=["Events"], dependencies=[Depends(HTTPBearer())]
)


@router.get("/download/{event_id}")
async def download_event_zip(event_id: str, db: Session = Depends(get_db)):
    return event_service.download_event(db, event_id)


@router.get(
    "",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[EventRead],
    summary="Get all Events",
)
async def get_all(
    request: Request,
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
    events = event_service.get_multi(db, skip, limit)
    return configs.templates.TemplateResponse(
        "events.html", {"request": request, "events": events}
    )


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


@router.get(
    "/with_attendees/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=EventReadWithAttendies,
    summary="Get Event with Attendees",
)
async def get_by_id_with_attendees(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Get Event by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return event_service.get_event_with_attendees(db, str(id))

@router.get(
    "/user/",
    dependencies=[Depends(HTTPBearer())],
    response_model=EventReadWithAttendies,
    summary="Get Event with Attendees",
)
async def get_event_by_user(
    *, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    """
    Get Event by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    # Get user ID from the JWT token's subject
    user_id = Authorize.get_jwt_subject()
    return event_service.get_event_by_user(db, user_id)

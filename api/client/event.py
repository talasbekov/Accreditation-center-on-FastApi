from datetime import date
from typing import List

from fastapi import APIRouter, Depends, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db, configs


from schemas import EventRead, EventUpdate, EventCreate, EventReadWithAttendies
from services import event_service, city_service
from exceptions import InvalidOperationException, BadRequestException

router = APIRouter(
    prefix="/events", tags=["Events"]
)


@router.get("/download/{event_id}")
async def download_event_zip(event_id: str, db: Session = Depends(get_db)):
    return event_service.download_event(db, event_id)


@router.get(
    "",
    response_model=List[EventRead],
    summary="Get all Events",
    response_class=HTMLResponse
)
async def get_all(
    request: Request,
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Events
    """
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    user_email = Authorize.get_raw_jwt()['email']
    events = event_service.get_multi(db, skip, limit)
    return configs.templates.TemplateResponse(
        "events.html",
        {
            "request": request,
            "events": events,
            "user": user,
            "user_email": user_email
        }
    )


@router.get(
    "/create",
    response_model=EventRead,
    summary="Create Event",
    response_class=HTMLResponse
)
async def create_form(
    *,
    request: Request,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """
    Create Event
    - **name**: required
    """
    Authorize.jwt_required()
    user_email = Authorize.get_raw_jwt()['email']
    cities = city_service.get_multi(db)
    try:
        return configs.templates.TemplateResponse(
            "create_event.html",
            {
                "request": request,
                "cities": cities,
                "user_email": user_email
            }
        )
    except Exception as e:
        raise InvalidOperationException(
            detail=f"Failed to create event: {str(e)}"
        )


@router.post(
    "/create/event",
    status_code=status.HTTP_201_CREATED,
    response_model=EventRead,
    summary="Create Event",
)
async def create(
    *, db: Session = Depends(get_db),
    request: Request,
    name: str = Form(...),
    lead: str = Form(...),
    event_code: str = Form(...),
    date_start: date = Form(...),
    date_end: date = Form(...),
    city_id: str = Form(...),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()

    body = EventCreate(
        name=name,
        lead=lead,
        event_code=event_code,
        date_start=date_start,
        date_end=date_end,
        city_id=city_id
    )
    try:
        event_service.create(db, body)
        return RedirectResponse(url="/api/client/events", status_code=status.HTTP_303_SEE_OTHER)
    except BadRequestException as e:
        return configs.templates.TemplateResponse("create_event.html", {"request": request, "error": str(e)})



@router.get(
    "/{id}/",
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

from datetime import date
from typing import List

from fastapi import APIRouter, Depends, status, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db, configs


from schemas import (
    EventRead,
    EventUpdate,
    EventCreate,
    RequestRead,
)
from services import (
    event_service,
    city_service,
    user_service,
    request_service,
    attendee_service,
)
from exceptions import InvalidOperationException, BadRequestException

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/download/zip/event_{event_id}")
async def download_event_zip(
    event_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return event_service.download_event(db, event_id)


@router.get("/download/json/event_{event_id}")
async def download_event_json(
    event_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return event_service.download_event_json(db, event_id)


@router.get(
    "",
    response_model=List[EventRead],
    summary="Get all Events",
    response_class=HTMLResponse,
)
async def get_all(
    request: Request,
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    Authorize: AuthJWT = Depends(),
):
    """
    Get all Events
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    if user.admin is True:
        events = event_service.get_multi(db, skip, limit)
    else:
        events = user.events

    return configs.templates.TemplateResponse(
        "events.html",
        {
            "request": request,
            "events": events,
            "user": user,
        },
    )


@router.get(
    "/event_{event_id}/requests",
    response_model=List[RequestRead],
    summary="Get all Attendees by request",
    response_class=HTMLResponse,
)
async def get_requests_by_event_id(
    *,
    db: Session = Depends(get_db),
    request: Request,
    event_id: int,
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends(),
):
    """
    Get all Requests
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    requests = request_service.get_by_event_id(db, event_id, skip, limit)
    return configs.templates.TemplateResponse(
        "requests.html",
        {"request": request, "requests": requests, "user": user, "event_id": event_id},
    )


@router.get(
    "/event_{event_id}/attendees",
    response_model=List[RequestRead],
    summary="Get all Attendees by request",
    response_class=HTMLResponse,
)
async def get_attendees_by_event_id(
    *,
    db: Session = Depends(get_db),
    request: Request,
    event_id: int,
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends(),
):
    """
    Get all Attendees
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    attendees = attendee_service.get_attendees_by_event_id(db, event_id, skip, limit)
    return configs.templates.TemplateResponse(
        "all_attendees.html", {"request": request, "attendees": attendees, "user": user}
    )


@router.get(
    "/create",
    response_model=EventRead,
    summary="Create Event",
    response_class=HTMLResponse,
)
async def create_form(
    *, request: Request, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    """
    Create Event
    - **name**: required
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    cities = city_service.get_multi(db)
    users = user_service.get_multi(db)
    try:
        return configs.templates.TemplateResponse(
            "create_event.html",
            {"request": request, "cities": cities, "users": users, "user": user},
        )
    except Exception as e:
        raise InvalidOperationException(detail=f"Failed to create event: {str(e)}")


@router.post(
    "/create/event",
    status_code=status.HTTP_201_CREATED,
    response_model=EventRead,
    summary="Create Event",
)
async def create(
    *,
    db: Session = Depends(get_db),
    request: Request,
    Authorize: AuthJWT = Depends(),
    name: str = Form(...),
    lead: str = Form(...),
    event_code: str = Form(...),
    date_start: date = Form(...),
    date_end: date = Form(...),
    city_id: str = Form(...),
    is_for_gov: str = Form(...),
    users: List[str] = Form(default=[]),  # Set a default empty list if None
):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    users_objects = [
        user_service.get(db=db, id=user_id) for user_id in users if user_id
    ]  # Ensure user_id is not None
    body = EventCreate(
        name=name,
        lead=lead,
        event_code=event_code,
        date_start=date_start,
        date_end=date_end,
        city_id=city_id,
        is_for_gov=is_for_gov
    )
    try:
        db_obj = event_service.create(db, body)
        db_obj.users = users_objects  # Assign the list of User objects
        db.add(db_obj)
        db.commit()  # Commit the transaction
        return RedirectResponse(
            url="/api/client/events", status_code=status.HTTP_303_SEE_OTHER
        )
    except BadRequestException as e:
        db.rollback()  # Roll back the transaction on error
        return configs.templates.TemplateResponse(
            "create_event.html", {"request": request, "error": str(e), "user": user}
        )


@router.get(
    "/update/event_{event_id}", summary="Update Event", response_class=HTMLResponse
)
async def update_event_form(
    *,
    db: Session = Depends(get_db),
    request: Request,
    event_id: int,
    skip: int = 0,
    limit: int = 10,
    Authorize: AuthJWT = Depends(),
):
    """
    Update Attendee
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    users = user_service.get_multi(db, skip, limit)
    cities = city_service.get_multi(db, skip, limit)
    if user.admin is True:
        try:
            event = event_service.get_by_id(db, event_id)
            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
                )

            return configs.templates.TemplateResponse(
                "update_event.html",
                {
                    "request": request,
                    "event": event,
                    "user": user,
                    "users": users,
                    "cities": cities,
                },
            )
        except Exception as e:
            raise InvalidOperationException(
                detail=f"Failed to move to update event list: {str(e)}"
            )
    else:
        return RedirectResponse(
            url="/api/client/events", status_code=status.HTTP_403_FORBIDDEN
        )


@router.patch(
    "/update/patch/event_{event_id}",
    status_code=status.HTTP_200_OK,
    summary="Update Event",
)
async def update_event(
    *,
    db: Session = Depends(get_db),
    request: Request,
    event_id: int,
    event_code: str = Form(None),
    lead: str = Form(None),
    city_id: str = Form(None),
    date_start: date = Form(None),
    date_end: date = Form(None),
    users: List[str] = Form(default=[]),
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    # Ensure user_id is not None
    users_objects = [
        user_service.get(db=db, id=user_id) for user_id in users if user_id
    ]
    if user.admin is True:
        # Fetch the existing attendee from the database
        event = event_service.get_by_id(db, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )
        updated_data = EventUpdate(
            event_code=event_code or event.event_code,
            lead=lead or event.lead,
            city_id=city_id or event.city_id,
            date_start=date_start or event.date_start,
            date_end=date_end or event.date_end,
        )
        try:
            obj = event_service.update(db=db, db_obj=event, obj_in=updated_data)
            obj.users = users_objects

            db.commit()
            return RedirectResponse(
                url="/api/client/events", status_code=status.HTTP_303_SEE_OTHER
            )
        except Exception as e:
            raise InvalidOperationException(
                detail=f"Failed to update attendee: {str(e)}"
            )
    else:
        return RedirectResponse(
            url="/api/client/events", status_code=status.HTTP_403_FORBIDDEN
        )

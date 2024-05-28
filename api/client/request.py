from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db, configs

from schemas import RequestRead
from services import request_service, user_service

router = APIRouter(
    prefix="/requests", tags=["Requests"]
)


@router.get(
    "",
    response_model=List[RequestRead],
    summary="Get all Requests",
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
    user = Authorize.get_raw_jwt()['email']
    requests = request_service.get_multi(db, skip, limit)
    return configs.templates.TemplateResponse(
        "requests.html",
        {
            "request": request,
            "requests": requests,
            "user": user
        }
    )


@router.get(
    "/request_{request_id}/attendees",
    response_model=List[RequestRead],
    summary="Get all Attendees by request",
    response_class=HTMLResponse
)
async def get_attendees_by_request(
    *,
    db: Session = Depends(get_db),
    request: Request,
    request_id: str,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Requests
    """
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = user_service.get_by_id(db, user_id)
    req = request_service.get_by_id(db, request_id)
    return configs.templates.TemplateResponse(
        "request_attendees.html",
        {
            "request": request,
            "req": req,
            "user": user
        }
    )

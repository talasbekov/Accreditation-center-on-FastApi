from typing import List

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db, configs

from schemas import RequestRead, RequestUpdate, RequestCreate
from services import request_service

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
    user_email = Authorize.get_raw_jwt()['email']
    requests = request_service.get_multi(db, skip, limit)
    return configs.templates.TemplateResponse(
        "requests.html",
        {
            "request": request,
            "requests": requests,
            "user_email": user_email
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
    user_email = Authorize.get_raw_jwt()['email']
    req = request_service.get_by_id(db, request_id)
    return configs.templates.TemplateResponse(
        "request_attendees.html",
        {
            "request": request,
            "req": req,
            "user_email": user_email
        }
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=RequestRead,
    summary="Create Request",
    response_class=HTMLResponse
)
async def create(
    *,
    db: Session = Depends(get_db),
    body: RequestCreate,
    Authorize: AuthJWT = Depends()
):
    """
    Create Request

    - **name**: required
    """
    Authorize.jwt_required()
    user_email = Authorize.get_raw_jwt()['email']
    print(user_email)
    requests = request_service.create(db, body)
    return configs.templates.TemplateResponse(requests)


@router.get(
    "/{id}/",
    response_model=RequestRead,
    summary="Get Request by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Get Request by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return request_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=RequestRead,
    summary="Update Request",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: RequestUpdate,
    Authorize: AuthJWT = Depends()
):
    """
    Update Request

    """
    Authorize.jwt_required()
    return request_service.update(
        db, db_obj=request_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(HTTPBearer())],
    summary="Delete Request",
)
async def delete(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Delete Request

    - **id**: UUId - required
    """
    Authorize.jwt_required()
    request_service.remove(db, str(id))

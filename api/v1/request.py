from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import Request

from schemas import RequestRead, RequestUpdate
from services import request_service

router = APIRouter(prefix="/requests",
                   tags=["Requests"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[RequestRead],
            summary="Get all Requests")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Requests

    """
    Authorize.jwt_required()
    return request_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=RequestRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new Request

        no parameters required.
    """
    Authorize.jwt_required()
    request = db.query(Request).filter(
        Request.user_id==Authorize.get_jwt_subject()
    ).first()
    if request is not None:
        return request
    return request_service.create(db, {"user_id": Authorize.get_jwt_subject()})


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=RequestRead,
            summary="Get Request by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Request by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return request_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=RequestRead,
            summary="Update Request")
async def update(*,
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
        db,
        db_obj=request_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Request")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Request

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    request_service.remove(db, str(id))

from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import Attendee

from schemas import AttendeeRead, AttendeeUpdate
from services import attendee_service

router = APIRouter(prefix="/attendee",
                   tags=["Attendees"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[AttendeeRead],
            summary="Get all Attendees")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Attendees

    """
    Authorize.jwt_required()
    return attendee_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=AttendeeRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new Attendee

        no parameters required.
    """
    Authorize.jwt_required()
    attendee = db.query(Attendee).filter(Attendee.user_id ==
                                       Authorize.get_jwt_subject()).first()
    if attendee is not None:
        return attendee
    return attendee_service.create(db, {"user_id": Authorize.get_jwt_subject()})


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AttendeeRead,
            summary="Get Attendee by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Attendee by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return attendee_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=AttendeeRead,
            summary="Update Attendee")
async def update(*,
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
        db,
        db_obj=attendee_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Attendee")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Attendee

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    attendee_service.remove(db, str(id))

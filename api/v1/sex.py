from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import Sex

from schemas import SexRead, SexUpdate
from services import sex_service

router = APIRouter(prefix="/sexes",
                   tags=["Sexes"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[SexRead],
            summary="Get all Sexes")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Sexes

    """
    Authorize.jwt_required()
    return sex_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=SexRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new Sex

        no parameters required.
    """
    Authorize.jwt_required()
    sex = db.query(Sex).filter(
        Sex.user_id==Authorize.get_jwt_subject()
    ).first()
    if sex is not None:
        return sex
    return sex_service.create(db, {"user_id": Authorize.get_jwt_subject()})


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SexRead,
            summary="Get Sex by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Sex by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return sex_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=SexRead,
            summary="Update Sex")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: SexUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Sex

    """
    Authorize.jwt_required()
    return sex_service.update(
        db,
        db_obj=sex_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Sex")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Sex

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    sex_service.remove(db, str(id))

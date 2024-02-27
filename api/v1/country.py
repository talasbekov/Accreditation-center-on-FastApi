from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import CountryRead, CountryUpdate, CountryCreate
from services import country_service

router = APIRouter(prefix="/countries",
                   tags=["Countrys"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[CountryRead],
            summary="Get all Countrys")
async def get_all(*,
                  db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 100,
                  Authorize: AuthJWT = Depends()
                  ):
    """
        Get all Countrys

    """
    Authorize.jwt_required()
    return country_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=CountryRead,
             summary="Create Country")
async def create(*,
                 db: Session = Depends(get_db),
                 body: CountryCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create Country

        - **name**: required
    """
    Authorize.jwt_required()
    return country_service.create(db, body)


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CountryRead,
            summary="Get Country by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get Country by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return country_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=CountryRead,
            summary="Update Country")
async def update(*,
                 db: Session = Depends(get_db),
                 id: str,
                 body: CountryUpdate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Update Country

    """
    Authorize.jwt_required()
    return country_service.update(
        db,
        db_obj=country_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete Country")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete Country

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    country_service.remove(db, str(id))

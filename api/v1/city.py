from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import CityRead, CityUpdate, CityCreate
from services import city_service

router = APIRouter(
    prefix="/cities", tags=["Cities"], dependencies=[Depends(HTTPBearer())]
)


@router.get(
    "",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[CityRead],
    summary="Get all Cities",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Citys

    """
    Authorize.jwt_required()
    return city_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(HTTPBearer())],
    response_model=CityRead,
    summary="Create City",
)
async def create(
    *, db: Session = Depends(get_db), body: CityCreate, Authorize: AuthJWT = Depends()
):
    """
    Create City

    - **name**: required
    """
    Authorize.jwt_required()
    return city_service.create(db, body)


@router.get(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=CityRead,
    summary="Get City by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Get City by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return city_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=CityRead,
    summary="Update City",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: CityUpdate,
    Authorize: AuthJWT = Depends()
):
    """
    Update City

    """
    Authorize.jwt_required()
    return city_service.update(
        db, db_obj=city_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(HTTPBearer())],
    summary="Delete City",
)
async def delete(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Delete City

    - **id**: UUId - required
    """
    Authorize.jwt_required()
    city_service.remove(db, str(id))

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core import get_db

from schemas import CityRead, CityUpdate, CityCreate
from services import city_service

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get(
    "",
    response_model=List[CityRead],
    summary="Get all Cities",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all Citys

    """
    return city_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CityRead,
    summary="Create City",
)
async def create(*, db: Session = Depends(get_db), body: CityCreate):
    """
    Create City

    - **name**: required
    """
    return city_service.create(db, body)


@router.get(
    "/{id}/",
    response_model=CityRead,
    summary="Get City by id",
)
async def get_by_id(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Get City by id

    - **id**: UUID - required.
    """

    return city_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    response_model=CityRead,
    summary="Update City",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: CityUpdate,
):
    """
    Update City

    """
    return city_service.update(
        db, db_obj=city_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete City",
)
async def delete(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Delete City

    - **id**: UUId - required
    """

    city_service.remove(db, str(id))

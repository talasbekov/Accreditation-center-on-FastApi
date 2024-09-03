from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core import get_db

from schemas import CountryRead, CountryUpdate, CountryCreate
from services import country_service

router = APIRouter(prefix="/countries", tags=["Countrys"])


@router.get(
    "",
    response_model=List[CountryRead],
    summary="Get all Countrys",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all Countrys

    """
    return country_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CountryRead,
    summary="Create Country",
)
async def create(
    *,
    db: Session = Depends(get_db),
    body: CountryCreate,
):
    """
    Create Country

    - **name**: required
    """

    return country_service.create(db, body)


@router.get(
    "/{id}/",
    response_model=CountryRead,
    summary="Get Country by id",
)
async def get_by_id(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Get Country by id

    - **id**: UUID - required.
    """

    return country_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    response_model=CountryRead,
    summary="Update Country",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: CountryUpdate,
):
    """
    Update Country

    """

    return country_service.update(
        db, db_obj=country_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Country",
)
async def delete(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Delete Country

    - **id**: UUId - required
    """

    country_service.remove(db, str(id))

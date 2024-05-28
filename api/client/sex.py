from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core import get_db

from schemas import SexRead, SexUpdate, SexCreate
from services import sex_service

router = APIRouter(
    prefix="/sexes", tags=["Sexes"]
)


@router.get(
    "",

    response_model=List[SexRead],
    summary="Get all Sexes",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,

):
    """
    Get all Sexes

    """

    return sex_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,

    response_model=SexRead,
    summary="Create Sex",
)
async def create(
    *, db: Session = Depends(get_db), body: SexCreate,
):
    """
    Create Sex

    - **name**: required
    """

    return sex_service.create(db, body)


@router.get(
    "/{id}/",

    response_model=SexRead,
    summary="Get Sex by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str,
):
    """
    Get Sex by id

    - **id**: UUID - required.
    """

    return sex_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    response_model=SexRead,
    summary="Update Sex",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: SexUpdate,
):
    """
    Update Sex

    """
    return sex_service.update(
        db, db_obj=sex_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,

    summary="Delete Sex",
)
async def delete(
    *, db: Session = Depends(get_db), id: str,
):
    """
    Delete Sex

    - **id**: UUId - required
    """

    sex_service.remove(db, str(id))

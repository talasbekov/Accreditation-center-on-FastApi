from typing import List

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from core import get_db

from schemas import CategoryRead, CategoryUpdate, CategoryCreate
from services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get(
    "",
    response_model=List[CategoryRead],
    summary="Get all Categories",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all Categories

    """

    return category_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryRead,
    summary="Create Position",
)
async def create(
    *,
    db: Session = Depends(get_db),
    body: CategoryCreate,
):
    """
    Create Category

    - **name**: required
    """

    return category_service.create(db, body)


@router.get(
    "/{id}/",
    response_model=CategoryRead,
    summary="Get Category by id",
)
async def get_by_id(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Get Category by id

    - **id**: UUID - required.
    """

    return category_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    response_model=CategoryRead,
    summary="Update Category",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: CategoryUpdate,
):
    """
    Update Category

    """

    return category_service.update(
        db, db_obj=category_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Category",
)
async def delete(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Delete Category

    - **id**: UUId - required
    """

    category_service.remove(db, str(id))

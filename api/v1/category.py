from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import CategoryRead, CategoryUpdate, CategoryCreate
from services import category_service

router = APIRouter(
    prefix="/categories", tags=["Categories"], dependencies=[Depends(HTTPBearer())]
)


@router.get(
    "",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[CategoryRead],
    summary="Get all Categories",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Categories

    """
    Authorize.jwt_required()
    return category_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(HTTPBearer())],
    response_model=CategoryRead,
    summary="Create Position",
)
async def create(
    *,
    db: Session = Depends(get_db),
    body: CategoryCreate,
    Authorize: AuthJWT = Depends()
):
    """
    Create Category

    - **name**: required
    """
    Authorize.jwt_required()
    return category_service.create(db, body)


@router.get(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=CategoryRead,
    summary="Get Category by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Get Category by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return category_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=CategoryRead,
    summary="Update Category",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: CategoryUpdate,
    Authorize: AuthJWT = Depends()
):
    """
    Update Category

    """
    Authorize.jwt_required()
    return category_service.update(
        db, db_obj=category_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(HTTPBearer())],
    summary="Delete Category",
)
async def delete(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Delete Category

    - **id**: UUId - required
    """
    Authorize.jwt_required()
    category_service.remove(db, str(id))

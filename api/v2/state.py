from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer

from sqlalchemy.orm import Session

from core import get_db

from schemas.record import StateRead, StateUpdate, StateCreate
from services import state_service

router = APIRouter(prefix="/states", tags=["States"], dependencies=[Depends(HTTPBearer())])


@router.get(
    "",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[StateRead],
    summary="Get all States",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 500,
):
    """
    Get all States

    """

    return state_service.get_multi(db, skip, limit)


@router.post(
    "",
    dependencies=[Depends(HTTPBearer())],
    status_code=status.HTTP_201_CREATED,
    response_model=StateRead,
    summary="Create State",
)
async def create(
    *,
    db: Session = Depends(get_db),
    body: StateCreate,
):
    """
    Create State

    - **name**: required
    """

    return state_service.create(db, body)


@router.get(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=StateRead,
    summary="Get State by id",
)
async def get_by_id(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Get State by id

    - **id**: UUID - required.
    """

    return state_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=StateRead,
    summary="Update State",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: StateUpdate,
):
    """
    Update State

    """

    return state_service.update(
        db, db_obj=state_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete State",
)
async def delete(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Delete State

    - **id**: UUId - required
    """

    state_service.remove(db, str(id))

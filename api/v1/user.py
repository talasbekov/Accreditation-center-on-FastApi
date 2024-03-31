from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db

from schemas import UserRead, UserUpdate, UserCreate
from services import user_service

router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(HTTPBearer())]
)


@router.get(
    "",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[UserRead],
    summary="Get all Users",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Users

    """
    Authorize.jwt_required()
    return user_service.get_multi(db, skip, limit)


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=UserRead,
             summary="Create User")
async def create(*,
                 db: Session = Depends(get_db),
                 body: UserCreate,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create User

        - **name**: required
    """
    Authorize.jwt_required()
    return user_service.create(db, body)


@router.get(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=UserRead,
    summary="Get User by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Get User by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return user_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=UserRead,
    summary="Update User",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: UserUpdate,
    Authorize: AuthJWT = Depends()
):
    """
    Update User

    """
    Authorize.jwt_required()
    return user_service.update(
        db, db_obj=user_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(HTTPBearer())],
    summary="Delete User",
)
async def delete(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Delete User

    - **id**: UUId - required
    """
    Authorize.jwt_required()
    user_service.remove(db, str(id))

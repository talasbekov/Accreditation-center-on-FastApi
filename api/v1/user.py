from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import User

from schemas import UserRead, UserUpdate
from services import user_service

router = APIRouter(prefix="/users",
                   tags=["Users"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[UserRead],
            summary="Get all Users")
async def get_all(*,
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
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new User

        no parameters required.
    """
    Authorize.jwt_required()
    user = db.query(User).filter(
        User.user_id==Authorize.get_jwt_subject()
    ).first()
    if user is not None:
        return user
    return user_service.create(db, {"user_id": Authorize.get_jwt_subject()})


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=UserRead,
            summary="Get User by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get User by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return user_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=UserRead,
            summary="Update User")
async def update(*,
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
        db,
        db_obj=user_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete User")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete User

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    user_service.remove(db, str(id))

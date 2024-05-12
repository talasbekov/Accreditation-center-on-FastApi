from typing import List

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import HTMLResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db, configs

from schemas import UserRead, UserUpdate, UserCreate
from services import user_service
router = APIRouter(
    prefix="/users", tags=["Users"]
)


@router.get(
    "",
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
    summary="Get User's data",
    response_class=HTMLResponse
)
async def get_data_of_user(
    *, request: Request, Authorize: AuthJWT = Depends()
):
    """
    Get User by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    user = Authorize.get_jwt_subject()
    user_email = Authorize.get_raw_jwt()['email']
    print(user_email)
    return configs.templates.TemplateResponse("base.html",
                                              {"request": request, "user": user, "user_email": user_email})


@router.put(
    "/{id}/",
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

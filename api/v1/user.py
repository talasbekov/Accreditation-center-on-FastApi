from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_jwt import JwtAccessBearer
from sqlalchemy.orm import Session

from core import get_db, configs
from schemas import UserRead, UserUpdate, UserCreate
from services import user_service

# Инициализируем JwtAccessBearer с секретным ключом
auth = JwtAccessBearer(secret_key=configs.SECRET_KEY)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get(
    "",
    response_model=List[UserRead],
    summary="Get all Users",
)
async def get_all(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    credentials=Depends(auth)
):
    """
    Get all Users
    """
    # Доступ к claims токена при необходимости через credentials
    return user_service.get_multi(db, skip, limit)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
    summary="Create User",
)
async def create(
    body: UserCreate,
    db: Session = Depends(get_db),
    credentials=Depends(auth)
):
    """
    Create User

    - **name**: required
    """
    return user_service.create(db, body)

@router.get(
    "/{id}/",
    response_model=UserRead,
    summary="Get User by id",
)
async def get_by_id(
    id: str,
    db: Session = Depends(get_db),
    credentials=Depends(auth)
):
    """
    Get User by id

    - **id**: String - required.
    """
    return user_service.get_by_id(db, id)

@router.put(
    "/{id}/",
    response_model=UserRead,
    summary="Update User",
)
async def update(
    id: str,
    body: UserUpdate,
    db: Session = Depends(get_db),
    credentials=Depends(auth)
):
    """
    Update User
    """
    user = user_service.get_by_id(db, id)
    return user_service.update(db, db_obj=user, obj_in=body)

@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete User",
)
async def delete(
    id: str,
    db: Session = Depends(get_db),
    credentials=Depends(auth)
):
    """
    Delete User

    - **id**: String - required
    """
    user_service.remove(db, id)

@router.get(
    "/user-role",
    summary="Get User Role",
)
async def get_user_role(
    db: Session = Depends(get_db),
    credentials=Depends(auth)
):
    """
    Get the role of the authenticated user.
    """
    # Получаем user_id из claims токена
    user_id = credentials["sub"]
    print(user_id, "user_id")

    return user_service.get_user_role(db, user_id)

from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
import pandas as pd
from core import get_db
from models.accr import City

from schemas import CityRead, CityUpdate, CityCreate
from services import city_service

router = APIRouter(
    prefix="/cities", tags=["Cities"], dependencies=[Depends(HTTPBearer())]
)


@router.get(
    "",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[CityRead],
    summary="Get all Cities",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Citys

    """
    Authorize.jwt_required()
    return city_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(HTTPBearer())],
    response_model=CityRead,
    summary="Create City",
)
async def create(
    *, db: Session = Depends(get_db), body: CityCreate, Authorize: AuthJWT = Depends()
):
    """
    Create City

    - **name**: required
    """
    Authorize.jwt_required()
    return city_service.create(db, body)


@router.get(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=CityRead,
    summary="Get City by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Get City by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return city_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=CityRead,
    summary="Update City",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: CityUpdate,
    Authorize: AuthJWT = Depends()
):
    """
    Update City

    """
    Authorize.jwt_required()
    return city_service.update(
        db, db_obj=city_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(HTTPBearer())],
    summary="Delete City",
)
async def delete(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Delete City

    - **id**: UUId - required
    """
    Authorize.jwt_required()
    city_service.remove(db, str(id))


@router.post("/load_cities")
async def load_cities(db: Session = Depends(get_db)):
    # Загрузить файл CSV с указанием разделителя
    file_path = "./docs/cities.csv"
    df = pd.read_csv(file_path, sep=";", usecols=[0, 3], names=["city_id", "name"], dtype={"city_id": int, "name": str})

    # Преобразование city_id в стандартный int
    df["city_id"] = df["city_id"].astype(int)

    # Пройтись по строкам и добавить данные в базу данных
    for _, row in df.iterrows():
        city_id = int(row["city_id"])
        city_name = row["name"]

        # Проверка на существование города перед добавлением
        existing_city = db.query(City).filter(City.id == city_id).first()
        if not existing_city:
            new_city = City(
                id=city_id,
                name=city_name
            )
            db.add(new_city)

    # Сохранить все изменения
    db.commit()

    return {"status": "success", "message": "Cities loaded successfully"}

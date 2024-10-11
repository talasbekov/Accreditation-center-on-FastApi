import os
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
import pandas as pd
from core import get_db
from models.accr import Country

from schemas import CountryRead, CountryUpdate, CountryCreate
from services import country_service

router = APIRouter(
    prefix="/countries", tags=["Countrys"], dependencies=[Depends(HTTPBearer())]
)


@router.get(
    "",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[CountryRead],
    summary="Get all Countrys",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
    Get all Countrys

    """
    Authorize.jwt_required()
    return country_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(HTTPBearer())],
    response_model=CountryRead,
    summary="Create Country",
)
async def create(
    *,
    db: Session = Depends(get_db),
    body: CountryCreate,
    Authorize: AuthJWT = Depends()
):
    """
    Create Country

    - **name**: required
    """
    Authorize.jwt_required()
    return country_service.create(db, body)


@router.get(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=CountryRead,
    summary="Get Country by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Get Country by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return country_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=CountryRead,
    summary="Update Country",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: CountryUpdate,
    Authorize: AuthJWT = Depends()
):
    """
    Update Country

    """
    Authorize.jwt_required()
    return country_service.update(
        db, db_obj=country_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(HTTPBearer())],
    summary="Delete Country",
)
async def delete(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Delete Country

    - **id**: UUId - required
    """
    Authorize.jwt_required()
    country_service.remove(db, str(id))


@router.post("/load_countries")
async def load_countries(db: Session = Depends(get_db)):
    # Укажите абсолютный путь к файлу
    # file_path = "/app/api/v1/docs/countries.csv"  # Замените на абсолютный путь, если требуется
    file_path = "./docs/countries.csv"

    # Проверяем, существует ли файл
    if os.path.exists(file_path):
        try:
            # Считываем CSV файл, выбираем только нужные колонки
            df = pd.read_csv(file_path, usecols=[0, 3], names=["country_id", "name"],
                             dtype={"country_id": int, "name": str})

            # Преобразуем country_id в int для совместимости
            df["country_id"] = df["country_id"].astype(int)

            # Проходим по строкам и добавляем данные в базу данных
            for _, row in df.iterrows():
                country_id = int(row["country_id"])
                country_name = row["name"]

                # Проверяем на существование страны перед добавлением
                existing_country = db.query(Country).filter(Country.id == country_id).first()
                if not existing_country:
                    new_country = Country(
                        id=country_id,
                        name=country_name
                    )
                    db.add(new_country)

            # Сохраняем все изменения
            db.commit()
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            return {"status": "error", "message": f"Ошибка при загрузке файла: {e}"}
    else:
        current_dir = os.getcwd()
        print(f"Файл не найден по пути: {file_path} в текущей директории {current_dir}")
        return {"status": "error", "message": f"Файл не найден по пути: {file_path}"}

    return {"status": "success", "message": "Countries loaded successfully"}


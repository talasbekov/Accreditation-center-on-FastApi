import os
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
import pandas as pd
from core import get_db

from models.accr import DocumentType
from schemas import DocumentTypeRead, DocumentTypeUpdate, DocumentTypeCreate
from services import document_service

router = APIRouter(
    prefix="/documents", tags=["DocumentTypes"], dependencies=[Depends(HTTPBearer())]
)


@router.get(
    "",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[DocumentTypeRead],
    summary="Get all DocumentTypes",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    Authorize: AuthJWT = Depends()
):
    """
    Get all DocumentTypes

    """
    Authorize.jwt_required()
    return document_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(HTTPBearer())],
    response_model=DocumentTypeRead,
    summary="Create DocumentType",
)
async def create(
    *,
    db: Session = Depends(get_db),
    body: DocumentTypeCreate,
    Authorize: AuthJWT = Depends()
):
    """
    Create DocumentType

    - **name**: required
    """
    Authorize.jwt_required()
    return document_service.create(db, body)


@router.get(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=DocumentTypeRead,
    summary="Get DocumentType by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Get DocumentType by id

    - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return document_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=DocumentTypeRead,
    summary="Update DocumentType",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: DocumentTypeUpdate,
    Authorize: AuthJWT = Depends()
):
    """
    Update DocumentType

    """
    Authorize.jwt_required()
    return document_service.update(
        db, db_obj=document_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(HTTPBearer())],
    summary="Delete DocumentType",
)
async def delete(
    *, db: Session = Depends(get_db), id: str, Authorize: AuthJWT = Depends()
):
    """
    Delete DocumentType

    - **id**: UUId - required
    """
    Authorize.jwt_required()
    document_service.remove(db, str(id))


@router.post("/load_documents")
async def load_documents(db: Session = Depends(get_db)):
    # Укажите абсолютный путь к файлу
    file_path = "/app/api/v1/docs/docs.csv"  # Убедитесь, что это правильный путь к файлу

    # Проверка существования файла
    if os.path.exists(file_path):
        try:
            # Загружаем CSV-файл с нужными колонками
            df = pd.read_csv(file_path, sep=";", usecols=[0, 3], names=["doc_id", "name"],
                             dtype={"doc_id": int, "name": str})

            # Преобразуем doc_id в int для совместимости
            df["doc_id"] = df["doc_id"].astype(int)

            # Проходим по строкам и добавляем данные в базу данных
            for _, row in df.iterrows():
                doc_id = int(row["doc_id"])
                doc_name = row["name"]

                # Проверка на существование документа перед добавлением
                existing_document = db.query(DocumentType).filter(DocumentType.id == doc_id).first()
                if not existing_document:
                    new_document = DocumentType(
                        id=doc_id,
                        name=doc_name
                    )
                    db.add(new_document)

            # Сохраняем все изменения
            db.commit()
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            return {"status": "error", "message": f"Ошибка при загрузке файла: {e}"}
    else:
        current_dir = os.getcwd()
        print(f"Файл не найден по пути: {file_path} в текущей директории {current_dir}")
        return {"status": "error", "message": f"Файл не найден по пути: {file_path}"}

    return {"status": "success", "message": "Documents loaded successfully"}


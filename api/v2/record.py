from typing import List

from fastapi import APIRouter, Depends, status, Response

from sqlalchemy.orm import Session

from core import get_db

from schemas import RecordRead, RecordUpdate, RecordCreate
from services import record_service

router = APIRouter(prefix="/records", tags=["Records"])


@router.get(
    "",
    response_model=List[RecordRead],
    summary="Get all Records",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all Records

    """

    return record_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=RecordRead,
    summary="Create Position",
)
async def create(
    *,
    db: Session = Depends(get_db),
    body: RecordCreate,
):
    """
    Create Record

    - **name**: required
    """

    return record_service.create(db, body)


@router.get(
    "/{id}/",
    response_model=RecordRead,
    summary="Get Record by id",
)
async def get_by_id(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Get Record by id

    - **id**: UUID - required.
    """

    return record_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    response_model=RecordRead,
    summary="Update Record",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: RecordUpdate,
):
    """
    Update Record

    """

    return record_service.update(
        db, db_obj=record_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Record",
)
async def delete(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Delete Record

    - **id**: UUId - required
    """

    record_service.remove(db, str(id))


@router.get("/department/directorate/count", response_model=List[dict])
def get_employer_count_by_directorate(db: Session = Depends(get_db)):
    """
    Расход сотрудников всего департамента
    """
    return record_service.get_count_state(db)


# FastAPI эндпоинт для выгрузки документа
@router.get("/download-word")
def download_word_report(db: Session = Depends(get_db)):
    # Получаем данные
    recs = record_service.get_count_state(db)

    # Создаем Word документ
    word_file = record_service.create_word_report_from_template(recs)

    # Отправляем документ как файл
    return Response(content=word_file.read(),
                    media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    headers={"Content-Disposition": "attachment; filename=report.docx"})

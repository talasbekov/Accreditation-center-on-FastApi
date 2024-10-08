from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer

from sqlalchemy.orm import Session

from core import get_db

from schemas import EmployerRead, EmployerUpdate, EmployerCreate
from services import employer_service

router = APIRouter(prefix="/employers", tags=["Employers"], dependencies=[Depends(HTTPBearer())])


@router.get(
    "",
    dependencies=[Depends(HTTPBearer())],
    response_model=List[EmployerRead],
    summary="Get all Employers",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all Employers

    """

    return employer_service.get_multi(db, skip, limit)


@router.post(
    "",
    dependencies=[Depends(HTTPBearer())],
    status_code=status.HTTP_201_CREATED,
    response_model=EmployerRead,
    summary="Create Position",
)
async def create(
    *,
    db: Session = Depends(get_db),
    body: EmployerCreate,
):
    """
    Create Employer

    - **name**: required
    """

    return employer_service.create(db, body)


@router.get(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=EmployerRead,
    summary="Get Employer by id",
)
async def get_by_id(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Get Employer by id

    - **id**: UUID - required.
    """

    return employer_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    response_model=EmployerRead,
    summary="Update Employer",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: EmployerUpdate,
):
    """
    Update Employer

    """

    return employer_service.update(
        db, db_obj=employer_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    dependencies=[Depends(HTTPBearer())],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Employer",
)
async def delete(
    *,
    db: Session = Depends(get_db),
    id: str,
):
    """
    Delete Employer

    - **id**: UUId - required
    """

    employer_service.remove(db, str(id))

#
# # Функция для автоматического возврата статуса к "в строю"
# def revert_status(worker_id: int, db: Session):
#     # Находим статус по ID
#     employer = db.query(Employer).filter(Employer.id == worker_id).first()
#     if employer:
#         # Устанавливаем статус на "в строю"
#         in_service_status = db.query(Status).filter(Status.name == "в строю").first()
#         employer.status_id = in_service_status.id
#         db.commit()
#
#
# @app.post("/employer/{worker_id}/set_status")
# def set_status(
#         worker_id: int,
#         status_name: str,
#         duration_days: Optional[int] = None,
#         db: Session = Depends(get_db),
#         background_tasks: BackgroundTasks = Depends()
# ):
#     # Проверка, существует ли работник
#     employer = db.query(Employer).filter(Employer.id == worker_id).first()
#     if not employer:
#         raise HTTPException(status_code=404, detail="Worker not found")
#
#     # Поиск статуса по имени
#     status = db.query(Status).filter(Status.name == status_name).first()
#     if not status:
#         raise HTTPException(status_code=404, detail="Status not found")
#
#     # Установка нового статуса
#     employer.status_id = status.id
#
#     # Если указана продолжительность, устанавливаем даты начала и окончания
#     if duration_days:
#         status.start_date = datetime.now().date()
#         status.end_date = status.start_date + timedelta(days=duration_days)
#
#         # Запуск фоновой задачи на возврат к "в строю"
#         background_tasks.add_task(revert_status, worker_id=worker_id, db=db)
#
#     db.commit()
#     return {"message": "Status updated successfully"}
#
#
# # Инициализация статуса по умолчанию для новых работников
# @app.post("/employer/{worker_id}/set_default_status")
# def set_default_status(worker_id: int, db: Session = Depends(get_db)):
#     employer = db.query(Employer).filter(Employer.id == worker_id).first()
#     if not employer:
#         raise HTTPException(status_code=404, detail="Worker not found")
#
#     # Поиск статуса по умолчанию "в строю"
#     default_status = db.query(Status).filter(Status.name == "в строю").first()
#     if not default_status:
#         raise HTTPException(status_code=404, detail="Default status 'в строю' not found")
#
#     employer.status_id = default_status.id
#     db.commit()
#     return {"message": "Default status set successfully"}
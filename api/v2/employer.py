from typing import List

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from core import get_db

from schemas import EmployerRead, EmployerUpdate, EmployerCreate
from services import employer_service

router = APIRouter(
    prefix="/employers", tags=["Employers"]
)


@router.get(
    "",
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
    response_model=EmployerRead,
    summary="Get Employer by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str,
):
    """
    Get Employer by id

    - **id**: UUID - required.
    """

    return employer_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
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
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Employer",
)
async def delete(
    *, db: Session = Depends(get_db), id: str,
):
    """
    Delete Employer

    - **id**: UUId - required
    """

    employer_service.remove(db, str(id))

@router.get(
    "",
    response_model=List[EmployerRead],
    summary="Get all Employers",
)
async def get_all_emp_by_state(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,

):
    """
    Get all Employers
    """

    return employer_service.get_multi(db, skip, limit)


@router.get("/state/count", response_model=int)
def get_employer_count_by_state():
    """
    Количество сотрудников по штату всего департамента
    """
    return employer_service.get_count_emp_by_state()


@router.get("/list/count", response_model=int)
def get_employer_count_by_list(db: Session = Depends(get_db)):
    """
    Количество сотрудников по списку всего департамента
    """
    return employer_service.get_count_emp_by_list(db)


@router.get("/vacant/count", response_model=int)
def get_vacant_employer_count(db: Session = Depends(get_db)):
    """
    Количество вакантных мест в департаменте
    """
    return employer_service.get_count_vacant(db)


@router.get("/status/count", response_model=int)
def get_employer_count_by_status(status: str, db: Session = Depends(get_db)):
    """
    Количество сотрудников по статусу всего департамента
    """
    return employer_service.get_count_emp_by_status(db, status)


@router.get("/in-service/count", response_model=int)
def get_employer_count_in_service(db: Session = Depends(get_db)):
    """
    Количество сотрудников которые в строю всего департамента
    """
    return employer_service.get_count_emp_in_service(db)


@router.get("/status", response_model=List[EmployerRead])
def get_employers_by_status(status: str, db: Session = Depends(get_db)):
    """
    Все сотрудники по статусу, например: на больничном, и т.д.
    """
    return employer_service.get_emp_by_status(db, status)


@router.get("/directorate/{record_id}/state/count", response_model=int)
def get_directorate_employer_count_by_state(record_id: int, db: Session = Depends(get_db)):
    """
    Количество сотрудников по штату в управлении
    """
    return employer_service.get_count_emp_by_state_from_directorate(db, record_id)


@router.get("/directorate/{record_id}/list/count", response_model=int)
def get_directorate_employer_count_by_list(record_id: int, db: Session = Depends(get_db)):
    """
    Количество сотрудников по списку в управлении
    """
    return employer_service.get_count_emp_by_list_from_directorate(db, record_id)


@router.get("/directorate/{record_id}/vacant/count", response_model=int)
def get_vacant_employer_count_in_directorate(record_id: int, db: Session = Depends(get_db)):
    """
    Количество вакантных мест в управлении
    """
    return employer_service.get_count_vacant_in_directorate(db, record_id)


@router.get("/directorate/{record_id}/status", response_model=List[EmployerRead])
def get_employers_by_status_from_directorate(record_id: int, status: str, db: Session = Depends(get_db)):
    """
    Все сотрудники по статусу в управлении
    """
    return employer_service.get_emp_by_status_from_directorate(db, status, record_id)

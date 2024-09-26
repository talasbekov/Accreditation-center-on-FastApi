from typing import List

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from core import get_db

from schemas import EmployerRead, EmployerUpdate, EmployerCreate
from services import employer_service

router = APIRouter(prefix="/employers", tags=["Employers"])


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
    *,
    db: Session = Depends(get_db),
    id: str,
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


@router.get("/statuses", response_model=dict)
def get_emp_statuses():
    """
    Все статусы сотрудников со значениями.
    """
    return {
        "IN_SERVICE": "в строю",
        "ON_LEAVE": "в отпуске",
        "ON_SICK_LEAVE": "на больничном",
        "BUSINESS_TRIP": "в командировке",
        "SECONDED_IN": "прикомандирован",
        "SECONDED_OUT": "откомандирован",
        "ON_DUTY": "на дежурстве",
        "AFTER_ON_DUTY": "после дежурства",
        "AT_THE_COMPETITION": "на соревновании",
    }


@router.get("/department/count", response_model=dict)
def get_employer_count_by_department(db: Session = Depends(get_db)):
    """
    Расход сотрудников всего департамента
    """
    return {
        "Количество сотрудников по штату всего департамента": employer_service.get_count_emp_by_state(),
        "Количество сотрудников по списку всего департамента": employer_service.get_count_emp_by_list(
            db
        ),
        "Количество вакантных мест в департаменте": employer_service.get_count_vacant(
            db
        ),
        "Количество сотрудников которые в строю всего департамента": employer_service.get_count_emp_in_service(
            db
        ),
    }


@router.get("/department/{record_id}_directorate/count", response_model=dict)
def get_employer_count_by_directorate(record_id: int, db: Session = Depends(get_db)):
    """
    Расход сотрудников за одно управление
    """
    return {
        "Количество сотрудников по штату в управлении": employer_service.get_count_emp_by_state_from_directorate(
            db, record_id
        ),
        "Количество сотрудников по списку в управлении": employer_service.get_count_emp_by_list_from_directorate(
            db, record_id
        ),
        "Количество сотрудников которые в строю в управлении": employer_service.get_count_emp_in_service_from_directorate(
            db, record_id
        ),
        "Количество вакантных мест в управлении": employer_service.get_count_vacant_in_directorate(
            db, record_id
        ),
    }


@router.get("/department/by_status", response_model=dict)
def get_employers_by_status(status: str, db: Session = Depends(get_db)):
    """
    Все сотрудники по статусу, например: на больничном, и т.д.
    """
    return {
        "Количество сотрудников по статусу всего департамента": employer_service.get_count_emp_by_status(
            db, status
        ),
        "Все сотрудники по статусу, например: на больничном, и т.д.": employer_service.get_emp_by_status(
            db, status
        ),
    }


@router.get("department/{record_id}_directorate/status", response_model=dict)
def get_employers_by_status_from_directorate(
    record_id: int, status: str, db: Session = Depends(get_db)
):
    """
    Все сотрудники по статусу в управлении
    """

    return {
        "Количество сотрудников по статусу в управлении": employer_service.get_count_emp_by_all_status_from_directorate(
            db, record_id
        ),
        "Количество сотрудников по каждому статусу в управлении": employer_service.get_count_emp_by_status_from_directorate(
            db, status, record_id
        ),
        "Все сотрудники по статусу, например: на больничном, и т.д. в управлении": employer_service.get_emp_by_status_from_directorate(
            db, status, record_id
        ),
    }

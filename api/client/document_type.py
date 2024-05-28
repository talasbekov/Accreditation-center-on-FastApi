from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core import get_db

from schemas import DocumentTypeRead, DocumentTypeUpdate, DocumentTypeCreate
from services import document_service

router = APIRouter(
    prefix="/documents", tags=["DocumentTypes"]
)


@router.get(
    "",
    response_model=List[DocumentTypeRead],
    summary="Get all DocumentTypes",
)
async def get_all(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,

):
    """
    Get all DocumentTypes

    """

    return document_service.get_multi(db, skip, limit)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=DocumentTypeRead,
    summary="Create DocumentType",
)
async def create(
    *,
    db: Session = Depends(get_db),
    body: DocumentTypeCreate,

):
    """
    Create DocumentType

    - **name**: required
    """

    return document_service.create(db, body)


@router.get(
    "/{id}/",
    response_model=DocumentTypeRead,
    summary="Get DocumentType by id",
)
async def get_by_id(
    *, db: Session = Depends(get_db), id: str,
):
    """
    Get DocumentType by id

    - **id**: UUID - required.
    """

    return document_service.get_by_id(db, str(id))


@router.put(
    "/{id}/",
    response_model=DocumentTypeRead,
    summary="Update DocumentType",
)
async def update(
    *,
    db: Session = Depends(get_db),
    id: str,
    body: DocumentTypeUpdate,

):
    """
    Update DocumentType

    """

    return document_service.update(
        db, db_obj=document_service.get_by_id(db, str(id)), obj_in=body
    )


@router.delete(
    "/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete DocumentType",
)
async def delete(
    *, db: Session = Depends(get_db), id: str,
):
    """
    Delete DocumentType

    - **id**: UUId - required
    """

    document_service.remove(db, str(id))

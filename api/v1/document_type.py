from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from core import get_db
from models import DocumentType

from schemas import DocumentTypeRead, DocumentTypeUpdate
from services import document_service

router = APIRouter(prefix="/documents",
                   tags=["DocumentTypes"], dependencies=[Depends(HTTPBearer())])


@router.get("", dependencies=[Depends(HTTPBearer())],
            response_model=List[DocumentTypeRead],
            summary="Get all DocumentTypes")
async def get_all(*,
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


@router.post("", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(HTTPBearer())],
             response_model=DocumentTypeRead,
             summary="Create")
async def create(*,
                 db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Create new DocumentType

        no parameters required.
    """
    Authorize.jwt_required()
    documentType = db.query(DocumentType).filter(
        DocumentType.user_id==Authorize.get_jwt_subject()
    ).first()
    if documentType is not None:
        return documentType
    return document_service.create(db, {"user_id": Authorize.get_jwt_subject()})


@router.get("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DocumentTypeRead,
            summary="Get DocumentType by id")
async def get_by_id(*,
                    db: Session = Depends(get_db),
                    id: str,
                    Authorize: AuthJWT = Depends()
                    ):
    """
        Get DocumentType by id

        - **id**: UUID - required.
    """
    Authorize.jwt_required()
    return document_service.get_by_id(db, str(id))


@router.put("/{id}/", dependencies=[Depends(HTTPBearer())],
            response_model=DocumentTypeRead,
            summary="Update DocumentType")
async def update(*,
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
        db,
        db_obj=document_service.get_by_id(db, str(id)),
        obj_in=body)


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(HTTPBearer())],
               summary="Delete DocumentType")
async def delete(*,
                 db: Session = Depends(get_db),
                 id: str,
                 Authorize: AuthJWT = Depends()
                 ):
    """
        Delete DocumentType

        - **id**: UUId - required
    """
    Authorize.jwt_required()
    document_service.remove(db, str(id))

from typing import Optional
from sqlalchemy.orm import Session
from models import (
    DocumentType,
)  # Предполагается, что у вас есть модель DocumentType в models.py
from schemas import (
    DocumentTypeCreate,
    DocumentTypeUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class DocumentTypeService(
    ServiceBase[DocumentType, DocumentTypeCreate, DocumentTypeUpdate]
):

    def get_by_name(self, db: Session, name: str) -> Optional[DocumentType]:
        return db.query(DocumentType).filter(DocumentType.name == name).first()


document_service = DocumentTypeService(DocumentType)

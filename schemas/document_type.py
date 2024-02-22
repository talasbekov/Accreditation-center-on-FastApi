from typing import Optional
from schemas import ReadNamedModel


class DocumentTypeBase(ReadNamedModel):
    doc_code: Optional[str]


class DocumentTypeCreate(DocumentTypeBase):
    pass


class DocumentTypeUpdate(DocumentTypeBase):
    pass


class DocumentTypeRead(DocumentTypeBase):
    pass

from typing import Optional
from schemas import ReadNamedModel, NamedModel


class DocumentTypeBase(NamedModel):
    doc_code: Optional[str]


class DocumentTypeCreate(DocumentTypeBase):
    pass


class DocumentTypeUpdate(DocumentTypeBase):
    pass


class DocumentTypeRead(DocumentTypeBase, ReadNamedModel):
    pass

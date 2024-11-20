from typing import Optional
from schemas import ReadNamedModel, NamedModel, NamesModel


class DocumentTypeBase(NamedModel):
    doc_code: Optional[str]


class DocumentTypeCreate(DocumentTypeBase):
    id: int
    pass


class DocumentTypeUpdate(DocumentTypeBase):
    pass


class DocumentTypeRead(DocumentTypeBase, ReadNamedModel):
    pass


class GovDocumentTypeRead(NamesModel):
    pass

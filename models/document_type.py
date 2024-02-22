from sqlalchemy import Column, String
from models import NamedModel


# Определите ваши модели здесь
class DocumentType(NamedModel):
    __tablename__ = "document_types"

    doc_code = Column(String(20), unique=True)

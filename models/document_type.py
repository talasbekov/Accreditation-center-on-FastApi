from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import NamedModel


# Определите ваши модели здесь
class DocumentType(NamedModel):
    __tablename__ = "document_types"

    doc_code = Column(String(20), unique=True)

    attendees = relationship("Attendee", back_populates="document_types")

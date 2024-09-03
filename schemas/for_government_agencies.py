from typing import List

from schemas import Model
from schemas.country import GovCountryRead
from schemas.document_type import GovDocumentTypeRead
from schemas.event import GovEventRead


class GovAttendeeRead(Model):
    events: List[GovEventRead]
    countries: List[GovCountryRead]
    doc_types: List[GovDocumentTypeRead]

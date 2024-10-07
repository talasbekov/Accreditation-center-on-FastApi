from typing import List

from schemas import Model
from schemas.accr.country import GovCountryRead
from schemas.accr import GovDocumentTypeRead
from schemas.accr.event import GovEventRead


class GovAttendeeRead(Model):
    events: List[GovEventRead]
    countries: List[GovCountryRead]
    doc_types: List[GovDocumentTypeRead]

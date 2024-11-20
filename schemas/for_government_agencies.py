from typing import List

from schemas import Model, GovCountryRead, GovDocumentTypeRead, GovEventRead


class GovAttendeeRead(Model):
    events: List[GovEventRead]
    countries: List[GovCountryRead]
    doc_types: List[GovDocumentTypeRead]

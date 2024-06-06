from typing import Optional
from schemas import ReadNamedModel, NamedModel, NamesModel


class CountryBase(NamedModel):
    country_code: Optional[str]
    country_iso: Optional[str]
    cis_flag: Optional[bool]


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class CountryRead(CountryBase, ReadNamedModel):
    pass


class GovCountryRead(NamesModel):
    pass

from typing import Optional
from schemas import ReadNamedModel


class CountryBase(ReadNamedModel):
    country_code: Optional[str]
    country_iso: Optional[str]
    cis_flag: Optional[bool]


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class CountryRead(CountryBase):
    pass

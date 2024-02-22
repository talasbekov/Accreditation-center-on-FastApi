from typing import Optional
from schemas import ReadNamedModel


class CityBase(ReadNamedModel):
    city_code: Optional[str]
    index: Optional[str]


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class CityRead(CityBase):
    pass

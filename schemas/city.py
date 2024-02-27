from typing import Optional
from schemas import ReadNamedModel, NamedModel


class CityBase(NamedModel):
    city_code: Optional[str]
    index: Optional[str]


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class CityRead(CityBase, ReadNamedModel):
    pass

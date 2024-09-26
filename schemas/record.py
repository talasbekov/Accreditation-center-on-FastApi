from typing import Optional

from schemas import EmployerRead, Model


class RecordBase(Model):
    name: Optional[str]
    count_state: Optional[int]
    count_list: Optional[int]
    count_on_leave: Optional[int]
    count_on_sick_leave: Optional[int]
    count_business_trip: Optional[int]
    count_seconded_in: Optional[int]
    count_seconded_out: Optional[int]
    count_on_duty: Optional[int]
    count_after_on_duty: Optional[int]
    count_at_the_competition: Optional[int]


class RecordCreate(RecordBase):
    pass


class RecordUpdate(RecordBase):
    pass


class RecordRead(RecordBase, Model):
    id: int
    count_in_service: Optional[int]
    count_vacant: Optional[int]
    employers: Optional[list[EmployerRead]]

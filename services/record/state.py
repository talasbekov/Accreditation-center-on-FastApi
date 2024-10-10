from typing import Optional
from sqlalchemy.orm import Session

from models import State
from schemas import (
    StateCreate,
    StateUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий

from services.base import ServiceBase


class StateService(ServiceBase[State, StateCreate, StateUpdate]):

    def get_by_employer_id(self, db: Session, employer_id: int) -> Optional[State]:
        return db.query(State).filter(State.employer_id == employer_id).first()


state_service = StateService(State)

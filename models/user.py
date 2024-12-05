from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from models import Model, user_event_association, user_roles


class User(Model):
    __tablename__ = "users"

    email = Column(String(150), nullable=True, unique=True)
    password = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    workplace = Column(String(128))
    iin = Column(Integer, unique=True)
    phone_number = Column(String(20), nullable=True)
    admin = Column(Boolean, default=False)
    last_signed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    login_count = Column(Integer, default=0)

    requests = relationship("Request", back_populates="users")
    events = relationship(
        "Event", secondary=user_event_association, back_populates="users"
    )

    # Import Role inside the class to avoid circular import
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    roles = relationship(
        'Role',
        secondary=user_roles,
        back_populates='users'
    )

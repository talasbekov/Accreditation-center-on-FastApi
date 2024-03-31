from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from models import NamedModel
from models.association import user_event_association


# Определите ваши модели здесь
class User(NamedModel):
    __tablename__ = "users"

    email = Column(String(150), nullable=True, unique=True)
    password = Column(String(255), nullable=True)
    workplace = Column(String(128))
    iin = Column(Integer, unique=True)
    phone_number = Column(String(20), nullable=True)
    is_accreditator = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    last_signed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    login_count = Column(Integer, default=0)

    requests = relationship("Request", back_populates="users")
    events = relationship(
        "Event", secondary=user_event_association, back_populates="users"
    )
    permissions = relationship("Permission", back_populates="user")

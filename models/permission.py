from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base  # Import your declarative base

# Import association tables
from .association import role_permissions

class Permission(Base):
    __tablename__ = "permissions"

    name = Column(String(255), nullable=False, unique=True)

    roles = relationship(
        'Role',
        secondary=role_permissions,
        back_populates='permissions'
    )

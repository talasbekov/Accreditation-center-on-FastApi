from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import Model

# Import association tables
from .association import role_permissions, user_roles

class Role(Model):
    __tablename__ = "roles"

    name = Column(String(255), nullable=False, unique=True)

    permissions = relationship(
        'Permission',
        secondary=role_permissions,
        back_populates='roles'
    )

    users = relationship(
        'User',
        secondary=user_roles,
        back_populates='roles'
    )

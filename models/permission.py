import enum

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from models import NamedModel, Model


class PermissionEnum(str, enum.Enum):
    FULL_ACCESS = 0  # "Полный доступ"
    ATTENDEE_EDITOR = 1  # "Редакторование штатного расписания"
    PERSONAL_PROFILE_EDITOR = 2  # "Редактирование личных дел"


class PermissionType(NamedModel):
    __tablename__ = "permission_types"

    sequence_id = Column(Integer, nullable=True)
    permissions = relationship(
        "Permission", back_populates="type", cascade="all,delete"
    )


class Permission(Model):
    __tablename__ = "permissions"

    user_id = Column(String(), ForeignKey("users.id"))
    user = relationship("User", back_populates="permissions")

    type_id = Column(String(), ForeignKey("permission_types.id"))
    type = relationship("PermissionType", back_populates="permissions")

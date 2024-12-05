from typing import List

from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import Permission
from schemas import PermissionCreate, PermissionUpdate

from services.base import ServiceBase


class PermissionService(ServiceBase[Permission, PermissionCreate, PermissionUpdate]):

    def get_by_id(self, db: Session, id: str):
        permission = super().get(db, id)
        if permission is None:
            raise NotFoundException(detail=f"Permission with id: {id} is not found!")
        return permission

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Permission]:
        permissions = (
            db.query(self.model)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        count = db.query(self.model).count()
        return {"total": count, "objects": permissions}

    # def get_permission_types(self, db: Session, skip: int = 0, limit: int = 100):
    #     return db.query(PermissionType).offset(skip).limit(limit).all()

    # def has_permission(
    #     self,
    #     db: Session,
    #     user_id: str,
    #     role: str,
    #     permissions: list[int],
    #     required_permission: int,
    # ):
    #
    #     # Проверяем, входит ли требуемое разрешение в список разрешений пользователя
    #     if required_permission not in permissions:
    #         raise ForbiddenException("У пользователя нет требуемого разрешения.")
    #
    #     # Ищем тип разрешения по требуемому разрешению
    #     permission_type = (
    #         db.query(PermissionType)
    #         .filter(PermissionType.sequence_id == required_permission)
    #         .first()
    #     )
    #     if not permission_type:
    #         raise NotFoundException("Тип разрешения не найдено.")
    #
    #     # Проверяем, есть ли у пользователя конкретное разрешение с учётом его роли
    #     permission = (
    #         db.query(self.model)
    #         .filter(
    #             self.model.type_id == permission_type.id, self.model.user_id == user_id
    #         )
    #         .first()
    #     )
    #
    #     return (
    #         permission is not None
    #     )  # Возвращает True, если разрешение найдено, иначе False

    def get_permissions_by_user(self, db: Session, user_id: str):
        permissions = db.query(self.model).filter(self.model.user_id == user_id).all()
        return permissions

    def get_permissions_sequence_id_by_user(self, db: Session, user_id: str):
        permissions = db.query(self.model).filter(self.model.user_id == user_id).all()
        permission_list = []
        for permission in permissions:
            permission_list.append(permission.type.sequence_id)
        update_permission_list = []
        for i in set(permission_list):
            update_permission_list.append(i)
        return update_permission_list


permission_service = PermissionService(Permission)

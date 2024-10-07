from typing import List, Optional

from schemas import Model, NamedModel, ReadModel, ReadNamedModel, UserRead


class PermissionType(NamedModel):
    sequence_id: Optional[int]
    pass


class PermissionTypeRead(ReadNamedModel):
    sequence_id: Optional[int]
    pass


class PermissionBase(Model):
    type_id: str
    user_id: str


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class UserPermission(NamedModel):
    user_id: str
    permission_ids: List[PermissionTypeRead]


class PermissionRead(PermissionBase, ReadModel):
    type: PermissionTypeRead
    user: UserRead

    class Config:
        orm_mode = True


class PermissionPaginationRead(Model):
    total: Optional[int]
    objects: Optional[List[PermissionRead]]

from typing import Optional



from schemas import ReadNamedModel, NamedModel


class FaceBlackListBase(NamedModel):
    photo_path: Optional[str]
    reason: Optional[str]
    description: Optional[str]


class FaceBlackListCreate(FaceBlackListBase):
    pass


class FaceBlackListUpdate(FaceBlackListBase):
    pass


class FaceBlackListRead(FaceBlackListBase, ReadNamedModel):
    pass

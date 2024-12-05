import asyncio

import face_recognition
from fastapi import HTTPException
from io import BytesIO
from pathlib import Path
from typing import Optional, Type

from PIL import Image
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models import FaceBlackList  # Предполагается, что у вас есть модель FaceBlackList в models.py
from schemas import (
    FaceBlackListCreate,
    FaceBlackListUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class FaceBlackListService(ServiceBase[FaceBlackList, FaceBlackListCreate, FaceBlackListUpdate]):

    def get_by_name(self, db: Session, name: str) -> Optional[FaceBlackList]:
        return db.query(FaceBlackList).filter(FaceBlackList.name == name).first()

    async def upload_face_photo(self, db: Session, face_id: str, photo: UploadFile) -> Type[FaceBlackList]:
        face = db.query(FaceBlackList).filter(FaceBlackList.id == face_id).first()
        if not face:
            raise HTTPException(status_code=404, detail="Face not found")

        file_location = Path(f"media/face_photos/{face_id}.jpg")
        file_location.parent.mkdir(parents=True, exist_ok=True)

        try:
            file_contents = await photo.read()
            loop = asyncio.get_event_loop()
            image = await loop.run_in_executor(None, Image.open, BytesIO(file_contents))
            if image.mode == "RGBA":
                image = image.convert("RGB")
            await loop.run_in_executor(None, image.save, file_location, "JPEG")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")

        photo_location = Path(f"face_photos/{face_id}.jpg")
        face.face_photo = str(photo_location)
        db.commit()
        db.refresh(face)
        return face

    def encode_faces_from_blacklist(self, db: Session):
        faces = db.query(FaceBlackList).all()
        photo_paths = [face.photo_path for face in faces]
        encodings = []

        for path in photo_paths:
            try:
                image = face_recognition.load_image_file(path)
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    encodings.append(encoding[0])
            except Exception as e:
                print(f"Failed to encode face from {path}: {str(e)}")

        return encodings


face_service = FaceBlackListService(FaceBlackList)

from sqlalchemy import Column, Text

from models import NamedModel


# Определите ваши модели здесь
class FaceBlackList(NamedModel):
    __tablename__ = "faceblacklists"

    photo_path = Column(Text, nullable=True)  # Путь к фото
    reason = Column(Text, nullable=True)  # Причина в черном списке
    description = Column(Text, nullable=True)  # Описание или заметки

    def __repr__(self):
        return f"<FaceBlackList(id={self.id}, name='{self.name}', photo_path='{self.photo_path}')>"

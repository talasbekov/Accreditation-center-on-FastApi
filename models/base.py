import datetime
from sqlalchemy import TIMESTAMP, Column, String, text, Integer, Boolean, Text

from core import Base

"""
    Этот класс является абстрактным классом сущности,
    который предоставляет следующие столбцы всем унаследованным сущностям:
    - **id** : Integer - первичный ключ таблицы
    - **created_at**: datetime - время создания сущности
    - **updated_at**: datetime - время обновления сущности
"""


class Cloneable:
    def clone(self, **attr):
        new_obj = self.__class__()

        for c in self.__table__.columns:
            if c.name == "namekz":
                setattr(new_obj, "nameKZ", getattr(self, "nameKZ"))
            else:
                setattr(new_obj, c.name, getattr(self, c.name))

        new_obj.__dict__.update(attr)
        new_obj.id = None  # Сброс id, чтобы база данных назначила новый
        new_obj.created_at = datetime.datetime.utcnow()
        new_obj.updated_at = datetime.datetime.utcnow()

        return new_obj



class Model(Base, Cloneable):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.datetime.now,
    )


"""
    Этот класс является абстрактным классом сущности,
    который предоставляет следующие столбцы всем унаследованным сущностям:
    - **name** : str - обязательно
"""


class NamedModel(Model):
    __abstract__ = True

    name = Column(String, nullable=False)
    nameKZ = Column("namekz", String, nullable=True)
    nameEN = Column("nameen", String, nullable=True)


"""
    Этот класс является абстрактным классом сущности, который может быть вложенным.
    Это просто маркер для вложенных классов.
"""


class NestedModel(Model):
    __abstract__ = True


"""
    Этот класс является абстрактным классом сущности, который может быть вложенным.
    Это просто маркер для вложенных классов.
    Единственное отличие между вложенными моделями — **name**
"""


class NamedNestedModel(NamedModel):
    __abstract__ = True


"""
    Этот класс является абстрактным классом сущности,
    который предоставляет следующие столбцы всем унаследованным сущностям:
    - **is_active** : bool - обязательно
"""


class IsActiveModel(Model):
    __abstract__ = True

    is_active = Column(Boolean, nullable=False, default=True)


class TextModel(Model):
    __abstract__ = True

    text = Column(Text, nullable=False)
    textKZ = Column("textkz", Text, nullable=True)
    textEN = Column("texten", Text, nullable=True)

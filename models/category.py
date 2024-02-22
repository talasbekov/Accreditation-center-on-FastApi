from sqlalchemy import Column, String
from models import NamedModel


# Определите ваши модели здесь
class Category(NamedModel):
    __tablename__ = "categories"

    category_code = Column(String(20), unique=True)
    index = Column(String(20))

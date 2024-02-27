from typing import Optional
from schemas import ReadNamedModel, NamedModel


class CategoryBase(NamedModel):
    category_code: Optional[str]
    index: Optional[str]


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryRead(CategoryBase, ReadNamedModel):
    pass

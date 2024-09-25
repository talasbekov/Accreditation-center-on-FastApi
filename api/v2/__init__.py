from fastapi import APIRouter

from .employer import router as emp_router
from .record import router as record_router


router = APIRouter(prefix="/v2")

router.include_router(emp_router)
router.include_router(record_router)

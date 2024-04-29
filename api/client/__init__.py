from fastapi import APIRouter

from .auth import router as auth_router
from .user import router as user_router
from .attendee import router as attendee_router
from .category import router as category_router
from .city import router as city_router
from .country import router as country_router
from .document_type import router as doc_router
from .event import router as event_router
from .request import router as request_router
from .sex import router as sex_router

router = APIRouter(prefix="/client")

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(attendee_router)
router.include_router(category_router)
router.include_router(city_router)
router.include_router(country_router)
router.include_router(doc_router)
router.include_router(event_router)
router.include_router(request_router)
router.include_router(sex_router)

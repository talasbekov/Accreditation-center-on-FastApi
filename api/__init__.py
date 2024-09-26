from fastapi import APIRouter, Request

from .v2 import router as v2_router
from .client import router as client_router


router = APIRouter(prefix="/api")


@client_router.get("/ip")
async def get_ip(request: Request):
    return request.client.host


router.include_router(v2_router)
router.include_router(client_router)

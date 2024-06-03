from fastapi import APIRouter, Request

from .client import router as client_router

router = APIRouter(prefix="/api")


@client_router.get("/ip")
async def get_ip(request: Request):
    return request.client.host


router.include_router(client_router)

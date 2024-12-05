from fastapi import APIRouter, Request

from .v1 import router as v1_router
# from .client import router as client_router


router = APIRouter(prefix="/api")


@v1_router.get("/ip")
async def get_ip(request: Request):
    return request.client.host

# @client_router.get("/ip")
# async def get_ip(request: Request):
#     return request.client.host


router.include_router(v1_router)
# router.include_router(client_router)

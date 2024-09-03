from fastapi import APIRouter, Depends, Request

from fastapi_jwt_auth import AuthJWT

from core import configs

router = APIRouter(prefix="/base")


@router.get("/")
async def get_user_email(request: Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_email = Authorize.get_raw_jwt()["email"]
    return configs.templates.TemplateResponse(
        "base.html", {"request": request, "user_email": user_email}
    )

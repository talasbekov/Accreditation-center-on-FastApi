from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from core import get_db, configs
from schemas import LoginForm, RegistrationForm
from services import auth_service


router = APIRouter(prefix="/auth", tags=["Authorization"])

# Инициализируем JwtAccessBearer с вашим секретным ключом
jwt_bearer = JwtAccessBearer(secret_key=configs.SECRET_KEY)


@router.post("/login", summary="Login")
async def login(form: LoginForm, db: AsyncSession = Depends(get_db)):
    """
    Login to the system.

    - **email**: required and should be a valid email format.
    - **password**: required.
    """
    return await auth_service.login(form, db)


@router.post("/register", summary="Register")
async def register(form: RegistrationForm, db: AsyncSession = Depends(get_db)):
    """
    Register new user to the system.
    """
    return await auth_service.register(form, db)


@router.get("/refresh", summary="Refresh Token")
async def refresh_token(
    credentials: JwtAuthorizationCredentials = Depends(jwt_bearer),
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh the access token using a valid refresh token.
    """
    token_type = credentials.claims.get("token_type")
    if token_type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
        )
    user_id = credentials.subject
    new_access_token = jwt_bearer.create_access_token(
        subject=user_id, expires_delta=timedelta(minutes=15)
    )
    return {"access_token": new_access_token}

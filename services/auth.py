from datetime import timedelta, datetime

from fastapi import HTTPException, status, Request
from fastapi_jwt_auth import AuthJWT
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_403_FORBIDDEN
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core import configs
from exceptions import BadRequestException
from models import User
from schemas import LoginForm, RegistrationForm, UserCreate
from services import user_service, permission_service

from utils import hash_password, verify_password


class AuthService:

    def login(self, form: LoginForm, db: Session, Authorize: AuthJWT):
        user = user_service.get_by_email(db, EmailStr(form.email).lower())
        if not user or not verify_password(form.password, user.password):
            raise BadRequestException(detail="Incorrect email or password!")

        self._set_last_signed_at(db, user)
        access_token, refresh_token = self._generate_tokens(db, Authorize, user)
        return {"access_token": access_token, "refresh_token": refresh_token}

    def register(self, form: RegistrationForm, db: Session):

        if user_service.get_by_email(db, EmailStr(form.email).lower()):
            raise BadRequestException(detail="User with this email already exists!")
        if form.password != form.re_password:
            raise BadRequestException(detail="Password mismatch!")

        user_obj_in = UserCreate(
            email=EmailStr(form.email).lower(),
            name=form.name,
            iin=form.iin,
            password=hash_password(form.password),
            is_admin=False,
        )

        user = user_service.create(db=db, obj_in=user_obj_in)

        return user

    def refresh_token(self, db: Session, Authorize: AuthJWT):
        if not Authorize.get_jwt_subject():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not refresh access token",
            )
        user = user_service.get(db, Authorize.get_jwt_subject())
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The user belonging to this token no longer exist",
            )

        access_token, refresh_token = self._generate_tokens(db, Authorize, user)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def _generate_tokens(self, db: Session, Authorize: AuthJWT, user: User):
        # Получение списка разрешений пользователя
        permissions = permission_service.get_permissions_sequence_id_by_user(
            db, user.id
        )

        # Если у пользователя нет разрешений, устанавливаем пустой список
        if permissions is None:
            permissions = []

        # Определение дополнительных утверждений для токена
        user_claims = {
            "role": str(user.workplace),
            "iin": str(user.iin),
            "permissions": permissions,
        }

        # Создание токена доступа
        access_token = Authorize.create_access_token(
            subject=str(user.id),
            user_claims=user_claims,
            expires_time=timedelta(minutes=configs.ACCESS_TOKEN_EXPIRES_IN),
        )

        # Создание токена обновления
        refresh_token = Authorize.create_refresh_token(
            subject=str(user.id),
            user_claims=user_claims,
            expires_time=timedelta(minutes=configs.REFRESH_TOKEN_EXPIRES_IN),
        )

        return access_token, refresh_token

    def _set_last_signed_at(self, db: Session, user: User):
        user.last_signed_at = datetime.now()

        db.add(user)
        db.flush()


auth_service = AuthService()


class CookieToken:
    def __init__(self):
        self.scheme = HTTPBearer()

    async def __call__(self, request: Request):
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        return credentials


cookie_bearer = CookieToken()

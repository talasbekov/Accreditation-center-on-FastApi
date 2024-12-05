from datetime import timedelta, datetime

from fastapi import HTTPException, status, Depends
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from core import configs
from exceptions import BadRequestException
from models import User
from schemas import LoginForm, RegistrationForm, UserCreate
from services import user_service

from utils import hash_password, verify_password, is_valid_phone_number


# Инициализация JwtAccessBearer с секретным ключом
jwt_bearer = JwtAccessBearer(secret_key=configs.SECRET_KEY)


class AuthService:

    async def login(self, form: LoginForm, db: AsyncSession):
        user = await user_service.get_by_email(db, EmailStr(form.email).lower())
        if not user or not verify_password(form.password, user.password):
            raise BadRequestException(detail="Incorrect email or password!")

        self._set_last_signed_at(db, user)
        access_token, refresh_token = self._generate_tokens(user)
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def register(self, db: AsyncSession, form: RegistrationForm):
        if user_service.get_by_email(db, EmailStr(form.email).lower()):
            raise BadRequestException(
                detail="Пользователь с таким Email-ом уже существует!"
            )
        if user_service.get_by_iin(db, form.iin):
            raise BadRequestException(
                detail="Пользователь с таким ИИН-ом уже существует!"
            )
        if not is_valid_phone_number(form.phone_number):
            raise BadRequestException(
                detail="Неправильно ввели телефонный номер! Попробуйте через +7"
            )
        if form.password != form.re_password:
            raise BadRequestException(detail="Ваши пароли не совпадают!")

        user_obj_in = UserCreate(
            email=EmailStr(form.email).lower(),
            name=form.name,
            workplace=form.workplace,
            phone_number=form.phone_number,
            iin=form.iin,
            admin=form.admin,
            password=hash_password(form.password),
        )
        user = user_service.create(db=db, obj_in=user_obj_in)
        return user

    async def refresh_token(self, db: AsyncSession, credentials: JwtAuthorizationCredentials = Depends(jwt_bearer)):
        token_type = credentials.claims.get("token_type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = credentials.subject
        user = user_service.get(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The user belonging to this token no longer exists"
            )

        access_token, refresh_token = self._generate_tokens(user)
        return {"access_token": access_token, "refresh_token": refresh_token}

    def _generate_tokens(self, user: User):
        # Дополнительные утверждения для токена
        user_claims = {}

        # Создание токена доступа
        access_token = jwt_bearer.create_access_token(
            subject=str(user.id),
            expires_delta=timedelta(minutes=configs.ACCESS_TOKEN_EXPIRES_IN),
            claims=user_claims
        )

        # Создание токена обновления
        refresh_token = jwt_bearer.create_access_token(
            subject=str(user.id),
            expires_delta=timedelta(minutes=configs.REFRESH_TOKEN_EXPIRES_IN),
            claims={"token_type": "refresh", **user_claims}
        )

        return access_token, refresh_token

    def _set_last_signed_at(self, db: AsyncSession, user: User):
        user.last_signed_at = datetime.now()
        db.add(user)
        db.commit()

    # Зависимость для получения текущего пользователя
    async def get_current_user(self, credentials: JwtAuthorizationCredentials = Depends(jwt_bearer), db: AsyncSession = Depends()):
        user_id = credentials.subject
        user = user_service.get(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user


auth_service = AuthService()

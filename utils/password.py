from datetime import timedelta

from fastapi_jwt import JwtAccessBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core import configs
from services import user_service

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Инициализируем JwtAccessBearer с секретным ключом
auth = JwtAccessBearer(secret_key=configs.SECRET_KEY)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def get_access_token_by_user_id(db: Session, user_id: str):
    user = user_service.get_by_id(db, user_id)
    # Передаем дополнительные данные в claims
    access_token = auth.create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(minutes=configs.ACCESS_TOKEN_EXPIRES_IN),
        iin=str(user.iin)
    )
    return access_token


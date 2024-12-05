from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User  # Предполагается, что у вас есть модель User в models.py
from schemas import (
    UserCreate,
    UserUpdate,
)  # Предполагается, что у вас есть схемы создания и обновления событий
from services.base import ServiceBase


class UserService(ServiceBase[User, UserCreate, UserUpdate]):

    async def get_by_email(self, db: AsyncSession, email: str):
        stmt = select(self.model).where(self.model.email == email)
        result = await db.execute(stmt)
        user = result.scalars().first()
        return user

    async def get_by_iin(self, db: AsyncSession, iin: int):
        stmt = select(self.model).where(self.model.iin == iin)
        result = await db.execute(stmt)
        user = result.scalars().first()
        return user

    async def user_login_activity(self, user_id: str, db: AsyncSession):
        stmt = select(self.model).where(self.model.id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if user:
            now = datetime.utcnow()
            if not user.last_login or now.date() > user.last_login.date():
                # Сброс счетчика, если последний логин был в другой день
                user.login_count = 1
            else:
                user.login_count += 1
            user.last_login = now
            # Отмечаем объект как измененный и сохраняем изменения
            db.add(user)
            await db.commit()
            await db.refresh(user)

    async def get_login_count(
        self, user_id: str, start_date: datetime, end_date: datetime, db: AsyncSession
    ) -> int:
        stmt = select(self.model).where(self.model.id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if user and user.last_login and start_date <= user.last_login <= end_date:
            return user.login_count
        return 0

    async def get_user_role(self, db: AsyncSession, user_id: str):
        # Получаем пользователя из базы данных
        user = await self.get_by_id(db, user_id)
        print(user, "user")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Возвращаем роль пользователя
        return {"role": user.workplace}

    # async def assign_role_to_user(self, db: AsyncSession, user_id: int, role_name: str):
    #     stmt_user = select(User).where(User.id == user_id)
    #     result_user = await db.execute(stmt_user)
    #     user = result_user.scalars().first()
    #     stmt_role = select(Role).where(Role.name == role_name)
    #     result_role = await db.execute(stmt_role)
    #     role = result_role.scalars().first()
    #     if role and user and role not in user.roles:
    #         user.roles.append(role)
    #         db.add(user)
    #         await db.commit()
    #         await db.refresh(user)


user_service = UserService(User)

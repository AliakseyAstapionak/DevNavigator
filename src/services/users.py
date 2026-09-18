from database import engine
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserBase
from sqlalchemy import select
from typing import Optional


class UserService:

    @staticmethod
    async def get_user_by_name(username: str, db: AsyncSession)-> Optional[UserBase]:
        query = select(UserBase).where(UserBase.username == username)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create_user(username: str, hashed_pwd: str , db: AsyncSession) -> UserBase:
        new_user = UserBase(username=username, hashed_password=hashed_pwd)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user    

    @staticmethod
    async def get_user_by_id(id: str, db: AsyncSession)-> Optional[UserBase]:
        query = select(UserBase).where(UserBase.id == id)
        result = await db.execute(query)
        return result.scalars().first()
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import VacancySearchSchema, VacancySearchResponseSchema
from typing import Any
from fastapi import Depends
from models import RequestBase
from database import get_db


class RequestService:

    @staticmethod
    async def create_request(user_id: int, request: Any , response: Any , db: AsyncSession) -> RequestBase:
        request_data = request.model_dump(mode="json")
        response_data = response.model_dump(mode='json')

        db_request = RequestBase(user_id=user_id, request=request_data, response=response_data)
        db.add(db_request)
        await db.commit()
        await db.refresh(db_request)

        return db_request
        


from schemas import VacancySearchSchema, VacancySearchResponseSchema
from sqlalchemy.ext.asyncio import AsyncSession


class VacancyService:

    @staticmethod
    async def search_vacancies(searh: VacancySearchSchema, db: AsyncSession) -> VacancySearchResponseSchema:
        ...
from fastapi import APIRouter, Depends, status, HTTPException, Response
from schemas import VacancySearchSchema, VacancySearchResponseSchema
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services import VacancyService


router = APIRouter()




@router.post('/vacancy_search', response_model=VacancySearchResponseSchema, status_code=status.HTTP_200_OK)
async def vacancy_search(search: VacancySearchSchema, db :AsyncSession = Depends(get_db)):
    result = await VacancyService.search_vacancies(search=search, db=db)
    return result

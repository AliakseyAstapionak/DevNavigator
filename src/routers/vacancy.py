from fastapi import APIRouter, Depends, status, HTTPException, Response
from schemas import VacancySearchSchema


router = APIRouter()

@router.post('/vacancy_search')
async def vacancy_search(search: VacancySearchSchema):
    ...
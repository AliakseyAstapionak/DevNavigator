from fastapi import APIRouter, Depends, status
from schemas import VacancySearchSchema, UserPayload, VacancySearchWithUserResponseSchema
from services import VacancyService, RequestService
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from dependences import get_current_user

router = APIRouter()


@router.post("/vacancy_search", response_model=VacancySearchWithUserResponseSchema, status_code=status.HTTP_200_OK)
async def vacancy_search(search: VacancySearchSchema, user: UserPayload = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await VacancyService.search_vacancies(search=search)
    user_id = user.id
    response = await RequestService.create_request(user_id=user_id, request=search, response=result, db=db)

    return {'user': user, 'results': response}
from fastapi import HTTPException, status
from schemas import HHVacancySearchSchema, HHVacancySearchResponseSchema, HHVacancyShortSchema, HHVacancySearchResponseSchema
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

"""
С апреля 2026 года HeadHunter закрыл публичный анонимный доступ к методу поиска вакансий. 
Теперь для работы с API требуется аутентификация. Получить необходимые права могут преимущественно
работодатели и разработчики рекрутинговых сервисов. Для этого нужен подтверждённый 
аккаунт работодателя, а созданное приложение должно пройти модерацию HeadHunter.
"""

HH_API_URL = 'https://api.hh.ru/vacancies'
# hh.ru просит указывать User-Agent с названием приложения и контактом —
# без этого могут прилетать 403 при повышенной нагрузке

HEADERS = {
  "User-Agent": "MyUniqueAppService/1.0 (developer123@gmail.com)"
}


class VacancyService:

    @staticmethod
    async def _built_params(search: HHVacancySearchSchema) -> dict:
        params = search.model_dump(exclude_none=True)
        # only_with_salary=False отправлять не нужно, hh.ru по умолчанию его не ждёт
        if not params.get("only_with_salary"):
            params.pop("only_with_salary", None)
        return params

    @staticmethod
    async def search_vacancies(search: HHVacancySearchSchema, db: AsyncSession) -> HHVacancySearchResponseSchema:
        params = await VacancyService._built_params(search)

        async with httpx.AsyncClient(timeout=10.0, headers=HEADERS) as client:
            try:
                response = await client.get(HH_API_URL, params=params)
                print("hh.ru статус:", response.status_code)
                print("hh.ru тело:", response.text[:500])
                response.raise_for_status()
            except httpx.TimeoutException:
                raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="hh.ru не ответил вовремя, попробуйте позже")
            except httpx.HTTPStatusError as e:
               raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Ошибка при обращении к hh.ru: {e.response.status_code}")
            
        data = response.json()

        items = [
            HHVacancyShortSchema(
                id=item["id"],
                name=item["name"],
                employer_name=item.get("employer", {}).get("name"),
                area_name=item.get("area", {}).get("name"),
                salary_from=item.get("salary", {}).get("from") if item.get("salary") else None,
                salary_to=item.get("salary", {}).get("to") if item.get("salary") else None,
                salary_currency=item.get("salary", {}).get("currency") if item.get("salary") else None,
                published_at=item.get("published_at"),
                alternate_url=item["alternate_url"],
                snippet_requirement=item.get("snippet", {}).get("requirement"),
                snippet_responsibility=item.get("snippet", {}).get("responsibility"),
            )
            for item in data.get("items", [])
        ]

        return HHVacancySearchResponseSchema(
            found=data.get("found", 0),
            pages=data.get("pages", 0),
            page=data.get("page", 0),
            per_page=data.get("per_page", 0),
            items=items,
        )



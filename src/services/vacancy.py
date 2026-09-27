import httpx
from fastapi import HTTPException, status
from schemas.vacancy import VacancySearchSchema, VacancySearchResponseSchema, VacancyShortSchema
from services.utils import get_client

BASE_URL ="https://opendata.trudvsem.ru/api/v1/vacancies"

# Контакты лучше не хранить в коде: задай USER_AGENT в .env

HEADERS = {
    "User-Agent": "DevNavigator/1.0 (astapnok131@gmail.com)"
}

# TODO подумать над тем как удобно вводить регион
class VacancyService:

    @staticmethod
    def _build_params(search: VacancySearchSchema) -> dict:
        """region_code, если он задан, идёт не в query-параметры (?region_code=...), а прямо в URL — в путь /vacancies/region/{region_code}"""
        params = search.model_dump(mode="json", exclude_none=True, exclude={"region_code"})
        return params

    @staticmethod
    def _build_url(search: VacancySearchSchema) -> str:
        # если указан регион — используется отдельный путь /vacancies/region/{code}
        if search.region_code:
            return f"{BASE_URL}/region/{search.region_code}"
        return BASE_URL

    @staticmethod
    async def search_vacancies(search: VacancySearchSchema) -> VacancySearchResponseSchema:
        params = VacancyService._build_params(search)
        url = VacancyService._build_url(search)

        client = await get_client(name='search_vacancies')
        try:
            response = await client.get(url, params=params, headers=HEADERS)
            response.raise_for_status()
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="trudvsem.ru не ответил вовремя, попробуйте позже"
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Ошибка при обращении к trudvsem.ru: {e.response.status_code}"
            )
        except httpx.RequestError:
            # сеть недоступна, сбой DNS, отказ в соединении и т.п.
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Не удалось связаться с trudvsem.ru, попробуйте позже"
            )

        data = response.json()

        meta = data.get("meta", {})
        raw_vacancies = data.get("results", {}).get("vacancies", [])

        items = []
        for entry in raw_vacancies:
            v = entry.get("vacancy", entry)  # на случай, если структура окажется плоской
            items.append(
                VacancyShortSchema(
                    id=str(v.get("id")),
                    name=v.get("job-name") or v.get("name", ""),
                    company_name=v.get("company", {}).get("name") if isinstance(v.get("company"), dict) else None,
                    region_name=v.get("region", {}).get("name") if isinstance(v.get("region"), dict) else None,
                    salary_min=v.get("salary_min"),
                    salary_max=v.get("salary_max"),
                    created_at=v.get("creation-date"),
                    url=v.get("vac_url"),
                )
            )

        return VacancySearchResponseSchema(
            total=meta.get("total", 0),
            limit=meta.get("limit", search.limit),
            offset=meta.get("offset", search.offset),
            items=items,
        )
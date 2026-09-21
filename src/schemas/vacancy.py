from pydantic import BaseModel, Field
from typing import Optional
from schemas.auth import UserPayload
from schemas.request import RequestResponseSchema


class VacancySearchSchema(BaseModel):
    text: str = Field(..., min_length=2, description="Стек/должность, например 'Python разработчик'")
    region_code: Optional[str] = Field(default=None, description="Код региона trudvsem (напр. 7700000000000 — Москва)")
    salary_min: Optional[int] = Field(default=None, ge=0, description="Минимальная зарплата")
    limit: int = Field(default=20, ge=1, le=100, description="Кол-во вакансий на странице")
    offset: int = Field(default=0, ge=0, description="Смещение (пагинация)")


class VacancyShortSchema(BaseModel):
    id: str
    name: str
    company_name: Optional[str] = None
    region_name: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    created_at: Optional[str] = None
    url: Optional[str] = None

class VacancySearchWithUserResponseSchema(BaseModel):   # <-- отдельное имя под обёртку
    user: UserPayload
    results: RequestResponseSchema
class VacancySearchResponseSchema(BaseModel):   # <-- переименовано
    total: int
    limit: int
    offset: int
    items: list[VacancyShortSchema]
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ExperienceEnum(str, Enum):
    no_experience = "noExperience"
    between_1_and_3 = "between1And3"
    between_3_and_6 = "between3And6"
    more_than_6 = "moreThan6"

class EmploymentEnum(str, Enum):
    full = "full"
    part = "part"
    project = "project"
    volunteer = "volunteer"
    probation = "probation"

class ScheduleEnum(str, Enum):
    full_day = "fullDay"
    shift = "shift"
    flexible = "flexible"
    remote = "remote"
    fly_in_fly_out = "flyInFlyOut"

class OrderByEnum(str, Enum):
    relevance = "relevance"
    publication_time = "publication_time"
    salary_desc = "salary_desc"
    salary_asc = "salary_asc"

class VacancySearchSchema(BaseModel):

    text: str = Field(..., min_length=2, description="Стек/должность, например 'Python FastAPI'")
    area: Optional[int] = Field(default=None, description="ID региона hh.ru (1=Москва, 2=СПб, 113=Россия)")
    experience: Optional[ExperienceEnum] = Field(default=None, description="Требуемый опыт работы")
    employment: Optional[EmploymentEnum] = Field(default=None, description="Тип занятости")
    schedule: Optional[ScheduleEnum] = Field(default=None, description="График работы")
    salary: Optional[int] = Field(default=None, ge=0, description="Желаемая зарплата")
    only_with_salary: bool = Field(default=False, description="Показывать только вакансии с указанной зарплатой")
    currency: Optional[str] = Field(default="RUR", description="Валюта зарплаты (RUR, USD, EUR)")
    professional_role: Optional[int] = Field(default=None, description="ID профессиональной роли hh.ru")
    order_by: OrderByEnum = Field(default=OrderByEnum.relevance, description="Сортировка результатов")
    page: int = Field(default=0, ge=0, description="Номер страницы (с 0)")
    per_page: int = Field(default=20, ge=1, le=100, description="Кол-во вакансий на странице")


class VacancyShortSchema(BaseModel):
    id: str
    name: str
    employer_name: Optional[str] = None
    area_name: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    salary_currency: Optional[str] = None
    published_at: Optional[str] = None
    alternate_url: str
    snippet_requirement: Optional[str] = None
    snippet_responsibility: Optional[str] = None
    
class VacancySearchResponseSchema(BaseModel):
    found: int
    pages: int
    page: int
    per_page: int
    items: list[VacancyShortSchema]
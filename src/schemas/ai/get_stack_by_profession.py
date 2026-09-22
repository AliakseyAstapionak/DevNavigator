from pydantic import BaseModel, Field
from typing import List


class GetStackByProfessionRequestSchema(BaseModel):
    profession: str = Field(..., min_length=2, description="Например 'Python разработчик на FastAPI'")

class GetStackByProfessionResponseSchema(BaseModel):
    role: str
    stack: list[str]
    learning_advice: list[str]
    difficulty: str    
    estimated_time_months: int
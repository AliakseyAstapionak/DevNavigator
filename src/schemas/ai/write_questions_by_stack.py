from pydantic import BaseModel, Field
from typing import List

class GetQuestionsByStackRequestSchema(BaseModel):
    profession_with_stack: str = Field(..., min_length=5)


class GetQuestionsByStackResponseSchema(BaseModel):
    questions: list[str]
    difficulty: str    
    



from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Any

class RequestResponseSchema(BaseModel):
    id: int
    user_id: int
    request: dict[str, Any]
    response: dict[str, Any] | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
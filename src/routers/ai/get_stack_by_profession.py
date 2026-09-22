from fastapi import APIRouter, Depends
from schemas import (
    GetStackByProfessionRequestSchema,
    UserPayload,
)
from services import GetStackByProfessionService, RequestService
from dependences import get_current_user
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter(prefix="/ai")

@router.post('/profession_advice')
async def get_stack_by_profession(payload: GetStackByProfessionRequestSchema, user: UserPayload = Depends(get_current_user), db: AsyncSession = Depends(get_db),):
    result = await GetStackByProfessionService.get_advice(payload)
    db_request = await RequestService.create_request(user_id=user.id, request=payload, response=result, db=db)
    return {'user': user, 'results': db_request}

from fastapi import APIRouter, Depends
from schemas import GetQuestionsByStackRequestSchema
from services import WriteQuestionsByStackService, RequestService
from dependences import get_current_user
from database import get_db
router = APIRouter(prefix='/ai')


@router.post('/interview_advice')
async def write_questions_by_stack(payload: GetQuestionsByStackRequestSchema, user=Depends(get_current_user), db=Depends(get_db)):
    result = await WriteQuestionsByStackService.get_advice(payload)
    db_request = await RequestService.create_request(user_id=user.id, request=payload, response=result, db=db)
    return {'user': user, 'results': db_request}



from fastapi import HTTPException, Depends, Request, status
from config import JWT_SECRET_KEY
from schemas import UserPayload

import jwt



async def get_current_user(request: Request) -> UserPayload:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Вы не авторизованы"
        )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("uid")
        user_name: str = payload.get('username')
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Срок действия сессии истек")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка валидации токена")
    
    user = UserPayload(id=user_id, username=user_name )
    return user
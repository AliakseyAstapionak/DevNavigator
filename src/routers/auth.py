from fastapi import APIRouter, Depends, status, HTTPException, Response
from schemas import RegistrateUserSchema, UserActionResponseSchema, LoginUserSchema,StatusResponseSchema
from sqlalchemy.ext.asyncio import AsyncSession
from utils import hash_password, verify_password
from config import JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_SECONDS
import time
from services import UserService
from database import get_db
import jwt

router = APIRouter()

@router.post('/registration', response_model=UserActionResponseSchema, status_code=status.HTTP_201_CREATED)
async def registration(user: RegistrateUserSchema, db: AsyncSession = Depends(get_db)):
    existing_user = await UserService.get_user_by_name(username=user.username, db=db)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с таким именем уже существует")
    hashed_pwd = await hash_password(user.password)
    new_user = await UserService.create_user(username=user.username, hashed_pwd=hashed_pwd, db=db)
    return {'success': True, 'user': new_user}

@router.post('/login', response_model=UserActionResponseSchema)
async def login(response: Response, user: LoginUserSchema, db: AsyncSession = Depends(get_db)):
    existing_user = await UserService.get_user_by_name(username=user.username, db=db)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Неверный логин или пароль")
    if not await verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный логин или пароль") 
    payload = {
        'uid': existing_user.id,
        'username': existing_user.username,
        'exp': int(time.time()) + ACCESS_TOKEN_EXPIRE_SECONDS
    }
    access_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=ACCESS_TOKEN_EXPIRE_SECONDS + 60,
            httponly=True,
            secure=False,
            path='/'
        )
    return {'success': True, 'user': existing_user}

@router.post('/logout', response_model=StatusResponseSchema)
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path='/',         
        httponly=True,    
        secure=False
    )
    return {'success': True, 'message': 'Успешный выход из системы'}
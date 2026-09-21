from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import auth_router, vacancy_router, get_stack_by_profession_router
from database import engine, Base
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Приложение запущено!')
    yield
    await engine.dispose()
    print('Приложение остановлено!')


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(vacancy_router)
app.include_router(get_stack_by_profession_router)


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
from routers import auth_router, vacancy_router, get_stack_by_profession_router, write_questions_by_stack_router
from database import engine, Base
import uvicorn
from services.vacancy import close_client

STATIC_DIR = Path(__file__).resolve().parent / "static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Приложение запущено!')
    yield
    await close_client()
    await engine.dispose()
    print('Приложение остановлено!')


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(vacancy_router)
app.include_router(get_stack_by_profession_router)
app.include_router(write_questions_by_stack_router)

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=False, workers=4)
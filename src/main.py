from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
from routers import auth_router, vacancy_router, get_stack_by_profession_router, write_questions_by_stack_router
from database import engine, Base
import uvicorn
from services.utils import close_client

from fastapi.responses import FileResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
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

@app.get("/ping")
async def ping():
    return {"message": "pong"}

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(STATIC_DIR / "index.html")

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=False, workers=1)
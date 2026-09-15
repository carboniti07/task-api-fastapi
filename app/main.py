from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine
from app.db_models import Base
from app.routes import tasks_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Para este projeto didático, criamos as tabelas automaticamente.
    # Em aplicações com evolução de schema, use migrações.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Task API",
    version="1.0.0",
    description="API REST de tarefas para estudo de FastAPI, SQLAlchemy e Docker.",
    lifespan=lifespan,
)


@app.get("/", tags=["system"])
def home() -> dict[str, str]:
    return {"message": "Task API funcionando"}


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(tasks_router)

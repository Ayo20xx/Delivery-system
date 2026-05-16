from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.schemas import master_router
from .database.session import create_db_tables


@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    await create_db_tables()
    yield


app= FastAPI(
    lifespan= lifespan_handler,
)


app.include_router(master_router)



from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from sqlmodel import SQLModel
from config import Db_settings

engine=create_async_engine(
    url=Db_settings.POSTGRES_URL,
    echo=True,
    

)


async def create_db_tables():
    async with engine.begin() as connection:
        from app.database.model import Shipment # noqa: F401
        await connection.run_sync(SQLModel.metadata.create_all)
        

async def get_session():
    async_session=async_sessionmaker(
        bind=engine,
        class_= AsyncSession,
        expire_on_commit= False,
    )
    async with async_session() as session:
        yield session


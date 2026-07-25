from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import settings

# Create a database engine to connet with database
engine = create_async_engine(
    # database type/dialect and file name
    url=settings.POSTGRES_URL,
    # log sql queriesd
    echo=True,
)


# Session to create tables inside DB if they don't exist
async def create_db_tables():
    async with engine.begin() as connection:
        from .models import Shipment  # noqa: F401

        await connection.run_sync(SQLModel.metadata.create_all(bind=engine))


# Session to interact with database
async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session as session:
        yield session


# Session Dependency Annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]

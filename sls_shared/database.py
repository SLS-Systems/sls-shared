import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Read database URL from environment
db_url = os.environ.get("DATABASE_URL", "")

# Ensure we use the psycopg driver
if "+asyncpg" in db_url:
    db_url = db_url.replace("+asyncpg", "+psycopg")
elif "postgresql://" in db_url and "+psycopg" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://")

engine = create_async_engine(
    db_url,
    pool_size=1,
    max_overflow=2,
    pool_pre_ping=True,
    pool_recycle=300,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

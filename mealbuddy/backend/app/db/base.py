from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Convert PostgresDsn to string and ensure asyncpg is used
if isinstance(settings.DATABASE_URL, str):
    database_url = settings.DATABASE_URL
else:
    database_url = str(settings.DATABASE_URL)

# Ensure we're using the asyncpg driver
database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

# Create async database engine
engine = create_async_engine(
    database_url,
    echo=settings.DEBUG,
    future=True
)

# Create async session factory
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
async def get_db() -> AsyncSession:
    """Dependency that provides a database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

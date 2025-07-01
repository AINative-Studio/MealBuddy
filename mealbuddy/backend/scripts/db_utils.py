"""Database utility functions for MealBuddy.

This module provides utility functions for common database operations,
such as initializing the database, creating the first superuser,
and managing database sessions.
"""
import asyncio
import logging
from typing import AsyncGenerator, Optional

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base
from app.models.user import User
from app.core.security import get_password_hash

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create async engine and session
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def init_db() -> None:
    """
    Initialize the database by creating all tables.
    
    This should be called when the application starts.
    """
    logger.info("Initializing database...")
    
    async with async_engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database initialized successfully")


async def create_first_superuser() -> None:
    """
    Create the first superuser if no users exist in the database.
    
    This is typically called during application startup.
    """
    logger.info("Checking for first superuser...")
    
    async with AsyncSessionLocal() as db:
        # Check if any users exist
        result = await db.execute(sa.select(User).limit(1))
        user = result.scalar_one_or_none()
        
        if user is not None:
            logger.info("Users already exist, skipping first superuser creation")
            return
        
        # Create first superuser
        logger.info("Creating first superuser...")
        
        user = User(
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
            is_active=True,
            is_verified=True,
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        logger.info("First superuser created: %s", user.email)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session.
    
    This is a dependency that can be used in FastAPI route handlers.
    
    Yields:
        AsyncSession: An async database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def reset_db() -> None:
    """
    Drop all tables and recreate them.
    
    Warning: This will delete all data in the database!
    Only use this in development and testing environments.
    """
    if not settings.DEBUG:
        raise RuntimeError("reset_db() can only be used in debug mode")
    
    logger.warning("Dropping all database tables...")
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    logger.info("Recreating all database tables...")
    await init_db()
    
    logger.info("Creating first superuser...")
    await create_first_superuser()
    
    logger.info("Database reset complete")


if __name__ == "__main__":
    # This allows running the script directly for testing
    import sys
    
    async def main() -> None:
        """Run the main async function."""
        if "--reset" in sys.argv:
            await reset_db()
        else:
            await init_db()
            await create_first_superuser()
    
    asyncio.run(main())

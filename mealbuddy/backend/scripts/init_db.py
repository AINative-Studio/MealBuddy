#!/usr/bin/env python3
"""Initialize the database and apply migrations.

This script initializes the database by applying all pending migrations
and creating the first superuser if no users exist.

Usage:
    python -m scripts.init_db [--reset]

Options:
    --reset  Drop all tables and recreate them (use with caution!)
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from alembic import command
from alembic.config import Config
from sqlalchemy_utils import database_exists, create_database

from scripts.db_utils import (
    init_db as db_init,
    create_first_superuser,
    reset_db,
    async_engine,
)
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def ensure_database() -> None:
    """Ensure the database exists."""
    # Convert asyncpg URL to sync URL for sqlalchemy-utils
    sync_url = str(settings.DATABASE_URL).replace("+asyncpg", "")
    
    if not database_exists(sync_url):
        logger.info(f"Creating database: {sync_url}")
        create_database(sync_url)


async def run_migrations() -> None:
    """Run database migrations using Alembic."""
    logger.info("Running database migrations...")
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    
    # Set up Alembic config
    alembic_cfg = Config(script_dir.parent / "alembic.ini")
    
    # Set the script location
    alembic_cfg.set_main_option(
        "script_location", 
        str(script_dir.parent / "alembic")
    )
    
    # Set the database URL
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))
    
    # Run the migrations
    command.upgrade(alembic_cfg, "head")
    
    logger.info("Migrations completed successfully")


async def main() -> None:
    """Initialize the database and create the first superuser."""
    # Check if we should reset the database
    if "--reset" in sys.argv:
        logger.warning("Resetting database...")
        await reset_db()
        return
    
    # Ensure database exists
    await ensure_database()
    
    # Run migrations
    await run_migrations()
    
    # Initialize the database
    await db_init()
    
    # Create the first superuser if no users exist
    await create_first_superuser()
    
    logger.info("Database initialization complete")


if __name__ == "__main__":
    asyncio.run(main())

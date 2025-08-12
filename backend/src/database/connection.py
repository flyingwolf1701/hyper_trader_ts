"""
Database connection management for PostgreSQL using asyncpg.
"""

from contextlib import asynccontextmanager
from typing import Optional, AsyncGenerator
import os

import asyncpg
import structlog
from pydantic import BaseSettings

logger = structlog.get_logger(__name__)


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    database_url: Optional[str] = None
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "hyper_trader"
    database_user: str = "postgres"
    database_password: str = ""
    database_pool_min_size: int = 10
    database_pool_max_size: int = 20
    
    class Config:
        env_prefix = "DATABASE_"
        env_file = ".env"


# Global connection pool
_pool: Optional[asyncpg.Pool] = None
_settings = DatabaseSettings()


async def get_database_pool() -> asyncpg.Pool:
    """Get or create the database connection pool."""
    global _pool
    
    if _pool is None:
        logger.info("Initializing database connection pool")
        
        # Build connection string
        if _settings.database_url:
            connection_string = _settings.database_url
        else:
            connection_string = (
                f"postgresql://{_settings.database_user}:{_settings.database_password}"
                f"@{_settings.database_host}:{_settings.database_port}/{_settings.database_name}"
            )
        
        try:
            _pool = await asyncpg.create_pool(
                connection_string,
                min_size=_settings.database_pool_min_size,
                max_size=_settings.database_pool_max_size,
                command_timeout=30,
                server_settings={
                    "jit": "off",  # Disable JIT for better performance on small queries
                }
            )
            
            logger.info(
                "Database connection pool created successfully",
                min_size=_settings.database_pool_min_size,
                max_size=_settings.database_pool_max_size
            )
            
        except Exception as e:
            logger.error("Failed to create database connection pool", exc_info=e)
            raise
    
    return _pool


async def close_database_pool() -> None:
    """Close the database connection pool."""
    global _pool
    
    if _pool:
        logger.info("Closing database connection pool")
        await _pool.close()
        _pool = None
        logger.info("Database connection pool closed")


@asynccontextmanager
async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """Get a database connection from the pool."""
    pool = await get_database_pool()
    
    async with pool.acquire() as connection:
        try:
            yield connection
        except Exception as e:
            logger.error("Database operation failed", exc_info=e)
            raise


async def execute_migration_file(connection: asyncpg.Connection, file_path: str) -> None:
    """Execute a SQL migration file."""
    logger.info("Executing migration file", file_path=file_path)
    
    try:
        with open(file_path, "r") as f:
            migration_sql = f.read()
        
        await connection.execute(migration_sql)
        logger.info("Migration file executed successfully", file_path=file_path)
        
    except Exception as e:
        logger.error("Failed to execute migration file", file_path=file_path, exc_info=e)
        raise


async def run_migrations() -> None:
    """Run all pending database migrations."""
    logger.info("Running database migrations")
    
    migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")
    
    if not os.path.exists(migrations_dir):
        logger.info("No migrations directory found, skipping migrations")
        return
    
    async with get_db_connection() as connection:
        # Create migrations table if it doesn't exist
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL UNIQUE,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Get list of executed migrations
        executed_migrations = await connection.fetch(
            "SELECT filename FROM migrations ORDER BY id"
        )
        executed_filenames = {row["filename"] for row in executed_migrations}
        
        # Get list of migration files
        migration_files = []
        for filename in os.listdir(migrations_dir):
            if filename.endswith(".sql"):
                migration_files.append(filename)
        
        migration_files.sort()  # Ensure consistent ordering
        
        # Execute new migrations
        for filename in migration_files:
            if filename not in executed_filenames:
                file_path = os.path.join(migrations_dir, filename)
                
                try:
                    async with connection.transaction():
                        await execute_migration_file(connection, file_path)
                        await connection.execute(
                            "INSERT INTO migrations (filename) VALUES ($1)",
                            filename
                        )
                    
                    logger.info("Migration completed successfully", filename=filename)
                    
                except Exception as e:
                    logger.error("Migration failed", filename=filename, exc_info=e)
                    raise
        
        logger.info("All migrations completed successfully")
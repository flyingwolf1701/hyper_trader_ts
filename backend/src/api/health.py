"""
Health check endpoints for monitoring system status.
"""

from datetime import datetime
from typing import Dict, Any

import structlog
from fastapi import APIRouter, Depends

from database.connection import get_db_connection

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "hyper-trader-backend"
    }


@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check including database connectivity."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "hyper-trader-backend",
        "components": {}
    }
    
    # Check database connectivity
    try:
        async with get_db_connection() as connection:
            result = await connection.fetchval("SELECT 1")
            health_status["components"]["database"] = {
                "status": "healthy" if result == 1 else "unhealthy",
                "response_time_ms": 0  # Could add timing here
            }
    except Exception as e:
        logger.error("Database health check failed", exc_info=e)
        health_status["components"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # TODO: Add more component checks (WebSocket, external APIs)
    
    return health_status
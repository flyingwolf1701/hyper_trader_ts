"""
HyperTrader FastAPI Application Entry Point

Main application server for the HyperTrader Fibonacci hedging trading system.
Provides REST API endpoints for trading plan management, portfolio allocation,
position monitoring, and market data integration.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api import health, trading_plans, portfolio, positions, market_data
from database.connection import get_database_pool, close_database_pool
from services.websocket_manager import WebSocketManager

# Configure structured logging
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan management."""
    logger.info("Starting HyperTrader backend")
    
    # Initialize database connection pool
    await get_database_pool()
    logger.info("Database connection pool initialized")
    
    # Initialize WebSocket manager for market data
    app.state.websocket_manager = WebSocketManager()
    logger.info("WebSocket manager initialized")
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down HyperTrader backend")
    await close_database_pool()
    await app.state.websocket_manager.close()
    logger.info("Cleanup completed")


# Create FastAPI application
app = FastAPI(
    title="HyperTrader API",
    description="Fibonacci hedging trading assistant backend API",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error("Unhandled exception", exc_info=exc, path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred"
        }
    )


# Include API routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(trading_plans.router, prefix="/api/v1", tags=["trading-plans"])
app.include_router(portfolio.router, prefix="/api/v1", tags=["portfolio"])
app.include_router(positions.router, prefix="/api/v1", tags=["positions"])
app.include_router(market_data.router, prefix="/api/v1", tags=["market-data"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "HyperTrader API",
        "version": "0.1.0",
        "description": "Fibonacci hedging trading assistant",
        "docs_url": "/docs",
        "health_check": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    )
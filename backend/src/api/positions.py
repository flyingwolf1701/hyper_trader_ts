"""
Active positions API endpoints for monitoring and management.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID

import structlog
from fastapi import APIRouter, HTTPException, Depends, status

from models.position import Position, PositionCreate, PositionUpdate
from database.repositories.position_repository import PositionRepository
from database.connection import get_db_connection

logger = structlog.get_logger(__name__)
router = APIRouter()


async def get_position_repo():
    """Dependency to get position repository."""
    async with get_db_connection() as connection:
        yield PositionRepository(connection)


@router.get("/positions", response_model=List[Position])
async def get_active_positions(
    coin: Optional[str] = None,
    status_filter: Optional[str] = "active",
    repo: PositionRepository = Depends(get_position_repo)
) -> List[Position]:
    """Get active positions with optional filtering."""
    logger.info("Retrieving positions", coin=coin, status=status_filter)
    
    try:
        positions = await repo.get_all(coin=coin, status=status_filter)
        logger.info("Positions retrieved successfully", count=len(positions))
        return positions
    except Exception as e:
        logger.error("Failed to retrieve positions", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve positions"
        )


@router.get("/positions/{position_id}", response_model=Position)
async def get_position(
    position_id: UUID,
    repo: PositionRepository = Depends(get_position_repo)
) -> Position:
    """Get a specific position by ID."""
    logger.info("Retrieving position", position_id=position_id)
    
    try:
        position = await repo.get_by_id(position_id)
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found"
            )
        
        logger.info("Position retrieved successfully", position_id=position_id)
        return position
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve position", position_id=position_id, exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve position"
        )


@router.post("/positions", response_model=Position, status_code=status.HTTP_201_CREATED)
async def create_position(
    position_data: PositionCreate,
    repo: PositionRepository = Depends(get_position_repo)
) -> Position:
    """Create a new position entry."""
    logger.info("Creating new position", coin=position_data.coin, side=position_data.side)
    
    try:
        position = await repo.create(position_data)
        logger.info("Position created successfully", position_id=position.id)
        return position
    except Exception as e:
        logger.error("Failed to create position", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create position"
        )


@router.put("/positions/{position_id}", response_model=Position)
async def update_position(
    position_id: UUID,
    position_update: PositionUpdate,
    repo: PositionRepository = Depends(get_position_repo)
) -> Position:
    """Update an existing position."""
    logger.info("Updating position", position_id=position_id)
    
    try:
        position = await repo.update(position_id, position_update)
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found"
            )
        
        logger.info("Position updated successfully", position_id=position_id)
        return position
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update position", position_id=position_id, exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update position"
        )


@router.post("/positions/{position_id}/close")
async def close_position(
    position_id: UUID,
    repo: PositionRepository = Depends(get_position_repo)
) -> Dict[str, Any]:
    """Close an active position."""
    logger.info("Closing position", position_id=position_id)
    
    try:
        success = await repo.close_position(position_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found or already closed"
            )
        
        logger.info("Position closed successfully", position_id=position_id)
        return {"message": "Position closed successfully", "position_id": str(position_id)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to close position", position_id=position_id, exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to close position"
        )


@router.get("/positions/{position_id}/fibonacci")
async def get_position_fibonacci_levels(
    position_id: UUID,
    repo: PositionRepository = Depends(get_position_repo)
) -> Dict[str, Any]:
    """Get current Fibonacci levels for a position."""
    logger.info("Retrieving Fibonacci levels", position_id=position_id)
    
    try:
        levels = await repo.get_fibonacci_levels(position_id)
        if not levels:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found"
            )
        
        logger.info("Fibonacci levels retrieved successfully", position_id=position_id)
        return levels
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve Fibonacci levels", position_id=position_id, exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve Fibonacci levels"
        )
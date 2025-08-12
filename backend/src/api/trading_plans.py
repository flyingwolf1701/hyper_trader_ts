"""
Trading plans API endpoints for CRUD operations on trading strategies.
"""

from typing import List, Optional
from uuid import UUID

import structlog
from fastapi import APIRouter, HTTPException, Depends, status

from models.trading_plan import TradingPlan, TradingPlanCreate, TradingPlanUpdate
from database.repositories.trading_plan_repository import TradingPlanRepository
from database.connection import get_db_connection

logger = structlog.get_logger(__name__)
router = APIRouter()


async def get_trading_plan_repo():
    """Dependency to get trading plan repository."""
    async with get_db_connection() as connection:
        yield TradingPlanRepository(connection)


@router.post("/trading-plans", response_model=TradingPlan, status_code=status.HTTP_201_CREATED)
async def create_trading_plan(
    plan_data: TradingPlanCreate,
    repo: TradingPlanRepository = Depends(get_trading_plan_repo)
) -> TradingPlan:
    """Create a new trading plan."""
    logger.info("Creating new trading plan", coin=plan_data.coin, strategy=plan_data.strategy)
    
    try:
        plan = await repo.create(plan_data)
        logger.info("Trading plan created successfully", plan_id=plan.id)
        return plan
    except Exception as e:
        logger.error("Failed to create trading plan", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create trading plan"
        )


@router.get("/trading-plans", response_model=List[TradingPlan])
async def get_trading_plans(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    repo: TradingPlanRepository = Depends(get_trading_plan_repo)
) -> List[TradingPlan]:
    """Get all trading plans with optional filtering."""
    logger.info("Retrieving trading plans", skip=skip, limit=limit, active_only=active_only)
    
    try:
        plans = await repo.get_all(skip=skip, limit=limit, active_only=active_only)
        logger.info("Retrieved trading plans", count=len(plans))
        return plans
    except Exception as e:
        logger.error("Failed to retrieve trading plans", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve trading plans"
        )


@router.get("/trading-plans/{plan_id}", response_model=TradingPlan)
async def get_trading_plan(
    plan_id: UUID,
    repo: TradingPlanRepository = Depends(get_trading_plan_repo)
) -> TradingPlan:
    """Get a specific trading plan by ID."""
    logger.info("Retrieving trading plan", plan_id=plan_id)
    
    try:
        plan = await repo.get_by_id(plan_id)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trading plan not found"
            )
        
        logger.info("Trading plan retrieved successfully", plan_id=plan_id)
        return plan
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve trading plan", plan_id=plan_id, exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve trading plan"
        )


@router.put("/trading-plans/{plan_id}", response_model=TradingPlan)
async def update_trading_plan(
    plan_id: UUID,
    plan_update: TradingPlanUpdate,
    repo: TradingPlanRepository = Depends(get_trading_plan_repo)
) -> TradingPlan:
    """Update an existing trading plan."""
    logger.info("Updating trading plan", plan_id=plan_id)
    
    try:
        plan = await repo.update(plan_id, plan_update)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trading plan not found"
            )
        
        logger.info("Trading plan updated successfully", plan_id=plan_id)
        return plan
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update trading plan", plan_id=plan_id, exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update trading plan"
        )


@router.delete("/trading-plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trading_plan(
    plan_id: UUID,
    repo: TradingPlanRepository = Depends(get_trading_plan_repo)
) -> None:
    """Delete a trading plan (soft delete - marks as inactive)."""
    logger.info("Deleting trading plan", plan_id=plan_id)
    
    try:
        success = await repo.delete(plan_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trading plan not found"
            )
        
        logger.info("Trading plan deleted successfully", plan_id=plan_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete trading plan", plan_id=plan_id, exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete trading plan"
        )
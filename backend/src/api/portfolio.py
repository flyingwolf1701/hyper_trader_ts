"""
Portfolio management API endpoints for allocation and performance tracking.
"""

from typing import List, Dict, Any

import structlog
from fastapi import APIRouter, HTTPException, Depends, status

from models.portfolio import PortfolioAllocation, PortfolioAllocationCreate, PortfolioAllocationUpdate
from database.repositories.portfolio_repository import PortfolioRepository
from database.connection import get_db_connection

logger = structlog.get_logger(__name__)
router = APIRouter()


async def get_portfolio_repo():
    """Dependency to get portfolio repository."""
    async with get_db_connection() as connection:
        yield PortfolioRepository(connection)


@router.get("/portfolio/overview")
async def get_portfolio_overview(
    repo: PortfolioRepository = Depends(get_portfolio_repo)
) -> Dict[str, Any]:
    """Get portfolio overview with total value, allocations, and performance."""
    logger.info("Retrieving portfolio overview")
    
    try:
        overview = await repo.get_overview()
        logger.info("Portfolio overview retrieved successfully")
        return overview
    except Exception as e:
        logger.error("Failed to retrieve portfolio overview", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve portfolio overview"
        )


@router.get("/portfolio/allocations", response_model=List[PortfolioAllocation])
async def get_portfolio_allocations(
    repo: PortfolioRepository = Depends(get_portfolio_repo)
) -> List[PortfolioAllocation]:
    """Get all portfolio allocations."""
    logger.info("Retrieving portfolio allocations")
    
    try:
        allocations = await repo.get_allocations()
        logger.info("Portfolio allocations retrieved successfully", count=len(allocations))
        return allocations
    except Exception as e:
        logger.error("Failed to retrieve portfolio allocations", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve portfolio allocations"
        )


@router.post("/portfolio/allocations", response_model=PortfolioAllocation, status_code=status.HTTP_201_CREATED)
async def create_portfolio_allocation(
    allocation_data: PortfolioAllocationCreate,
    repo: PortfolioRepository = Depends(get_portfolio_repo)
) -> PortfolioAllocation:
    """Create a new portfolio allocation."""
    logger.info("Creating portfolio allocation", coin=allocation_data.coin)
    
    try:
        allocation = await repo.create_allocation(allocation_data)
        logger.info("Portfolio allocation created successfully", allocation_id=allocation.id)
        return allocation
    except Exception as e:
        logger.error("Failed to create portfolio allocation", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create portfolio allocation"
        )


@router.put("/portfolio/allocations/{coin}", response_model=PortfolioAllocation)
async def update_portfolio_allocation(
    coin: str,
    allocation_update: PortfolioAllocationUpdate,
    repo: PortfolioRepository = Depends(get_portfolio_repo)
) -> PortfolioAllocation:
    """Update portfolio allocation for a specific coin."""
    logger.info("Updating portfolio allocation", coin=coin)
    
    try:
        allocation = await repo.update_allocation(coin, allocation_update)
        if not allocation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio allocation not found"
            )
        
        logger.info("Portfolio allocation updated successfully", coin=coin)
        return allocation
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update portfolio allocation", coin=coin, exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update portfolio allocation"
        )


@router.get("/portfolio/performance")
async def get_portfolio_performance(
    days: int = 30,
    repo: PortfolioRepository = Depends(get_portfolio_repo)
) -> Dict[str, Any]:
    """Get portfolio performance metrics over specified time period."""
    logger.info("Retrieving portfolio performance", days=days)
    
    try:
        performance = await repo.get_performance(days=days)
        logger.info("Portfolio performance retrieved successfully")
        return performance
    except Exception as e:
        logger.error("Failed to retrieve portfolio performance", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve portfolio performance"
        )


@router.post("/portfolio/rebalance")
async def rebalance_portfolio(
    repo: PortfolioRepository = Depends(get_portfolio_repo)
) -> Dict[str, Any]:
    """Trigger portfolio rebalancing based on current allocations."""
    logger.info("Initiating portfolio rebalance")
    
    try:
        # TODO: Implement actual rebalancing logic
        result = {"message": "Portfolio rebalancing initiated", "status": "pending"}
        logger.info("Portfolio rebalance initiated successfully")
        return result
    except Exception as e:
        logger.error("Failed to initiate portfolio rebalance", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initiate portfolio rebalance"
        )
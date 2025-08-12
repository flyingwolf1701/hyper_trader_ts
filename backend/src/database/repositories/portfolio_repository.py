"""
Repository for portfolio data operations.
"""

from typing import List, Optional, Dict, Any

import asyncpg
import structlog

from models.portfolio import PortfolioAllocation, PortfolioAllocationCreate, PortfolioAllocationUpdate

logger = structlog.get_logger(__name__)


class PortfolioRepository:
    """Repository for portfolio database operations."""
    
    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection
    
    async def create_allocation(self, allocation_data: PortfolioAllocationCreate) -> PortfolioAllocation:
        """Create a new portfolio allocation."""
        query = """
            INSERT INTO portfolio_allocations (
                coin, target_allocation_percent, max_allocation_percent,
                min_allocation_percent, cash_reserve_percent,
                spot_savings_enabled, spot_savings_percent
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING *
        """
        
        row = await self.connection.fetchrow(
            query,
            allocation_data.coin,
            allocation_data.target_allocation_percent,
            allocation_data.max_allocation_percent,
            allocation_data.min_allocation_percent,
            allocation_data.cash_reserve_percent,
            allocation_data.spot_savings_enabled,
            allocation_data.spot_savings_percent
        )
        
        return PortfolioAllocation(**row)
    
    async def get_allocations(self, active_only: bool = True) -> List[PortfolioAllocation]:
        """Get all portfolio allocations."""
        query = "SELECT * FROM portfolio_allocations"
        params = []
        
        if active_only:
            query += " WHERE is_active = $1"
            params.append(True)
        
        query += " ORDER BY target_allocation_percent DESC"
        
        rows = await self.connection.fetch(query, *params)
        return [PortfolioAllocation(**row) for row in rows]
    
    async def update_allocation(self, coin: str, allocation_update: PortfolioAllocationUpdate) -> Optional[PortfolioAllocation]:
        """Update portfolio allocation for a specific coin."""
        update_fields = []
        params = []
        param_count = 0
        
        for field, value in allocation_update.model_dump(exclude_unset=True).items():
            if value is not None:
                param_count += 1
                update_fields.append(f"{field} = ${param_count}")
                params.append(value)
        
        if not update_fields:
            # No updates to make, return current allocation
            query = "SELECT * FROM portfolio_allocations WHERE coin = $1"
            row = await self.connection.fetchrow(query, coin.upper())
            return PortfolioAllocation(**row) if row else None
        
        param_count += 1
        params.append(coin.upper())
        
        query = f"""
            UPDATE portfolio_allocations 
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE coin = ${param_count}
            RETURNING *
        """
        
        row = await self.connection.fetchrow(query, *params)
        
        if row:
            return PortfolioAllocation(**row)
        return None
    
    async def get_overview(self) -> Dict[str, Any]:
        """Get portfolio overview with aggregated metrics."""
        # TODO: Implement actual portfolio calculations
        # This is a placeholder implementation
        
        return {
            "total_value_usd": 0.0,
            "total_cash_usd": 0.0,
            "total_invested_usd": 0.0,
            "total_pnl_usd": 0.0,
            "total_pnl_percent": 0.0,
            "daily_pnl_usd": 0.0,
            "daily_pnl_percent": 0.0,
            "total_exposure_usd": 0.0,
            "cash_reserve_ratio": 0.1,
            "max_drawdown_percent": 0.0,
            "active_positions_count": 0,
            "total_positions_count": 0,
            "allocated_coins_count": 0,
            "target_allocation_sum": 0.0,
            "current_allocation_sum": 0.0,
            "last_updated": "2025-01-01T00:00:00Z"
        }
    
    async def get_performance(self, days: int = 30) -> Dict[str, Any]:
        """Get portfolio performance metrics over specified time period."""
        # TODO: Implement actual performance calculations
        # This is a placeholder implementation
        
        return {
            "start_date": "2025-01-01T00:00:00Z",
            "end_date": "2025-01-31T00:00:00Z",
            "total_return_percent": 0.0,
            "annualized_return_percent": None,
            "volatility_percent": None,
            "sharpe_ratio": None,
            "max_drawdown_percent": 0.0,
            "max_drawdown_date": None,
            "current_drawdown_percent": 0.0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate_percent": 0.0,
            "avg_win_percent": 0.0,
            "avg_loss_percent": 0.0,
            "profit_factor": None,
            "monthly_returns": []
        }
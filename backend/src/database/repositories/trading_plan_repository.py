"""
Repository for trading plan data operations.
"""

from typing import List, Optional
from uuid import UUID

import asyncpg
import structlog

from models.trading_plan import TradingPlan, TradingPlanCreate, TradingPlanUpdate

logger = structlog.get_logger(__name__)


class TradingPlanRepository:
    """Repository for trading plan database operations."""
    
    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection
    
    async def create(self, plan_data: TradingPlanCreate) -> TradingPlan:
        """Create a new trading plan."""
        query = """
            INSERT INTO trading_plans (
                coin, strategy, retracement_23_percent, retracement_38_percent,
                retracement_50_percent, max_drawdown_percent, stop_loss_percent,
                take_profit_percent, position_size_usd, max_position_count,
                hedge_ratio, scaling_enabled
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12
            ) RETURNING *
        """
        
        row = await self.connection.fetchrow(
            query,
            plan_data.coin,
            plan_data.strategy,
            plan_data.retracement_23_percent,
            plan_data.retracement_38_percent,
            plan_data.retracement_50_percent,
            plan_data.max_drawdown_percent,
            plan_data.stop_loss_percent,
            plan_data.take_profit_percent,
            plan_data.position_size_usd,
            plan_data.max_position_count,
            plan_data.hedge_ratio,
            plan_data.scaling_enabled
        )
        
        return TradingPlan(**row)
    
    async def get_by_id(self, plan_id: UUID) -> Optional[TradingPlan]:
        """Get a trading plan by ID."""
        query = "SELECT * FROM trading_plans WHERE id = $1"
        row = await self.connection.fetchrow(query, plan_id)
        
        if row:
            return TradingPlan(**row)
        return None
    
    async def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[TradingPlan]:
        """Get all trading plans with optional filtering."""
        base_query = "SELECT * FROM trading_plans"
        conditions = []
        params = []
        param_count = 0
        
        if active_only:
            param_count += 1
            conditions.append(f"is_active = ${param_count}")
            params.append(True)
        
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        base_query += " ORDER BY created_at DESC"
        
        param_count += 1
        base_query += f" LIMIT ${param_count}"
        params.append(limit)
        
        param_count += 1
        base_query += f" OFFSET ${param_count}"
        params.append(skip)
        
        rows = await self.connection.fetch(base_query, *params)
        return [TradingPlan(**row) for row in rows]
    
    async def update(self, plan_id: UUID, plan_update: TradingPlanUpdate) -> Optional[TradingPlan]:
        """Update an existing trading plan."""
        update_fields = []
        params = []
        param_count = 0
        
        for field, value in plan_update.model_dump(exclude_unset=True).items():
            if value is not None:
                param_count += 1
                update_fields.append(f"{field} = ${param_count}")
                params.append(value)
        
        if not update_fields:
            # No updates to make
            return await self.get_by_id(plan_id)
        
        param_count += 1
        params.append(plan_id)
        
        query = f"""
            UPDATE trading_plans 
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ${param_count}
            RETURNING *
        """
        
        row = await self.connection.fetchrow(query, *params)
        
        if row:
            return TradingPlan(**row)
        return None
    
    async def delete(self, plan_id: UUID) -> bool:
        """Soft delete a trading plan (mark as inactive)."""
        query = """
            UPDATE trading_plans 
            SET is_active = false, updated_at = CURRENT_TIMESTAMP
            WHERE id = $1 AND is_active = true
        """
        
        result = await self.connection.execute(query, plan_id)
        return result == "UPDATE 1"
    
    async def get_by_coin(self, coin: str, active_only: bool = True) -> List[TradingPlan]:
        """Get all trading plans for a specific coin."""
        query = "SELECT * FROM trading_plans WHERE coin = $1"
        params = [coin.upper()]
        
        if active_only:
            query += " AND is_active = $2"
            params.append(True)
        
        query += " ORDER BY created_at DESC"
        
        rows = await self.connection.fetch(query, *params)
        return [TradingPlan(**row) for row in rows]
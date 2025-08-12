"""
Repository for position data operations.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID

import asyncpg
import structlog

from models.position import Position, PositionCreate, PositionUpdate

logger = structlog.get_logger(__name__)


class PositionRepository:
    """Repository for position database operations."""
    
    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection
    
    async def create(self, position_data: PositionCreate) -> Position:
        """Create a new position."""
        query = """
            INSERT INTO positions (
                trading_plan_id, coin, side, entry_price, entry_quantity,
                entry_value_usd, entry_timestamp
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING *
        """
        
        row = await self.connection.fetchrow(
            query,
            position_data.trading_plan_id,
            position_data.coin,
            position_data.side,
            position_data.entry_price,
            position_data.entry_quantity,
            position_data.entry_value_usd,
            position_data.entry_timestamp
        )
        
        return Position(**row)
    
    async def get_by_id(self, position_id: UUID) -> Optional[Position]:
        """Get a position by ID."""
        query = "SELECT * FROM positions WHERE id = $1"
        row = await self.connection.fetchrow(query, position_id)
        
        if row:
            return Position(**row)
        return None
    
    async def get_all(self, coin: Optional[str] = None, status: Optional[str] = None) -> List[Position]:
        """Get positions with optional filtering."""
        base_query = "SELECT * FROM positions"
        conditions = []
        params = []
        param_count = 0
        
        if coin:
            param_count += 1
            conditions.append(f"coin = ${param_count}")
            params.append(coin.upper())
        
        if status:
            param_count += 1
            conditions.append(f"status = ${param_count}")
            params.append(status)
        
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        base_query += " ORDER BY created_at DESC"
        
        rows = await self.connection.fetch(base_query, *params)
        return [Position(**row) for row in rows]
    
    async def update(self, position_id: UUID, position_update: PositionUpdate) -> Optional[Position]:
        """Update an existing position."""
        update_fields = []
        params = []
        param_count = 0
        
        for field, value in position_update.model_dump(exclude_unset=True).items():
            if value is not None:
                param_count += 1
                update_fields.append(f"{field} = ${param_count}")
                params.append(value)
        
        if not update_fields:
            # No updates to make
            return await self.get_by_id(position_id)
        
        param_count += 1
        params.append(position_id)
        
        query = f"""
            UPDATE positions 
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ${param_count}
            RETURNING *
        """
        
        row = await self.connection.fetchrow(query, *params)
        
        if row:
            return Position(**row)
        return None
    
    async def close_position(self, position_id: UUID) -> bool:
        """Close a position by setting status to closed."""
        query = """
            UPDATE positions 
            SET status = 'closed', updated_at = CURRENT_TIMESTAMP
            WHERE id = $1 AND status != 'closed'
        """
        
        result = await self.connection.execute(query, position_id)
        return result == "UPDATE 1"
    
    async def get_fibonacci_levels(self, position_id: UUID) -> Optional[Dict[str, Any]]:
        """Get current Fibonacci levels for a position."""
        # TODO: Implement actual Fibonacci calculations
        # This is a placeholder implementation
        
        position = await self.get_by_id(position_id)
        if not position:
            return None
        
        return {
            "position_id": str(position_id),
            "coin": position.coin,
            "side": position.side,
            "entry_price": float(position.entry_price),
            "current_price": float(position.current_price) if position.current_price else None,
            "highest_since_entry": float(position.highest_price) if position.highest_price else None,
            "lowest_since_entry": float(position.lowest_price) if position.lowest_price else None,
            "level_23_price": float(position.fib_23_price) if position.fib_23_price else None,
            "level_38_price": float(position.fib_38_price) if position.fib_38_price else None,
            "level_50_price": float(position.fib_50_price) if position.fib_50_price else None,
            "current_gain_percent": 0.0,
            "peak_gain_percent": 0.0,
            "current_retracement_percent": 0.0,
            "is_23_triggered": False,
            "is_38_triggered": False,
            "is_50_triggered": False,
            "recommended_action": None,
            "hedge_suggested": False,
            "scale_suggested": False
        }
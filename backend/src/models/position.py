"""
Position data models for tracking individual trades and their Fibonacci levels.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, Literal
from uuid import UUID

from pydantic import BaseModel, Field, validator


class PositionBase(BaseModel):
    """Base position model with common fields."""
    
    coin: str = Field(..., min_length=1, max_length=10, description="Trading pair symbol")
    side: Literal["long", "short"] = Field(..., description="Position side")
    
    # Entry information
    entry_price: Decimal = Field(..., gt=0, description="Entry price")
    entry_quantity: Decimal = Field(..., gt=0, description="Entry quantity")
    entry_value_usd: Decimal = Field(..., gt=0, description="Entry value in USD")
    entry_timestamp: datetime = Field(..., description="Entry timestamp")
    
    @validator("coin")
    def coin_uppercase(cls, v):
        """Convert coin symbol to uppercase."""
        return v.upper().strip()


class PositionCreate(PositionBase):
    """Model for creating a new position."""
    
    trading_plan_id: UUID = Field(..., description="Associated trading plan ID")


class PositionUpdate(BaseModel):
    """Model for updating an existing position."""
    
    status: Optional[Literal["active", "hedged", "scaled", "closed"]] = None
    highest_price: Optional[Decimal] = None
    lowest_price: Optional[Decimal] = None
    current_price: Optional[Decimal] = None
    fib_23_price: Optional[Decimal] = None
    fib_38_price: Optional[Decimal] = None
    fib_50_price: Optional[Decimal] = None
    unrealized_pnl_usd: Optional[Decimal] = None
    realized_pnl_usd: Optional[Decimal] = None
    exit_price: Optional[Decimal] = None
    exit_quantity: Optional[Decimal] = None
    exit_timestamp: Optional[datetime] = None
    
    @validator("highest_price", "lowest_price", "current_price", 
              "fib_23_price", "fib_38_price", "fib_50_price", "exit_price")
    def validate_prices(cls, v):
        """Validate prices are positive if provided."""
        if v is not None and v <= 0:
            raise ValueError("Prices must be greater than 0")
        return v
    
    @validator("exit_quantity")
    def validate_exit_quantity(cls, v):
        """Validate exit quantity is positive if provided."""
        if v is not None and v <= 0:
            raise ValueError("Exit quantity must be greater than 0")
        return v


class Position(PositionBase):
    """Complete position model with database fields."""
    
    id: UUID
    trading_plan_id: UUID
    status: Literal["active", "hedged", "scaled", "closed"] = "active"
    
    # Position tracking
    highest_price: Optional[Decimal] = None
    lowest_price: Optional[Decimal] = None
    current_price: Optional[Decimal] = None
    
    # Cached Fibonacci levels
    fib_23_price: Optional[Decimal] = None
    fib_38_price: Optional[Decimal] = None
    fib_50_price: Optional[Decimal] = None
    
    # P&L tracking
    unrealized_pnl_usd: Optional[Decimal] = None
    realized_pnl_usd: Decimal = Decimal("0")
    
    # Exit information
    exit_price: Optional[Decimal] = None
    exit_quantity: Optional[Decimal] = None
    exit_timestamp: Optional[datetime] = None
    
    # Metadata
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PositionFibonacci(BaseModel):
    """Model for position-specific Fibonacci levels and analysis."""
    
    position_id: UUID
    coin: str
    side: Literal["long", "short"]
    
    # Current position data
    entry_price: Decimal
    current_price: Decimal
    highest_since_entry: Optional[Decimal]
    lowest_since_entry: Optional[Decimal]
    
    # Fibonacci levels (position-relative)
    level_23_price: Decimal
    level_38_price: Decimal
    level_50_price: Decimal
    
    # Retracement analysis
    current_gain_percent: Decimal  # Current % gain from entry
    peak_gain_percent: Decimal     # Highest % gain reached
    current_retracement_percent: Decimal  # Current % retracement from peak
    
    # Trigger status
    is_23_triggered: bool = False
    is_38_triggered: bool = False
    is_50_triggered: bool = False
    
    # Action recommendations
    recommended_action: Optional[str] = None
    hedge_suggested: bool = False
    scale_suggested: bool = False
    
    class Config:
        from_attributes = True


class PositionSummary(BaseModel):
    """Summary model for position overview."""
    
    id: UUID
    coin: str
    side: Literal["long", "short"]
    status: Literal["active", "hedged", "scaled", "closed"]
    
    entry_price: Decimal
    current_price: Optional[Decimal]
    entry_value_usd: Decimal
    unrealized_pnl_usd: Optional[Decimal]
    realized_pnl_usd: Decimal
    
    # Performance metrics
    gain_percent: Optional[Decimal]
    max_gain_percent: Optional[Decimal]
    current_retracement_percent: Optional[Decimal]
    
    # Duration
    duration_hours: Optional[Decimal]
    entry_timestamp: datetime
    exit_timestamp: Optional[datetime]
    
    class Config:
        from_attributes = True


class PositionRisk(BaseModel):
    """Model for position risk analysis."""
    
    position_id: UUID
    coin: str
    
    # Current exposure
    current_value_usd: Decimal
    max_loss_usd: Decimal  # Based on stop loss
    
    # Risk ratios
    risk_reward_ratio: Optional[Decimal]
    position_size_percent_of_portfolio: Decimal
    
    # Stop loss analysis
    current_stop_price: Optional[Decimal]
    distance_to_stop_percent: Optional[Decimal]
    
    # Fibonacci risk levels
    risk_at_23_percent: Decimal
    risk_at_38_percent: Decimal
    risk_at_50_percent: Decimal
    
    class Config:
        from_attributes = True
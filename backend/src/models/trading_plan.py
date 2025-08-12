"""
Trading plan data models for Fibonacci hedging strategy configuration.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class TradingPlanBase(BaseModel):
    """Base trading plan model with common fields."""
    
    coin: str = Field(..., min_length=1, max_length=10, description="Trading pair symbol (e.g., 'BTC', 'ETH')")
    strategy: str = Field(default="fibonacci_hedging", description="Trading strategy type")
    
    # Fibonacci levels configuration
    retracement_23_percent: Decimal = Field(default=Decimal("0.2300"), description="23% retracement level")
    retracement_38_percent: Decimal = Field(default=Decimal("0.3800"), description="38% retracement level") 
    retracement_50_percent: Decimal = Field(default=Decimal("0.5000"), description="50% retracement level")
    
    # Risk management parameters
    max_drawdown_percent: Decimal = Field(default=Decimal("0.2300"), description="Maximum allowed drawdown")
    stop_loss_percent: Decimal = Field(default=Decimal("0.0500"), description="Stop loss percentage")
    take_profit_percent: Optional[Decimal] = Field(default=None, description="Take profit percentage (optional)")
    
    # Position sizing
    position_size_usd: Decimal = Field(..., gt=0, description="Position size in USD")
    max_position_count: int = Field(default=1, ge=1, description="Maximum concurrent positions")
    
    # Hedging configuration
    hedge_ratio: Decimal = Field(default=Decimal("0.5000"), description="Hedge ratio at 23% retracement")
    scaling_enabled: bool = Field(default=True, description="Enable position scaling at deeper retracements")
    
    @validator("coin")
    def coin_uppercase(cls, v):
        """Convert coin symbol to uppercase."""
        return v.upper().strip()
    
    @validator("retracement_23_percent", "retracement_38_percent", "retracement_50_percent", 
              "max_drawdown_percent", "stop_loss_percent", "hedge_ratio")
    def validate_percentages(cls, v):
        """Validate percentage values are between 0 and 1."""
        if not 0 < v < 1:
            raise ValueError("Percentage values must be between 0 and 1")
        return v
    
    @validator("take_profit_percent")
    def validate_take_profit(cls, v):
        """Validate take profit percentage if provided."""
        if v is not None and not 0 < v < 1:
            raise ValueError("Take profit percentage must be between 0 and 1")
        return v
    
    def __init__(self, **data):
        super().__init__(**data)
        # Validate retracement level ordering
        if not (self.retracement_23_percent < self.retracement_38_percent < self.retracement_50_percent):
            raise ValueError("Retracement levels must be in ascending order: 23% < 38% < 50%")


class TradingPlanCreate(TradingPlanBase):
    """Model for creating a new trading plan."""
    pass


class TradingPlanUpdate(BaseModel):
    """Model for updating an existing trading plan."""
    
    strategy: Optional[str] = None
    retracement_23_percent: Optional[Decimal] = None
    retracement_38_percent: Optional[Decimal] = None
    retracement_50_percent: Optional[Decimal] = None
    max_drawdown_percent: Optional[Decimal] = None
    stop_loss_percent: Optional[Decimal] = None
    take_profit_percent: Optional[Decimal] = None
    position_size_usd: Optional[Decimal] = None
    max_position_count: Optional[int] = None
    hedge_ratio: Optional[Decimal] = None
    scaling_enabled: Optional[bool] = None
    is_active: Optional[bool] = None
    
    @validator("retracement_23_percent", "retracement_38_percent", "retracement_50_percent",
              "max_drawdown_percent", "stop_loss_percent", "hedge_ratio")
    def validate_percentages(cls, v):
        """Validate percentage values are between 0 and 1."""
        if v is not None and not 0 < v < 1:
            raise ValueError("Percentage values must be between 0 and 1")
        return v
    
    @validator("take_profit_percent")
    def validate_take_profit(cls, v):
        """Validate take profit percentage if provided."""
        if v is not None and not 0 < v < 1:
            raise ValueError("Take profit percentage must be between 0 and 1")
        return v
    
    @validator("position_size_usd")
    def validate_position_size(cls, v):
        """Validate position size is positive."""
        if v is not None and v <= 0:
            raise ValueError("Position size must be greater than 0")
        return v
    
    @validator("max_position_count")
    def validate_max_positions(cls, v):
        """Validate max position count is positive."""
        if v is not None and v < 1:
            raise ValueError("Max position count must be at least 1")
        return v


class TradingPlan(TradingPlanBase):
    """Complete trading plan model with database fields."""
    
    id: UUID
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FibonacciLevels(BaseModel):
    """Model for Fibonacci retracement levels calculation."""
    
    entry_price: Decimal
    highest_price: Decimal
    current_price: Decimal
    
    # Calculated levels
    level_23_price: Decimal
    level_38_price: Decimal 
    level_50_price: Decimal
    
    # Current position relative to levels
    current_retracement_percent: Decimal
    triggered_levels: list[str] = Field(default_factory=list)
    
    @validator("entry_price", "highest_price", "current_price",
              "level_23_price", "level_38_price", "level_50_price")
    def validate_prices(cls, v):
        """Validate all prices are positive."""
        if v <= 0:
            raise ValueError("All prices must be greater than 0")
        return v
    
    @validator("current_retracement_percent")
    def validate_retracement_percent(cls, v):
        """Validate retracement percentage."""
        if v < 0:
            raise ValueError("Retracement percentage cannot be negative")
        return v


class TradingPlanStats(BaseModel):
    """Model for trading plan performance statistics."""
    
    plan_id: UUID
    coin: str
    
    # Position counts
    total_positions: int
    active_positions: int
    closed_positions: int
    
    # Performance metrics
    total_pnl_usd: Decimal
    total_realized_pnl_usd: Decimal
    total_unrealized_pnl_usd: Decimal
    win_rate_percent: Decimal
    avg_trade_duration_hours: Optional[Decimal]
    
    # Risk metrics
    max_drawdown_experienced: Decimal
    current_exposure_usd: Decimal
    
    # Last updated
    last_updated: datetime
    
    class Config:
        from_attributes = True
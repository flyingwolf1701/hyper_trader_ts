"""
Portfolio data models for allocation management and performance tracking.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, validator


class PortfolioAllocationBase(BaseModel):
    """Base portfolio allocation model."""
    
    coin: str = Field(..., min_length=1, max_length=10, description="Trading pair symbol")
    target_allocation_percent: Decimal = Field(..., gt=0, le=1, description="Target allocation percentage")
    max_allocation_percent: Decimal = Field(..., gt=0, le=1, description="Maximum allocation percentage")
    min_allocation_percent: Decimal = Field(default=Decimal("0"), ge=0, description="Minimum allocation percentage")
    cash_reserve_percent: Decimal = Field(default=Decimal("0.1"), ge=0, lt=1, description="Cash reserve percentage")
    spot_savings_enabled: bool = Field(default=False, description="Enable spot savings accumulation")
    spot_savings_percent: Decimal = Field(default=Decimal("0.05"), ge=0, lt=1, description="Spot savings percentage")
    
    @validator("coin")
    def coin_uppercase(cls, v):
        """Convert coin symbol to uppercase."""
        return v.upper().strip()
    
    @validator("max_allocation_percent")
    def validate_max_allocation(cls, v, values):
        """Validate max allocation is >= target allocation."""
        target = values.get("target_allocation_percent")
        if target and v < target:
            raise ValueError("Max allocation must be >= target allocation")
        return v
    
    @validator("min_allocation_percent")
    def validate_min_allocation(cls, v, values):
        """Validate min allocation is <= target allocation."""
        target = values.get("target_allocation_percent")
        if target and v > target:
            raise ValueError("Min allocation must be <= target allocation")
        return v


class PortfolioAllocationCreate(PortfolioAllocationBase):
    """Model for creating a new portfolio allocation."""
    pass


class PortfolioAllocationUpdate(BaseModel):
    """Model for updating an existing portfolio allocation."""
    
    target_allocation_percent: Optional[Decimal] = None
    max_allocation_percent: Optional[Decimal] = None
    min_allocation_percent: Optional[Decimal] = None
    cash_reserve_percent: Optional[Decimal] = None
    spot_savings_enabled: Optional[bool] = None
    spot_savings_percent: Optional[Decimal] = None
    is_active: Optional[bool] = None
    
    @validator("target_allocation_percent", "max_allocation_percent")
    def validate_percentages(cls, v):
        """Validate percentages are between 0 and 1."""
        if v is not None and not 0 < v <= 1:
            raise ValueError("Allocation percentages must be between 0 and 1")
        return v
    
    @validator("min_allocation_percent", "cash_reserve_percent", "spot_savings_percent")
    def validate_non_negative_percentages(cls, v):
        """Validate percentages are non-negative and less than 1."""
        if v is not None and not 0 <= v < 1:
            raise ValueError("Percentages must be between 0 and 1")
        return v


class PortfolioAllocation(PortfolioAllocationBase):
    """Complete portfolio allocation model with database fields."""
    
    id: UUID
    current_allocation_percent: Decimal = Decimal("0")
    current_value_usd: Decimal = Decimal("0")
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PortfolioOverview(BaseModel):
    """Model for portfolio overview and summary statistics."""
    
    # Total portfolio value
    total_value_usd: Decimal
    total_cash_usd: Decimal
    total_invested_usd: Decimal
    
    # Performance metrics
    total_pnl_usd: Decimal
    total_pnl_percent: Decimal
    daily_pnl_usd: Decimal
    daily_pnl_percent: Decimal
    
    # Risk metrics
    total_exposure_usd: Decimal
    cash_reserve_ratio: Decimal
    max_drawdown_percent: Decimal
    
    # Position summary
    active_positions_count: int
    total_positions_count: int
    
    # Allocation summary
    allocated_coins_count: int
    target_allocation_sum: Decimal
    current_allocation_sum: Decimal
    
    # Last updated
    last_updated: datetime
    
    class Config:
        from_attributes = True


class CoinAllocationStatus(BaseModel):
    """Model for individual coin allocation status."""
    
    coin: str
    
    # Allocation percentages
    target_percent: Decimal
    current_percent: Decimal
    max_percent: Decimal
    min_percent: Decimal
    
    # Values
    target_value_usd: Decimal
    current_value_usd: Decimal
    deviation_value_usd: Decimal
    
    # Status
    is_overallocated: bool
    is_underallocated: bool
    needs_rebalancing: bool
    
    # Active positions
    active_positions_count: int
    total_position_value_usd: Decimal
    
    class Config:
        from_attributes = True


class PortfolioPerformance(BaseModel):
    """Model for portfolio performance analytics."""
    
    # Time period
    start_date: datetime
    end_date: datetime
    
    # Return metrics
    total_return_percent: Decimal
    annualized_return_percent: Optional[Decimal]
    volatility_percent: Optional[Decimal]
    sharpe_ratio: Optional[Decimal]
    
    # Drawdown analysis
    max_drawdown_percent: Decimal
    max_drawdown_date: Optional[datetime]
    current_drawdown_percent: Decimal
    
    # Win/loss analysis
    winning_trades: int
    losing_trades: int
    win_rate_percent: Decimal
    avg_win_percent: Decimal
    avg_loss_percent: Decimal
    profit_factor: Optional[Decimal]
    
    # Monthly breakdown
    monthly_returns: List[dict] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class RebalanceRecommendation(BaseModel):
    """Model for portfolio rebalancing recommendations."""
    
    coin: str
    current_allocation_percent: Decimal
    target_allocation_percent: Decimal
    recommended_action: str  # 'buy', 'sell', 'hold'
    recommended_amount_usd: Decimal
    priority: int  # 1 = high, 5 = low
    reason: str
    
    class Config:
        from_attributes = True


class PortfolioRebalance(BaseModel):
    """Model for portfolio rebalancing plan."""
    
    total_portfolio_value_usd: Decimal
    cash_available_usd: Decimal
    rebalance_threshold_percent: Decimal = Field(default=Decimal("0.05"))  # 5% threshold
    
    recommendations: List[RebalanceRecommendation]
    total_trades_needed: int
    estimated_cost_usd: Decimal
    
    # Execution status
    status: str = "pending"  # pending, executing, completed, failed
    created_at: datetime
    
    class Config:
        from_attributes = True


class SpotSavings(BaseModel):
    """Model for spot savings accumulation tracking."""
    
    id: UUID
    coin: str
    
    amount: Decimal
    price_usd: Decimal
    value_usd: Decimal
    
    source_type: str  # 'profit_skim', 'manual_deposit'
    source_position_id: Optional[UUID]
    
    created_at: datetime
    
    class Config:
        from_attributes = True


class SpotSavingsSummary(BaseModel):
    """Model for spot savings summary by coin."""
    
    coin: str
    total_amount: Decimal
    total_value_usd: Decimal
    average_price: Decimal
    entry_count: int
    first_entry_date: datetime
    last_entry_date: datetime
    
    class Config:
        from_attributes = True
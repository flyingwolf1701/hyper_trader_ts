-- Initial database schema for HyperTrader
-- Creates all core tables for trading plans, positions, portfolio management, and logging

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Trading plans table
CREATE TABLE trading_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coin VARCHAR(10) NOT NULL,
    strategy VARCHAR(50) NOT NULL DEFAULT 'fibonacci_hedging',
    
    -- Fibonacci levels configuration
    retracement_23_percent DECIMAL(5,4) NOT NULL DEFAULT 0.2300,
    retracement_38_percent DECIMAL(5,4) NOT NULL DEFAULT 0.3800,
    retracement_50_percent DECIMAL(5,4) NOT NULL DEFAULT 0.5000,
    
    -- Risk management parameters
    max_drawdown_percent DECIMAL(5,4) NOT NULL DEFAULT 0.2300,
    stop_loss_percent DECIMAL(5,4) NOT NULL DEFAULT 0.0500,
    take_profit_percent DECIMAL(5,4) NULL,
    
    -- Position sizing
    position_size_usd DECIMAL(15,2) NOT NULL,
    max_position_count INTEGER NOT NULL DEFAULT 1,
    
    -- Hedging configuration
    hedge_ratio DECIMAL(5,4) NOT NULL DEFAULT 0.5000, -- 50% hedge at 23% retracement
    scaling_enabled BOOLEAN NOT NULL DEFAULT true,
    
    -- Status and metadata
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_percentages CHECK (
        retracement_23_percent > 0 AND retracement_23_percent < 1 AND
        retracement_38_percent > 0 AND retracement_38_percent < 1 AND
        retracement_50_percent > 0 AND retracement_50_percent < 1 AND
        max_drawdown_percent > 0 AND max_drawdown_percent < 1
    ),
    CONSTRAINT valid_position_size CHECK (position_size_usd > 0),
    CONSTRAINT valid_retracement_order CHECK (
        retracement_23_percent < retracement_38_percent AND
        retracement_38_percent < retracement_50_percent
    )
);

-- Positions table for tracking individual trade entries
CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trading_plan_id UUID NOT NULL REFERENCES trading_plans(id),
    
    -- Position details
    coin VARCHAR(10) NOT NULL,
    side VARCHAR(10) NOT NULL CHECK (side IN ('long', 'short')),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'hedged', 'scaled', 'closed')),
    
    -- Entry information
    entry_price DECIMAL(15,8) NOT NULL,
    entry_quantity DECIMAL(15,8) NOT NULL,
    entry_value_usd DECIMAL(15,2) NOT NULL,
    entry_timestamp TIMESTAMP NOT NULL,
    
    -- Position tracking
    highest_price DECIMAL(15,8) NULL, -- Track highest price since entry for longs
    lowest_price DECIMAL(15,8) NULL,  -- Track lowest price since entry for shorts
    current_price DECIMAL(15,8) NULL,
    
    -- Fibonacci levels (calculated dynamically but cached)
    fib_23_price DECIMAL(15,8) NULL,
    fib_38_price DECIMAL(15,8) NULL,
    fib_50_price DECIMAL(15,8) NULL,
    
    -- P&L tracking
    unrealized_pnl_usd DECIMAL(15,2) NULL,
    realized_pnl_usd DECIMAL(15,2) NOT NULL DEFAULT 0,
    
    -- Exit information (when position is closed)
    exit_price DECIMAL(15,8) NULL,
    exit_quantity DECIMAL(15,8) NULL,
    exit_timestamp TIMESTAMP NULL,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_quantities CHECK (entry_quantity > 0),
    CONSTRAINT valid_prices CHECK (entry_price > 0),
    CONSTRAINT valid_exit_data CHECK (
        (status = 'closed' AND exit_price IS NOT NULL AND exit_quantity IS NOT NULL) OR
        (status != 'closed' AND exit_price IS NULL AND exit_quantity IS NULL)
    )
);

-- Portfolio allocations table
CREATE TABLE portfolio_allocations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coin VARCHAR(10) NOT NULL UNIQUE,
    
    -- Allocation settings
    target_allocation_percent DECIMAL(5,4) NOT NULL,
    max_allocation_percent DECIMAL(5,4) NOT NULL,
    min_allocation_percent DECIMAL(5,4) NOT NULL DEFAULT 0,
    
    -- Current status
    current_allocation_percent DECIMAL(5,4) NOT NULL DEFAULT 0,
    current_value_usd DECIMAL(15,2) NOT NULL DEFAULT 0,
    
    -- Cash management
    cash_reserve_percent DECIMAL(5,4) NOT NULL DEFAULT 0.1000, -- 10% cash reserve
    spot_savings_enabled BOOLEAN NOT NULL DEFAULT false,
    spot_savings_percent DECIMAL(5,4) NOT NULL DEFAULT 0.0500, -- 5% to spot savings
    
    -- Status
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_allocation_percents CHECK (
        target_allocation_percent > 0 AND target_allocation_percent <= 1 AND
        max_allocation_percent >= target_allocation_percent AND
        min_allocation_percent >= 0 AND min_allocation_percent <= target_allocation_percent
    ),
    CONSTRAINT valid_cash_settings CHECK (
        cash_reserve_percent >= 0 AND cash_reserve_percent < 1 AND
        spot_savings_percent >= 0 AND spot_savings_percent < 1
    )
);

-- Execution logs table for complete audit trail
CREATE TABLE execution_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Related entities
    trading_plan_id UUID REFERENCES trading_plans(id),
    position_id UUID REFERENCES positions(id),
    
    -- Action details
    action_type VARCHAR(50) NOT NULL, -- 'entry', 'hedge', 'scale', 'exit', 'stop_loss', etc.
    coin VARCHAR(10) NOT NULL,
    side VARCHAR(10) NOT NULL CHECK (side IN ('buy', 'sell')),
    
    -- Trade execution
    price DECIMAL(15,8) NOT NULL,
    quantity DECIMAL(15,8) NOT NULL,
    value_usd DECIMAL(15,2) NOT NULL,
    
    -- Context information
    reason TEXT NULL, -- Why this action was taken
    fibonacci_level DECIMAL(5,4) NULL, -- Which Fibonacci level triggered this
    
    -- Execution status
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'executed', 'failed', 'cancelled')),
    exchange_order_id VARCHAR(100) NULL, -- External order ID
    error_message TEXT NULL,
    
    -- Metadata
    executed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_trade_data CHECK (price > 0 AND quantity > 0 AND value_usd > 0)
);

-- Spot savings table for long-term accumulation tracking
CREATE TABLE spot_savings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coin VARCHAR(10) NOT NULL,
    
    -- Accumulation details
    amount DECIMAL(15,8) NOT NULL,
    price_usd DECIMAL(15,8) NOT NULL,
    value_usd DECIMAL(15,2) NOT NULL,
    
    -- Source information
    source_type VARCHAR(20) NOT NULL CHECK (source_type IN ('profit_skim', 'manual_deposit')),
    source_position_id UUID REFERENCES positions(id),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_accumulation_data CHECK (amount > 0 AND price_usd > 0 AND value_usd > 0)
);

-- Market data cache for recent price history
CREATE TABLE market_data_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coin VARCHAR(10) NOT NULL,
    
    -- OHLCV data
    open_price DECIMAL(15,8) NOT NULL,
    high_price DECIMAL(15,8) NOT NULL,
    low_price DECIMAL(15,8) NOT NULL,
    close_price DECIMAL(15,8) NOT NULL,
    volume DECIMAL(20,8) NOT NULL,
    
    -- Time information
    interval_type VARCHAR(10) NOT NULL, -- '1m', '5m', '1h', '1d'
    timestamp TIMESTAMP NOT NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_ohlc CHECK (
        open_price > 0 AND high_price > 0 AND 
        low_price > 0 AND close_price > 0 AND
        high_price >= low_price
    ),
    CONSTRAINT unique_market_data UNIQUE (coin, interval_type, timestamp)
);

-- Indexes for performance
CREATE INDEX idx_trading_plans_coin_active ON trading_plans(coin, is_active);
CREATE INDEX idx_positions_trading_plan ON positions(trading_plan_id);
CREATE INDEX idx_positions_coin_status ON positions(coin, status);
CREATE INDEX idx_positions_created_at ON positions(created_at DESC);
CREATE INDEX idx_execution_logs_position ON execution_logs(position_id);
CREATE INDEX idx_execution_logs_created_at ON execution_logs(created_at DESC);
CREATE INDEX idx_portfolio_allocations_active ON portfolio_allocations(is_active);
CREATE INDEX idx_spot_savings_coin ON spot_savings(coin);
CREATE INDEX idx_market_data_coin_timestamp ON market_data_cache(coin, timestamp DESC);

-- Update timestamp triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_trading_plans_updated_at 
    BEFORE UPDATE ON trading_plans 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_positions_updated_at 
    BEFORE UPDATE ON positions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_portfolio_allocations_updated_at 
    BEFORE UPDATE ON portfolio_allocations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
# Fibonacci Hedging Trading Strategy

## Executive Summary
A dynamic position management system that uses position-relative Fibonacci retracements with built-in hedging to minimize drawdowns and capitalize on market volatility while letting winners run.

## Core Principle
**Note**: Position sizes are percentage-based, not fixed token amounts. Example: $10,000 investment.

- **Target Position**: 50% of available capital ($5,000 worth of tokens)
- **Working Position**: 100% of available capital ($10,000 worth of tokens at 5x-10x leverage)
- **Portfolio Management**: Flexible allocation system supporting 1-20 positions with automatic cash management
- **Allocation Control**: User-defined percentage allocation per coin with rebalancing options
- **Cash Management**: Configurable cash reserve (default 10%) maintained through profit skimming
- **Risk Management**: Dynamic hedging through short positions during pullbacks
- **Profit Optimization**: Let winners run while hedging against pullbacks to capture 77%+ of unrealized gains

## Initial Setup Phase

### 1. Fibonacci Level Calculation
**User Input Required:**
- Last fractal high price
- Last fractal low price
- Desired entry point

**App Calculates (Position-Relative):**
- 23.6% retracement level (pullback of position gains)
- 38.2% retracement level (pullback of position gains)
- 50.0% retracement level (pullback of position gains)
- 61.8% retracement level (pullback of position gains)

### 2. Position Initialization
- **Purchase**: 100% of allocated capital using 5x-10x leverage at chosen entry point
- **Calculate**: Average purchase price (becomes 0% baseline anchor point)
- **Set**: Initial stop loss at user-defined percentage (default: -23%) from average purchase price
- **Dynamic Stop Loss**: Automatically adjusts upward as price increases

## Dynamic Management Rules

### Market Thesis Configuration
**User Input Required:**
- **Market Thesis**: Bull or Bear market expectation
- **Bull Market**: Shorts are protective hedges (strategy below)
- **Bear Market**: Strategy inverted - start with shorts, hedge with longs
- **Current Focus**: Bull market thesis implementation

### Pullback Protection Protocol - Bull Thesis

#### Hedge Trigger (23% Retracement from Position High):
1. **Track Position High**: Monitor the highest price reached since position entry (not historical highs)
2. **Calculate 23% Pullback**: 23% of total position gains (not 23% of price)
3. **Execute Hedge**: When 23% retracement is hit:
   - **Sell**: 50% of position (half of holdings)
   - **Short**: Equal amount at market price
   - **Net Position**: 50% long + 50% short = market neutral
   - **Short Stop Loss**: User-configurable options:
     - **Default**: 23% above short entry (matches pullback trigger)
     - **Conservative Preset**: 11.5% above short entry (tighter risk control)
     - **Custom**: User-defined percentage within safe range (5-30%)
     - **Real-time Adjustment**: Can be modified during active trades
   - **Effect**: Protected from further downside, maintains upside exposure
   - **Auto Re-entry**: If short is stopped out, automatically re-enter long position at market price

#### Long Position Scaling (38% Retracement):
- **Scale Out Trigger**: When price hits 38% retracement of position gains
- **Action**: Begin scaling out of remaining 50% long tokens
- **Tracking**: Continuously monitor and update the lowest low as price declines

### Maximum Drawdown Analysis (Default Settings)
**Scenario: Short Stop Out**
- **Position Entry**: $100 (0% baseline)
- **Position High**: $130 (100% = $30 total gain)
- **23% Pullback**: 23% of $30 gain = $6.90 pullback
- **Hedge Trigger**: $130 - $6.90 = **$123.10**
- **Captured Gain**: $23.10 out of $30 move (**77%** of the upside)
- **Hedge Execution**: 50% long + 50% short at $123.10
- **Short Stop Loss**: $141.81 (23% above $123.10 short entry)

**When Short Gets Stopped Out:**
- **Remaining 50% Long**: Gains from $123.10 to $141.81
- **Short Position**: Loses from $123.10 to $141.81  
- **Net Hedge Effect**: Approximately breaks even
- **Maximum Drawdown**: 23% from peak ($130 to $123.10)

**Key Insight**: The strategy captures **77%** of upward moves while capping maximum drawdown at 23% from the peak. This creates an asymmetric risk/reward profile where the system adapts to YOUR position gains, not arbitrary market levels.

### Trend Analysis & Fractal Reset

#### Trend Determination:
- **Monitor**: Price action relative to fractal highs/lows
- **Trend States**: Up, Down, or Sideways
- **Reset Trigger**: When trend definitively shifts to DOWN

#### Downtrend Management:
1. **Fractal Reset**: Establish new high/low fractal points
2. **Short Riding**: Allow short position to ride to ~50% retracement
3. **Partial Cover**: Buy back tokens at 50% retracement level
4. **Short Optimization**: Continue short position seeking better exit levels

#### Short-to-Long Transition:
- **Lowest Low Tracking**: Continuously update lowest point reached
- **Reversal Detection**: Look for signs of trend shift from down to up
- **Mirror Strategy**: Apply same 23% retracement logic but in reverse
  - When price rallies 23% from lowest low, begin transitioning shorts back to longs
  - Scale back into long positions as uptrend confirms

## Risk Management Framework

### Dynamic Stop Loss System
**Initial Setup:**
- **Base Stop Loss**: User-configurable percentage (default: -23%) from average purchase price
- **Example**: Purchase at $100, initial stop loss at $77 (max loss: $23)

**Dynamic Adjustment Rules:**
1. **Breakeven Milestone**: When price rises enough to move stop to breakeven ($100)
   - **Max Loss**: Reduced from $23 to $0
2. **Trailing Stop Logic**: Stop loss moves up proportionally with price
   - **Example**: Price up 5% → Stop loss moves up 5%
   - **New Price**: $105 → **New Stop**: $82 (still -23% from new level)
3. **User Customization**: 
   - **Negative Stop %**: Adjustable downside protection
   - **Positive Stop %**: Optional upside protection for profit taking
   - **Risk/Reward Ratios**: Configure 1:2, 1:3, or custom ratios

**Advanced Stop Loss Examples:**
- **Scenario**: User changes stop to -10% when price is up 5%
- **Calculation**: New stop = $105 × 0.90 = $94.50
- **Result**: Stop moved from $82 to $94.50 (reduced risk, locked in gains)

### Portfolio Allocation System
**Watchlist Management:**
- **Single Coin Option**: Use strategy on just BTC, ETH, or any individual asset
- **Multi-Coin Portfolio**: Define percentage allocation for each coin (e.g., 40% BTC, 30% ETH, 20% SOL, 10% cash)
- **Local Compounding**: Profits compound within each coin's allocation initially
- **Graceful Exit**: Set any coin to 0% allocation to wind down position and reallocate

**Dynamic Rebalancing:**
- **Natural Drift**: Allow successful coins to grow their portfolio percentage
- **Manual Rebalancing**: Adjust allocations based on performance or market conditions  
- **Replacement Strategy**: Remove underperforming coins and add new opportunities

**Cash Management System:**
- **Target Cash Reserve**: Configurable percentage (default: 10%)
- **Profit Skimming**: When taking profits, reserve specified percentage as cash before reinvesting
- **Spot Savings**: Allocate percentage of profits to long-term spot accumulation (separate from trading portfolio)
- **Example Processing Order**: 
  1. Take profits from position
  2. Reserve cash percentage if below target (e.g., 10%)
  3. Allocate spot savings percentage (e.g., 15% to BTC spot)
  4. Reinvest remainder into active trading position
- **Flexibility**: All percentages user-configurable

### Spot Savings Feature
**Long-term Accumulation Strategy:**
- **Purpose**: Build long-term holdings separate from active trading portfolio
- **Trigger**: Activated during profit-taking events (especially at 50% retracement reinvestment)
- **Target Assets**: Typically blue-chip coins like BTC, ETH for long-term holding
- **Hold Strategy**: Accumulate continuously, only sell at extreme market peaks

**Configuration Options:**
- **Spot Percentage**: User-defined portion of profits allocated to spot savings (e.g., 15%)
- **Target Coin**: Choose which coin to accumulate (can be different from trading pair)
- **Accumulation Mode**: Dollar-cost average into spot positions over time
- **Separation**: Spot savings tracked separately from active trading portfolio

**Example Profit Processing:**
```
Total Profit: $1,000
1. Cash Reserve (10%): $100 (if below target)
2. Spot Savings (15%): $150 → Buy BTC spot
3. Reinvestment (75%): $750 → Back into active position
```

## Implementation Requirements for HyperTrader

### Core Calculations & Portfolio Logic
```python
def calculate_position_fibonacci_levels(entry_price, position_high):
    """Calculate Fibonacci levels based on position gains, not absolute price"""
    total_gain = position_high - entry_price
    return {
        'level_236': position_high - (total_gain * 0.236),  # 23.6% pullback of gains
        'level_382': position_high - (total_gain * 0.382),  # 38.2% pullback of gains  
        'level_500': position_high - (total_gain * 0.500),  # 50% pullback of gains
        'level_618': position_high - (total_gain * 0.618)   # 61.8% pullback of gains
    }

def calculate_average_price(positions):
    total_cost = sum(pos.quantity * pos.price for pos in positions)
    total_quantity = sum(pos.quantity for pos in positions)
    return total_cost / total_quantity

def calculate_stop_loss(avg_price, stop_percent=-0.23):
    return avg_price * (1 + stop_percent)

def process_profit_taking_with_savings(coin, profit_amount):
    """Process profits with cash management and spot savings"""
    current_cash_percentage = calculate_cash_percentage()
    target_cash_percentage = user_config.cash_target  # default 10%
    spot_savings_percentage = user_config.spot_savings_target  # default 0%
    
    # Calculate allocations
    cash_reserve = 0
    spot_savings = 0
    
    # First priority: Cash reserve if below target
    if current_cash_percentage < target_cash_percentage:
        cash_reserve = profit_amount * (target_cash_percentage / 100)
    
    # Second priority: Spot savings
    if spot_savings_percentage > 0:
        spot_savings = profit_amount * (spot_savings_percentage / 100)
    
    # Remainder goes to reinvestment
    reinvest_amount = profit_amount - cash_reserve - spot_savings
    
    # Execute spot purchase if configured
    if spot_savings > 0:
        target_spot_coin = user_config.spot_savings_coin  # e.g., 'BTC'
        purchase_spot(target_spot_coin, spot_savings)
    
    return cash_reserve, spot_savings, reinvest_amount

def graceful_coin_exit(coin_symbol):
    # Set allocation to 0%
    # Close positions systematically 
    # Redistribute capital to remaining allocations
    pass
```

### Automated Logic Requirements
1. **Position High Tracking**: Continuously monitor highest price since entry
2. **23% Retracement Detection**: Trigger hedge when price drops 23% of position gains
3. **38% Scaling Logic**: Begin scaling out of longs at 38% retracement of gains
4. **Trend Analysis**: Determine if market is up, down, or sideways trending
5. **Fractal Reset**: Update fractal levels when trend definitively shifts
6. **Lowest Low Tracking**: Monitor deepest retracement points
7. **Short-to-Long Reversal**: Mirror the hedging strategy for trend reversals
8. **Dynamic Position Management**: Maintain optimal risk/reward balance
9. **Portfolio Rebalancing**: Manage multiple positions and cash reserves
10. **Spot Savings Execution**: Automatic long-term accumulation purchases

### Key Monitoring Metrics
- Current position high since entry
- Current retracement percentage of position gains
- Trend direction (up/down/sideways)
- Current net long/short exposure per position
- Lowest low reached during downtrend
- Active position sizes and average prices
- Portfolio allocation percentages
- Cash reserve levels
- Spot savings accumulation progress

## Analysis: Short Stop Loss Configuration

### Default Setting (23% above entry):
- **Logic**: Matches the pullback trigger that initiated the hedge
- **Risk**: Moderate - allows room for normal volatility
- **Benefit**: Consistent with overall strategy framework

### Conservative Preset (11.5% above entry):
- **Logic**: Tighter risk control for cautious traders
- **Risk**: Lower maximum loss but higher stop-out probability  
- **Benefit**: Better risk/reward ratio on successful shorts

### Custom Configuration:
- **Range**: 5-30% above short entry price
- **Real-time**: Adjustable during active trades
- **Protection**: Range limits prevent extreme settings
- **Flexibility**: Adapt to different market conditions and risk tolerance

## Strategy Benefits
- **Downside Protection**: Short hedges limit losses during pullbacks
- **Volatility Profit**: Make money on both up and down moves
- **Risk Minimization**: Never fully exposed to major market drops
- **Systematic Approach**: Removes emotion from position management
- **Flexible Scaling**: Adapts to different market conditions
- **Position-Relative**: All calculations based on YOUR entry and gains, not arbitrary levels
- **Long-term Wealth Building**: Automatic spot savings creates forced accumulation

## Example Scenario: Complete Cycle

### Uptrend Phase
1. **Entry**: Buy $10,000 worth of ETH at $100 (position baseline: 0%)
2. **Setup**: Track position high as price rises
3. **New High**: ETH reaches $130 (position gain: 100% = $30 per token)

### Hedge Activation
4. **23% Retracement**: ETH drops to $123.10 (23% of $30 gain = $6.90 pullback)
5. **Execute Hedge**: 
   - Sell 50% of ETH at $123.10
   - Short equal amount at $123.10
   - Net position: 50% long + 50% short

### Scaling Out
6. **38% Retracement**: ETH falls to $118.60 (38% of $30 gain = $11.40 pullback)
7. **Scale Long**: Begin selling remaining 50% long ETH as price declines
8. **Track Lowest Low**: Monitor deepest point (e.g., $115 = 50% retracement)

### Trend Shift Detection
9. **Trend Analysis**: Price action confirms downtrend
10. **Fractal Reset**: New position high = $130, new fractal low = $115
11. **Short Management**: Allow short to ride toward deeper levels
12. **Profit Taking**: Take profits on shorts, begin building new long positions

### Reversal Preparation
13. **Monitor Upside**: Watch for 23% rally from lowest low
14. **Reversal Trigger**: Begin transitioning back to long bias
15. **Spot Savings**: Allocate portion of profits to BTC accumulation
16. **New Cycle**: Reset strategy for next uptrend phase

This approach captures the majority of profits in both directions while maintaining controlled risk through systematic position management and building long-term wealth through forced savings.
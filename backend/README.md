# HyperTrader Backend

Python FastAPI backend for the HyperTrader Fibonacci hedging trading system.

## Features

- **FastAPI** - Modern async Python web framework
- **PostgreSQL** - Database with asyncpg for async operations
- **UV** - Fast Python package manager
- **Structured Logging** - Using structlog
- **WebSocket Support** - Real-time market data integration
- **Pydantic Models** - Type-safe data validation
- **Database Migrations** - Automated schema management

## Quick Start

### Prerequisites

- Python 3.13+
- UV package manager
- PostgreSQL database (Neon or local)

### Installation

1. Install dependencies with UV:
   ```bash
   cd backend
   uv install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. Run database migrations:
   ```bash
   uv run python -c "from src.database.connection import run_migrations; import asyncio; asyncio.run(run_migrations())"
   ```

4. Start the development server:
   ```bash
   uv run python src/main.py
   ```

The API will be available at http://localhost:3000

## API Documentation

- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc

## Project Structure

```
backend/
├── src/
│   ├── main.py                 # FastAPI application entry
│   ├── api/                    # API endpoints
│   │   ├── trading_plans.py    # Trading plan CRUD
│   │   ├── portfolio.py        # Portfolio management
│   │   ├── positions.py        # Position monitoring
│   │   └── market_data.py      # WebSocket market data
│   ├── models/                 # Pydantic data models
│   │   ├── trading_plan.py     # Trading strategy models
│   │   ├── position.py         # Position tracking models
│   │   └── portfolio.py        # Portfolio allocation models
│   ├── database/               # Database layer
│   │   ├── connection.py       # PostgreSQL connection
│   │   ├── migrations/         # SQL migration files
│   │   └── repositories/       # Data access layer
│   ├── services/               # Business logic
│   │   ├── websocket_manager.py     # WebSocket connections
│   │   ├── execution_engine.py      # Trading execution
│   │   └── hyperliquid_client.py    # Exchange integration
│   └── calculators/            # Fibonacci calculations
│       ├── fibonacci.py        # Position-relative levels
│       └── position_sizing.py  # Risk management
├── tests/                      # Test files
├── pyproject.toml             # UV project configuration
└── README.md                  # This file
```

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run ruff format src/
uv run ruff check src/
```

### Type Checking

```bash
uv run mypy src/
```

## Database Schema

The system uses PostgreSQL with the following core tables:

- `trading_plans` - Fibonacci hedging strategy configurations
- `positions` - Individual trade entries and tracking
- `portfolio_allocations` - Coin allocation percentages
- `execution_logs` - Complete audit trail of all trades
- `spot_savings` - Long-term accumulation tracking
- `market_data_cache` - Recent price history

## Environment Variables

Key environment variables for configuration:

```bash
# Database (required)
DATABASE_URL=postgresql://user:pass@host:port/db
# or individual components:
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=hyper_trader
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password

# Development
ENVIRONMENT=development
LOG_LEVEL=info
```

## API Endpoints

### Trading Plans
- `POST /api/v1/trading-plans` - Create new plan
- `GET /api/v1/trading-plans` - List all plans
- `GET /api/v1/trading-plans/{id}` - Get specific plan
- `PUT /api/v1/trading-plans/{id}` - Update plan
- `DELETE /api/v1/trading-plans/{id}` - Delete plan

### Positions
- `GET /api/v1/positions` - List active positions
- `GET /api/v1/positions/{id}` - Get position details
- `GET /api/v1/positions/{id}/fibonacci` - Get Fibonacci levels
- `POST /api/v1/positions/{id}/close` - Close position

### Portfolio
- `GET /api/v1/portfolio/overview` - Portfolio summary
- `GET /api/v1/portfolio/allocations` - Allocation settings
- `POST /api/v1/portfolio/rebalance` - Trigger rebalancing

### Market Data
- `GET /api/v1/market-data/price/{coin}` - Current price
- `GET /api/v1/market-data/prices` - Multiple prices
- `WS /api/v1/market-data/ws/{coin}` - Real-time price feed

## License

MIT License - see LICENSE file for details.
"""
WebSocket manager for HyperLiquid market data connections.
"""

import asyncio
import json
from typing import Dict, Set, Optional, Callable, Any
import websockets
import structlog

logger = structlog.get_logger(__name__)


class WebSocketManager:
    """Manages WebSocket connections for real-time market data."""
    
    def __init__(self):
        self.connections: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.subscriptions: Dict[str, Set[str]] = {}  # coin -> set of connection_ids
        self.hyperliquid_ws: Optional[websockets.WebSocketClientProtocol] = None
        self.is_running: bool = False
        self.price_callbacks: Dict[str, Callable[[str, dict], None]] = {}
    
    async def start(self):
        """Start the WebSocket manager and connect to HyperLiquid."""
        if self.is_running:
            return
        
        logger.info("Starting WebSocket manager")
        self.is_running = True
        
        # TODO: Connect to actual HyperLiquid WebSocket
        # For now, this is a placeholder
        logger.info("WebSocket manager started (placeholder implementation)")
    
    async def close(self):
        """Close all WebSocket connections."""
        logger.info("Closing WebSocket manager")
        self.is_running = False
        
        # Close HyperLiquid connection
        if self.hyperliquid_ws:
            await self.hyperliquid_ws.close()
            self.hyperliquid_ws = None
        
        # Close all client connections
        for connection_id, websocket in self.connections.items():
            try:
                await websocket.close()
            except Exception as e:
                logger.warning("Error closing WebSocket connection", connection_id=connection_id, error=str(e))
        
        self.connections.clear()
        self.subscriptions.clear()
        self.price_callbacks.clear()
        
        logger.info("WebSocket manager closed")
    
    async def connect_to_hyperliquid(self):
        """Connect to HyperLiquid WebSocket feed."""
        # TODO: Implement actual HyperLiquid WebSocket connection
        # Placeholder implementation
        logger.info("Connecting to HyperLiquid WebSocket (placeholder)")
        pass
    
    async def subscribe_to_coin(self, coin: str, connection_id: str):
        """Subscribe a connection to price updates for a specific coin."""
        if coin not in self.subscriptions:
            self.subscriptions[coin] = set()
        
        self.subscriptions[coin].add(connection_id)
        logger.info("WebSocket subscription added", coin=coin, connection_id=connection_id)
        
        # TODO: Send subscription request to HyperLiquid
        # For now, this is a placeholder
    
    async def unsubscribe_from_coin(self, coin: str, connection_id: str):
        """Unsubscribe a connection from price updates for a specific coin."""
        if coin in self.subscriptions:
            self.subscriptions[coin].discard(connection_id)
            
            # Remove empty subscription sets
            if not self.subscriptions[coin]:
                del self.subscriptions[coin]
                # TODO: Send unsubscription request to HyperLiquid
        
        logger.info("WebSocket subscription removed", coin=coin, connection_id=connection_id)
    
    async def add_connection(self, connection_id: str, websocket: websockets.WebSocketServerProtocol):
        """Add a new WebSocket connection."""
        self.connections[connection_id] = websocket
        logger.info("WebSocket connection added", connection_id=connection_id)
    
    async def remove_connection(self, connection_id: str):
        """Remove a WebSocket connection and clean up subscriptions."""
        if connection_id in self.connections:
            del self.connections[connection_id]
        
        # Clean up subscriptions
        coins_to_remove = []
        for coin, connection_ids in self.subscriptions.items():
            connection_ids.discard(connection_id)
            if not connection_ids:
                coins_to_remove.append(coin)
        
        for coin in coins_to_remove:
            del self.subscriptions[coin]
        
        logger.info("WebSocket connection removed", connection_id=connection_id)
    
    async def broadcast_price_update(self, coin: str, price_data: dict):
        """Broadcast price update to all subscribers of a coin."""
        if coin not in self.subscriptions:
            return
        
        message = {
            "type": "price_update",
            "coin": coin,
            "data": price_data
        }
        
        # Send to all subscribers
        disconnected_connections = []
        
        for connection_id in self.subscriptions[coin]:
            if connection_id in self.connections:
                try:
                    await self.connections[connection_id].send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    disconnected_connections.append(connection_id)
                except Exception as e:
                    logger.warning("Error sending price update", 
                                 connection_id=connection_id, error=str(e))
                    disconnected_connections.append(connection_id)
        
        # Clean up disconnected connections
        for connection_id in disconnected_connections:
            await self.remove_connection(connection_id)
    
    def add_price_callback(self, coin: str, callback: Callable[[str, dict], None]):
        """Add a callback function for price updates."""
        self.price_callbacks[coin] = callback
        logger.info("Price callback added", coin=coin)
    
    def remove_price_callback(self, coin: str):
        """Remove a price callback function."""
        if coin in self.price_callbacks:
            del self.price_callbacks[coin]
            logger.info("Price callback removed", coin=coin)
    
    async def process_hyperliquid_message(self, message: dict):
        """Process incoming message from HyperLiquid WebSocket."""
        # TODO: Implement actual message processing
        # This is a placeholder implementation
        
        try:
            # Example message structure (needs to match actual HyperLiquid format)
            if message.get("type") == "price":
                coin = message.get("coin")
                price_data = message.get("data", {})
                
                # Broadcast to subscribers
                await self.broadcast_price_update(coin, price_data)
                
                # Call registered callbacks
                if coin in self.price_callbacks:
                    try:
                        self.price_callbacks[coin](coin, price_data)
                    except Exception as e:
                        logger.error("Error in price callback", coin=coin, error=str(e))
                        
        except Exception as e:
            logger.error("Error processing HyperLiquid message", error=str(e))
    
    async def get_current_price(self, coin: str) -> Optional[dict]:
        """Get current price data for a coin."""
        # TODO: Implement actual price fetching
        # This is a placeholder implementation
        
        return {
            "coin": coin,
            "price": 0.0,
            "timestamp": "2025-01-01T00:00:00Z",
            "volume": 0.0,
            "24h_change": 0.0
        }
    
    def get_connection_count(self) -> int:
        """Get the number of active connections."""
        return len(self.connections)
    
    def get_subscription_count(self) -> int:
        """Get the total number of subscriptions."""
        return sum(len(connection_ids) for connection_ids in self.subscriptions.values())
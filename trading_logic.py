
import threading
from typing import Dict, Optional, Set
from dataclasses import dataclass
from enum import Enum

class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"

@dataclass
class Position:
    """Trading position"""
    symbol: str
    side: OrderType
    size: float
    entry_price: float
    entry_time: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

class TradingLogicManager:
    """Safe trading logic management"""
    
    def __init__(self):
        self.positions: Dict[str, Position] = {}
        self.orders: Dict[str, Dict] = {}
        self._positions_lock = threading.Lock()
        self._orders_lock = threading.Lock()
        self.max_positions = 5
        self.max_position_size = 0.2  # 20% of capital per position
        self.max_total_exposure = 1.0  # 100% of capital
    
    def can_open_position(self, symbol: str, side: OrderType, size: float, current_price: float) -> bool:
        """Check if position can be opened safely"""
        with self._positions_lock:
            # Check if already have position in this symbol
            if symbol in self.positions:
                return False
            
            # Check maximum positions
            if len(self.positions) >= self.max_positions:
                return False
            
            # Calculate total exposure
            total_exposure = sum(pos.size for pos in self.positions.values())
            if total_exposure + size > self.max_total_exposure:
                return False
            
            # Check position size
            if size > self.max_position_size:
                return False
            
            return True
    
    def open_position(self, symbol: str, side: OrderType, size: float, entry_price: float, entry_time: float) -> bool:
        """Open new position safely"""
        if not self.can_open_position(symbol, side, size, entry_price):
            return False
        
        with self._positions_lock:
            position = Position(
                symbol=symbol,
                side=side,
                size=size,
                entry_price=entry_price,
                entry_time=entry_time,
                stop_loss=entry_price * 0.95,  # 5% stop loss
                take_profit=entry_price * 1.10  # 10% take profit
            )
            
            self.positions[symbol] = position
            return True
    
    def close_position(self, symbol: str, exit_price: float, exit_time: float) -> Optional[float]:
        """Close position safely"""
        with self._positions_lock:
            position = self.positions.get(symbol)
            if not position:
                return None
            
            # Calculate P&L
            if position.side == OrderType.BUY:
                pnl = (exit_price - position.entry_price) * position.size
            else:
                pnl = (position.entry_price - exit_price) * position.size
            
            # Remove position
            del self.positions[symbol]
            return pnl
    
    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for symbol"""
        with self._positions_lock:
            return self.positions.get(symbol)
    
    def get_total_exposure(self) -> float:
        """Get total market exposure"""
        with self._positions_lock:
            return sum(pos.size for pos in self.positions.values())
    
    def validate_order(self, order: Dict) -> bool:
        """Validate order before execution"""
        required_fields = ['symbol', 'side', 'size', 'price']
        for field in required_fields:
            if field not in order:
                return False
        
        # Validate order type
        if order['side'] not in [OrderType.BUY.value, OrderType.SELL.value]:
            return False
        
        # Validate size
        if order['size'] <= 0 or order['size'] > self.max_position_size:
            return False
        
        # Validate price
        if order['price'] <= 0:
            return False
        
        return True

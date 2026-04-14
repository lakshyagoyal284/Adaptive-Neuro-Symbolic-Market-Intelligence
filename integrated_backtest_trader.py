"""
Integrated Backtest Trader
Combines our existing backtesting model with real market data
"""

import yfinance as yf
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
import time
import sys
import os
import warnings
warnings.filterwarnings('ignore')

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our existing backtesting components
try:
    import backtesting
    import symbolic_engine
    from symbolic_engine.decision_engine import DecisionEngine
    from symbolic_engine.market_intelligence import MarketIntelligence
except ImportError as e:
    print(f"Warning: Could not import backtesting components: {e}")
    # Fallback implementations
    backtesting = None

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntegratedBacktestTrader:
    """Integrated system combining backtesting with real market data"""
    
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
        self.backtest_results = []
        self.logger = logging.getLogger(__name__)
        
        # Define stock tickers
        self.tickers = [
            'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA',
            'META', 'NVDA', 'JPM', 'JNJ', 'V'
        ]
        
        # Initialize backtesting components if available
        self.decision_engine = None
        self.market_intelligence = None
        self.init_backtesting_components()
        
        print(f"Integrated Backtest Trader Initialized")
        print(f"Initial Capital: ${self.capital:,.2f}")
        print(f"Testing {len(self.tickers)} stocks with integrated model")
        
    def init_backtesting_components(self):
        """Initialize backtesting components"""
        try:
            if backtesting:
                self.decision_engine = DecisionEngine()
                self.market_intelligence = MarketIntelligence()
                print("Backtesting components loaded successfully")
            else:
                print("Using fallback trading logic")
        except Exception as e:
            self.logger.error(f"Error initializing backtesting: {e}")
            print(f"Error initializing backtesting: {e}")
    
    def get_real_market_data(self, ticker, period='1mo'):
        """Get real market data for analysis"""
        try:
            print(f"   Fetching real data for {ticker}...")
            stock = yf.Ticker(ticker)
            
            # Try different periods
            for p in ['1mo', '3mo', '6mo', '1y']:
                try:
                    data = stock.history(period=p, interval='1d')
                    if not data.empty and len(data) >= 50:
                        print(f"   Got {len(data)} days of data for {ticker}")
                        break
                except:
                    continue
            else:
                print(f"   No data available for {ticker}")
                return None
                
            return data
            
        except Exception as e:
            self.logger.error(f"Error getting data for {ticker}: {e}")
            return None
    
    def calculate_technical_indicators(self, data):
        """Calculate comprehensive technical indicators"""
        if data is None or len(data) < 20:
            return None
        
        # Basic indicators
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['EMA_12'] = data['Close'].ewm(span=12).mean()
        data['EMA_26'] = data['Close'].ewm(span=26).mean()
        
        # MACD
        data['MACD'] = data['EMA_12'] - data['EMA_26']
        data['MACD_Signal'] = data['MACD'].ewm(span=9).mean()
        data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']
        
        # RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        data['BB_Middle'] = data['Close'].rolling(window=20).mean()
        bb_std = data['Close'].rolling(window=20).std()
        data['BB_Upper'] = data['BB_Middle'] + (bb_std * 2)
        data['BB_Lower'] = data['BB_Middle'] - (bb_std * 2)
        
        # Additional indicators
        data['Volatility'] = data['Close'].pct_change().rolling(window=20).std() * 100
        data['Price_Change'] = data['Close'].pct_change() * 100
        data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
        
        # Stochastic
        low_min = data['Low'].rolling(window=14).min()
        high_max = data['High'].rolling(window=14).max()
        data['Stoch_K'] = 100 * (data['Close'] - low_min) / (high_max - low_min)
        data['Stoch_D'] = data['Stoch_K'].rolling(window=3).mean()
        
        return data
    
    def run_backtesting_analysis(self, ticker, data):
        """Run our existing backtesting analysis on real data"""
        try:
            if self.decision_engine and self.market_intelligence:
                # Use our existing backtesting components
                market_data = {
                    'price': data['Close'].iloc[-1],
                    'volume': data['Volume'].iloc[-1],
                    'sma_20': data['SMA_20'].iloc[-1],
                    'sma_50': data['SMA_50'].iloc[-1],
                    'rsi': data['RSI'].iloc[-1],
                    'macd': data['MACD'].iloc[-1],
                    'volatility': data['Volatility'].iloc[-1],
                    'price_change': data['Price_Change'].iloc[-1]
                }
                
                # Generate market intelligence
                intelligence = self.market_intelligence.analyze_market(market_data)
                
                # Make trading decision
                decision = self.decision_engine.make_decision(intelligence)
                
                return {
                    'ticker': ticker,
                    'price': market_data['price'],
                    'decision': decision,
                    'intelligence': intelligence,
                    'confidence': decision.get('confidence', 0.5),
                    'action': decision.get('action', 'HOLD'),
                    'reason': decision.get('reason', 'No clear signal')
                }
            else:
                # Fallback to our own analysis
                return self.analyze_with_indicators(ticker, data)
                
        except Exception as e:
            self.logger.error(f"Error in backtesting analysis: {e}")
            return self.analyze_with_indicators(ticker, data)
    
    def analyze_with_indicators(self, ticker, data):
        """Fallback analysis using technical indicators"""
        latest = data.iloc[-1]
        prev = data.iloc[-2] if len(data) > 1 else latest
        
        # Extract indicators
        price = latest['Close']
        sma_20 = latest['SMA_20']
        sma_50 = latest['SMA_50']
        rsi = latest['RSI']
        macd = latest['MACD']
        macd_signal = latest['MACD_Signal']
        bb_upper = latest['BB_Upper']
        bb_lower = latest['BB_Lower']
        stoch_k = latest['Stoch_K']
        stoch_d = latest['Stoch_D']
        volatility = latest['Volatility']
        price_change = latest['Price_Change']
        
        # Generate signals
        signals = []
        
        # SMA signals
        if price > sma_20 and sma_20 > sma_50:
            signals.append(('SMA', 'BUY', 0.7, f'Bullish SMA crossover'))
        elif price < sma_20 and sma_20 < sma_50:
            signals.append(('SMA', 'SELL', 0.7, f'Bearish SMA crossover'))
        
        # RSI signals
        if rsi < 30:
            signals.append(('RSI', 'BUY', 0.8, f'RSI oversold: {rsi:.1f}'))
        elif rsi > 70:
            signals.append(('RSI', 'SELL', 0.8, f'RSI overbought: {rsi:.1f}'))
        
        # MACD signals
        if macd > macd_signal and macd > 0:
            signals.append(('MACD', 'BUY', 0.6, f'Bullish MACD'))
        elif macd < macd_signal and macd < 0:
            signals.append(('MACD', 'SELL', 0.6, f'Bearish MACD'))
        
        # Bollinger Bands
        if price < bb_lower:
            signals.append(('BB', 'BUY', 0.7, f'Below lower BB'))
        elif price > bb_upper:
            signals.append(('BB', 'SELL', 0.7, f'Above upper BB'))
        
        # Stochastic
        if stoch_k < 20 and stoch_d < 20:
            signals.append(('Stoch', 'BUY', 0.6, f'Stoch oversold'))
        elif stoch_k > 80 and stoch_d > 80:
            signals.append(('Stoch', 'SELL', 0.6, f'Stoch overbought'))
        
        # Momentum
        if price_change > 2:
            signals.append(('Momentum', 'BUY', 0.5, f'Strong momentum: +{price_change:.1f}%'))
        elif price_change < -2:
            signals.append(('Momentum', 'SELL', 0.5, f'Strong downward momentum: {price_change:.1f}%'))
        
        # Determine overall action
        buy_signals = [s for s in signals if s[1] == 'BUY']
        sell_signals = [s for s in signals if s[1] == 'SELL']
        
        action = 'HOLD'
        confidence = 0.5
        reason = 'No clear signal'
        
        if len(buy_signals) > len(sell_signals):
            action = 'BUY'
            confidence = sum(s[2] for s in buy_signals) / len(buy_signals)
            reason = ', '.join([f"{s[0]}({s[2]:.1f})" for s in buy_signals])
        elif len(sell_signals) > len(buy_signals):
            action = 'SELL'
            confidence = sum(s[2] for s in sell_signals) / len(sell_signals)
            reason = ', '.join([f"{s[0]}({s[2]:.1f})" for s in sell_signals])
        
        return {
            'ticker': ticker,
            'price': price,
            'action': action,
            'confidence': confidence,
            'reason': reason,
            'signals': signals,
            'indicators': {
                'sma_20': sma_20, 'sma_50': sma_50, 'rsi': rsi,
                'macd': macd, 'volatility': volatility, 'price_change': price_change
            }
        }
    
    def execute_integrated_trade(self, analysis):
        """Execute trade based on integrated analysis"""
        if not analysis or analysis['action'] == 'HOLD':
            return None
        
        # Position sizing based on confidence
        risk_per_trade = 0.02 + (analysis['confidence'] - 0.5) * 0.02  # 1-3% risk
        position_size = self.capital * risk_per_trade
        shares = int(position_size / analysis['price'])
        
        if shares == 0:
            return None
        
        trade = {
            'timestamp': datetime.now(),
            'ticker': analysis['ticker'],
            'action': analysis['action'],
            'shares': shares,
            'price': analysis['price'],
            'value': shares * analysis['price'],
            'confidence': analysis['confidence'],
            'reason': analysis['reason'],
            'signals': analysis.get('signals', [])
        }
        
        # Execute trade
        if analysis['action'] == 'BUY':
            if analysis['ticker'] not in self.positions:
                self.positions[analysis['ticker']] = {
                    'shares': shares,
                    'avg_price': analysis['price'],
                    'total_cost': shares * analysis['price']
                }
                self.capital -= shares * analysis['price']
                trade['capital_change'] = -shares * analysis['price']
                trade['position_type'] = 'LONG'
                
        elif analysis['action'] == 'SELL':
            # For demo purposes, allow short selling
            if analysis['ticker'] not in self.positions:
                # Short sell
                self.positions[analysis['ticker']] = {
                    'shares': -shares,
                    'avg_price': analysis['price'],
                    'total_cost': shares * analysis['price']
                }
                self.capital += shares * analysis['price']  # Receive cash from short sale
                trade['capital_change'] = shares * analysis['price']
                trade['position_type'] = 'SHORT'
                trade['profit'] = 0  # No profit yet on short position
                trade['return_rate'] = 0
            else:
                # Close existing position
                position = self.positions[analysis['ticker']]
                sell_shares = min(shares, abs(position['shares']))
                sell_value = sell_shares * analysis['price']
                cost_basis = sell_shares * position['avg_price']
                
                if position['shares'] > 0:  # Long position
                    profit = sell_value - cost_basis
                else:  # Short position
                    profit = cost_basis - sell_value  # Profit from short selling
                
                self.capital += sell_value if position['shares'] > 0 else cost_basis
                self.positions[analysis['ticker']]['shares'] += (sell_shares if position['shares'] > 0 else -sell_shares)
                
                if self.positions[analysis['ticker']]['shares'] == 0:
                    del self.positions[analysis['ticker']]
                
                trade['shares'] = sell_shares
                trade['profit'] = profit
                trade['return_rate'] = (profit / cost_basis) * 100
                trade['capital_change'] = sell_value if position['shares'] > 0 else cost_basis
                trade['success'] = profit > 0
                trade['position_type'] = 'CLOSE'
        
        self.trades.append(trade)
        return trade
    
    def run_integrated_session(self):
        """Run integrated trading session"""
        print(f"\n{'='*80}")
        print(f"INTEGRATED BACKTEST TRADING SESSION")
        print(f"{'='*80}")
        print(f"Session Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Initial Capital: ${self.capital:,.2f}")
        print(f"{'='*80}")
        
        session_trades = []
        
        for ticker in self.tickers:
            print(f"\n{'-'*60}")
            print(f"ANALYZING {ticker}")
            print(f"{'-'*60}")
            
            # Get real market data
            data = self.get_real_market_data(ticker)
            if data is None:
                print(f"   No data available for {ticker}")
                continue
            
            # Calculate indicators
            data = self.calculate_technical_indicators(data)
            if data is None:
                print(f"   Could not calculate indicators for {ticker}")
                continue
            
            # Run backtesting analysis
            analysis = self.run_backtesting_analysis(ticker, data)
            if analysis is None:
                print(f"   Could not analyze {ticker}")
                continue
            
            # Display analysis
            print(f"   Current Price: ${analysis['price']:.2f}")
            if 'indicators' in analysis:
                ind = analysis['indicators']
                print(f"   SMA20: ${ind['sma_20']:.2f} | SMA50: ${ind['sma_50']:.2f}")
                print(f"   RSI: {ind['rsi']:.1f} | MACD: {ind['macd']:.3f}")
                print(f"   Volatility: {ind['volatility']:.2f}% | Change: {ind['price_change']:+.2f}%")
            
            print(f"   Action: {analysis['action']} (Confidence: {analysis['confidence']:.2f})")
            print(f"   Reason: {analysis['reason']}")
            
            if 'signals' in analysis and analysis['signals']:
                print(f"   Signals: {len(analysis['signals'])}")
                for sig_type, sig_action, sig_conf, sig_reason in analysis['signals']:
                    print(f"     {sig_type}: {sig_action} ({sig_conf:.1f}) - {sig_reason}")
            
            # Execute trade
            trade = self.execute_integrated_trade(analysis)
            if trade:
                session_trades.append(trade)
                print(f"\n   TRADE EXECUTED: {trade['action']} {trade['shares']} shares @ ${trade['price']:.2f}")
                print(f"   Confidence: {trade['confidence']:.2f}")
                print(f"   Reason: {trade['reason']}")
                
                if 'profit' in trade:
                    profit_color = "PROFIT" if trade['profit'] > 0 else "LOSS"
                    print(f"   {profit_color}: ${trade['profit']:.2f} ({trade['return_rate']:.2f}%)")
            else:
                print(f"   No trade executed")
            
            time.sleep(0.5)
        
        # Display session results
        self.display_session_results(session_trades)
        
        return session_trades
    
    def display_session_results(self, session_trades):
        """Display comprehensive session results in desired format"""
        print(f"\n{'='*80}")
        print(f"INTEGRATED SESSION RESULTS")
        print(f"{'='*80}")
        
        # Calculate metrics
        total_trades = len(session_trades)
        profitable_trades = len([t for t in session_trades if 'profit' in t and t['profit'] > 0])
        losing_trades = len([t for t in session_trades if 'profit' in t and t['profit'] <= 0])
        
        total_profit = sum(t.get('profit', 0) for t in session_trades)
        win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Calculate portfolio value with unrealized P/L
        portfolio_value = self.capital
        unrealized_pnl = 0
        
        for ticker, position in self.positions.items():
            if position['shares'] > 0:  # Long position
                position_value = position['shares'] * position['avg_price']
                portfolio_value += position_value
            else:  # Short position
                position_value = abs(position['shares']) * position['avg_price']
                # For short positions, we've already received cash
                portfolio_value += position_value
        
        total_return = ((portfolio_value - self.initial_capital) / self.initial_capital) * 100
        
        # Display in the desired format
        print(f"Total Trades: {total_trades}")
        print(f"Profitable Trades: {profitable_trades}")
        print(f"Losing Trades: {losing_trades}")
        print(f"Win Rate: {win_rate:.1f}%")
        print(f"Total P/L: ${total_profit:.2f}")
        print(f"Portfolio Value: ${portfolio_value:,.2f}")
        print(f"Total Return: {total_return:.2f}%")
        
        # Display positions
        if self.positions:
            print(f"\nOpen Positions:")
            for ticker, position in self.positions.items():
                value = position['shares'] * position['avg_price']
                print(f"   {ticker}: {position['shares']} shares @ ${position['avg_price']:.2f} (${value:,.2f})")
        
        # Performance rating
        if total_return > 5:
            print(f"\nEXCELLENT PERFORMANCE! +{total_return:.2f}% return")
        elif total_return > 0:
            print(f"\nGOOD PERFORMANCE! +{total_return:.2f}% return")
        else:
            print(f"\nNEGATIVE PERFORMANCE! {total_return:.2f}% return")
        
        print(f"{'='*80}")
        
        # Additional detailed metrics in desired format
        print(f"\nDETAILED PERFORMANCE METRICS:")
        print(f"{'-'*50}")
        
        # Trade breakdown
        if session_trades:
            print(f"Trade Breakdown:")
            for i, trade in enumerate(session_trades, 1):
                print(f"  Trade {i}: {trade['ticker']} {trade['action']} {trade['shares']} @ ${trade['price']:.2f}")
                if 'profit' in trade:
                    profit_status = "PROFIT" if trade['profit'] > 0 else "LOSS"
                    print(f"    {profit_status}: ${trade['profit']:.2f} ({trade.get('return_rate', 0):.2f}%)")
                print(f"    Confidence: {trade['confidence']:.2f}")
                print(f"    Reason: {trade['reason']}")
        
        # Portfolio details
        print(f"\nPortfolio Details:")
        print(f"Cash Available: ${self.capital:,.2f}")
        print(f"Open Positions Value: ${portfolio_value - self.capital:,.2f}")
        print(f"Total Portfolio: ${portfolio_value:,.2f}")
        
        # Performance metrics
        print(f"\nPerformance Analysis:")
        print(f"Return on Investment: {total_return:.2f}%")
        print(f"Trade Success Rate: {win_rate:.1f}%")
        print(f"Average Trade Size: ${sum(t.get('value', 0) for t in session_trades) / len(session_trades):,.2f}" if session_trades else "Average Trade Size: $0.00")
        print(f"Risk per Trade: {abs(total_profit / total_trades):.2f}" if total_trades > 0 else "Risk per Trade: $0.00")
        
        print(f"{'='*80}")

def main():
    """Main function"""
    try:
        print("INTEGRATED BACKTEST TRADING SYSTEM")
        print("="*80)
        print("Combining existing backtesting model with real market data")
        print("DISCLAIMER: Educational purposes only!")
        print("="*80)
        
        # Initialize integrated trader
        trader = IntegratedBacktestTrader(initial_capital=10000)
        
        # Run integrated session
        trades = trader.run_integrated_session()
        
        print(f"\nIntegrated session completed!")
        print(f"Total trades executed: {len(trades)}")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

"""
Indian Market Continuous Trader
Runs continuously until Indian market close (3:30 PM IST)
"""

import yfinance as yf
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
import time
import pytz
import warnings
warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IndianMarketTrader:
    """Continuous Indian market trading system"""
    
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
        self.session_trades = []
        self.market_open = False
        self.logger = logging.getLogger(__name__)
        
        # Define Indian stock tickers (with .NS suffix for NSE)
        self.tickers = [
            'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
            'HINDUNILVR.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'KOTAKBANK.NS', 'LT.NS'
        ]
        
        # Indian market hours (IST)
        self.market_open_time = 9.25  # 9:15 AM
        self.market_close_time = 15.5  # 3:30 PM
        
        print(f"Indian Market Trader Initialized")
        print(f"Initial Capital: ${self.capital:,.2f}")
        print(f"Trading {len(self.tickers)} Indian stocks")
        print(f"Market Hours: 9:15 AM - 3:30 PM IST")
    
    def is_market_open(self):
        """Check if Indian market is currently open"""
        try:
            # Get current time in IST
            ist = pytz.timezone('Asia/Kolkata')
            now = datetime.now(ist)
            current_time = now.hour + now.minute/60.0
            current_day = now.weekday()
            
            # Check if it's a weekday and within market hours
            if current_day < 5 and self.market_open_time <= current_time < self.market_close_time:
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking market hours: {e}")
            return False
    
    def get_market_data(self, ticker, period='5d'):
        """Get real market data for Indian ticker"""
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period, interval='1d')
            
            if data.empty or len(data) < 20:
                return None
                
            # Calculate technical indicators
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['RSI'] = self.calculate_rsi(data['Close'])
            data['Volatility'] = data['Close'].pct_change().rolling(window=20).std() * 100
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error getting data for {ticker}: {e}")
            return None
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def analyze_market_conditions(self, data, ticker):
        """Analyze market conditions and generate trading signals"""
        if data is None or len(data) < 20:
            return None
            
        latest = data.iloc[-1]
        prev = data.iloc[-2]
        
        # Get current price
        current_price = latest['Close']
        
        # Technical analysis
        sma_20 = latest['SMA_20']
        sma_50 = latest['SMA_50']
        rsi = latest['RSI']
        volatility = latest['Volatility']
        
        # Price change
        price_change = (current_price - prev['Close']) / prev['Close'] * 100
        
        # Generate trading signal
        signal = self.generate_trading_signal(current_price, sma_20, sma_50, rsi, volatility, price_change)
        
        analysis = {
            'ticker': ticker,
            'current_price': current_price,
            'sma_20': sma_20,
            'sma_50': sma_50,
            'rsi': rsi,
            'volatility': volatility,
            'price_change': price_change,
            'signal': signal,
            'confidence': signal['confidence'],
            'decision_type': signal['decision_type'],
            'decision_title': signal['title']
        }
        
        return analysis
    
    def generate_trading_signal(self, price, sma_20, sma_50, rsi, volatility, price_change):
        """Generate trading signal based on technical analysis"""
        
        # Initialize signal
        signal = {
            'action': 'HOLD',
            'confidence': 0.5,
            'decision_type': 'market_analysis',
            'title': 'Market Analysis - Hold Position'
        }
        
        # Strong buy signals for Indian market
        if (price > sma_20 and sma_20 > sma_50 and 
            rsi < 70 and rsi > 30 and volatility < 5 and price_change > 0.5):
            signal = {
                'action': 'BUY',
                'confidence': 0.8,
                'decision_type': 'momentum_buy',
                'title': f'Strong Buy - Momentum: {price_change:.2f}%, RSI: {rsi:.1f}'
            }
        
        # Buy signals
        elif (price > sma_20 and rsi < 60 and 
              price_change > 1.0 and volatility < 6):
            signal = {
                'action': 'BUY',
                'confidence': 0.7,
                'decision_type': 'breakout_buy',
                'title': f'Buy Breakout - Price: ${price:.2f}, Change: {price_change:.2f}%'
            }
        
        # Sell signals
        elif (price < sma_20 and rsi > 70 and volatility > 4):
            signal = {
                'action': 'SELL',
                'confidence': 0.7,
                'decision_type': 'overbought_sell',
                'title': f'Sell Overbought - RSI: {rsi:.1f}, Vol: {volatility:.1f}%'
            }
        
        # Strong sell signals
        elif (sma_20 < sma_50 and rsi > 65 and 
              price_change < -2.0 and volatility > 5):
            signal = {
                'action': 'SELL',
                'confidence': 0.8,
                'decision_type': 'downtrend_sell',
                'title': f'Strong Sell - Downtrend: {price_change:.2f}%'
            }
        
        return signal
    
    def execute_trade(self, ticker, signal, current_price):
        """Execute a trade based on signal"""
        
        if signal['action'] == 'HOLD':
            return None
        
        # Calculate position size (1% of capital per trade for continuous trading)
        position_size = self.capital * 0.01
        shares = int(position_size / current_price)
        
        if shares == 0:
            return None
        
        trade = {
            'timestamp': datetime.now(),
            'ticker': ticker,
            'action': signal['action'],
            'shares': shares,
            'price': current_price,
            'value': shares * current_price,
            'signal': signal['title'],
            'decision_type': signal['decision_type'],
            'confidence': signal['confidence']
        }
        
        # Execute trade
        if signal['action'] == 'BUY':
            if ticker not in self.positions:
                self.positions[ticker] = {
                    'shares': shares,
                    'avg_price': current_price,
                    'total_cost': shares * current_price
                }
                self.capital -= shares * current_price
                trade['capital_change'] = -shares * current_price
                
        elif signal['action'] == 'SELL':
            if ticker in self.positions:
                position = self.positions[ticker]
                sell_shares = min(shares, position['shares'])
                sell_value = sell_shares * current_price
                cost_basis = sell_shares * position['avg_price']
                profit = sell_value - cost_basis
                
                self.capital += sell_value
                self.positions[ticker]['shares'] -= sell_shares
                
                if self.positions[ticker]['shares'] <= 0:
                    del self.positions[ticker]
                
                trade['shares'] = sell_shares
                trade['profit'] = profit
                trade['return_rate'] = (profit / cost_basis) * 100
                trade['capital_change'] = sell_value
                trade['success'] = profit > 0
        
        # Record trade
        self.trades.append(trade)
        self.session_trades.append(trade)
        
        return trade
    
    def run_trading_cycle(self):
        """Run one complete trading cycle"""
        print(f"\n{'='*80}")
        print(f"TRADING CYCLE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST")
        print(f"{'='*80}")
        
        cycle_trades = []
        
        for ticker in self.tickers:
            print(f"\nAnalyzing {ticker}...")
            
            # Get market data
            data = self.get_market_data(ticker)
            if data is None:
                print(f"   No data available for {ticker}")
                continue
            
            # Analyze market conditions
            analysis = self.analyze_market_conditions(data, ticker)
            if analysis is None:
                print(f"   Could not analyze {ticker}")
                continue
            
            # Display analysis
            print(f"   Price: ${analysis['current_price']:.2f} ({analysis['price_change']:+.2f}%)")
            print(f"   SMA20: ${analysis['sma_20']:.2f} | SMA50: ${analysis['sma_50']:.2f}")
            print(f"   RSI: {analysis['rsi']:.1f} | Vol: {analysis['volatility']:.2f}%")
            print(f"   Signal: {analysis['signal']['action']} (Conf: {analysis['signal']['confidence']:.1f})")
            print(f"   Reason: {analysis['signal']['title']}")
            
            # Execute trade
            trade = self.execute_trade(ticker, analysis['signal'], analysis['current_price'])
            if trade:
                cycle_trades.append(trade)
                print(f"   TRADE EXECUTED: {trade['action']} {trade['shares']} shares @ ${trade['price']:.2f}")
                
                if 'profit' in trade:
                    profit_color = "PROFIT" if trade['profit'] > 0 else "LOSS"
                    print(f"   {profit_color}: ${trade['profit']:.2f} ({trade['return_rate']:.2f}%)")
            
            # Small delay to avoid rate limiting
            time.sleep(0.3)
        
        # Display cycle summary
        self.display_cycle_summary(cycle_trades)
        
        return cycle_trades
    
    def display_cycle_summary(self, cycle_trades):
        """Display summary of the trading cycle"""
        print(f"\nCYCLE SUMMARY:")
        print(f"Trades Executed: {len(cycle_trades)}")
        
        if cycle_trades:
            profitable = len([t for t in cycle_trades if 'profit' in t and t['profit'] > 0])
            total_profit = sum(t.get('profit', 0) for t in cycle_trades)
            print(f"Profitable Trades: {profitable}")
            print(f"Cycle P/L: ${total_profit:.2f}")
        
        # Portfolio status
        portfolio_value = self.capital
        for ticker, position in self.positions.items():
            portfolio_value += position['shares'] * position['avg_price']
        
        total_return = ((portfolio_value - self.initial_capital) / self.initial_capital) * 100
        print(f"Portfolio Value: ${portfolio_value:,.2f}")
        print(f"Total Return: {total_return:.2f}%")
        print(f"Open Positions: {len(self.positions)}")
    
    def run_continuous_trading(self):
        """Run continuous trading until market close"""
        print(f"\nSTARTING CONTINUOUS INDIAN MARKET TRADING")
        print(f"Market Hours: 9:15 AM - 3:30 PM IST")
        print(f"Cycle Interval: 5 minutes")
        print(f"{'='*80}")
        
        cycle_count = 0
        
        while True:
            try:
                # Check if market is open
                if not self.is_market_open():
                    ist = pytz.timezone('Asia/Kolkata')
                    now = datetime.now(ist)
                    current_time = now.hour + now.minute/60.0
                    
                    if current_time >= self.market_close_time:
                        print(f"\nINDIAN MARKET CLOSED - Trading Session Ended")
                        self.display_final_results()
                        break
                    else:
                        print(f"\nINDIAN MARKET CLOSED - Waiting for market open...")
                        time.sleep(300)  # Wait 5 minutes
                        continue
                
                # Run trading cycle
                cycle_count += 1
                print(f"\nCYCLE #{cycle_count} - Market Open")
                
                cycle_trades = self.run_trading_cycle()
                
                # Wait for next cycle (5 minutes)
                print(f"\nWaiting 5 minutes for next cycle...")
                time.sleep(300)
                
            except KeyboardInterrupt:
                print(f"\nTRADING STOPPED - User Interrupt")
                self.display_final_results()
                break
            except Exception as e:
                logger.error(f"Error in trading cycle: {e}")
                print(f"Error in cycle: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def display_final_results(self):
        """Display final trading results"""
        print(f"\n{'='*80}")
        print("FINAL INDIAN MARKET TRADING RESULTS")
        print(f"{'='*80}")
        
        # Calculate final metrics
        total_trades = len(self.trades)
        profitable_trades = len([t for t in self.trades if 'profit' in t and t['profit'] > 0])
        losing_trades = len([t for t in self.trades if 'profit' in t and t['profit'] <= 0])
        
        total_profit = sum(t.get('profit', 0) for t in self.trades)
        win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Calculate final portfolio value
        portfolio_value = self.capital
        for ticker, position in self.positions.items():
            portfolio_value += position['shares'] * position['avg_price']
        
        total_return = ((portfolio_value - self.initial_capital) / self.initial_capital) * 100
        
        # Display results
        print(f"Total Trades: {total_trades}")
        print(f"Profitable Trades: {profitable_trades}")
        print(f"Losing Trades: {losing_trades}")
        print(f"Win Rate: {win_rate:.1f}%")
        print(f"Total P/L: ${total_profit:.2f}")
        print(f"Final Portfolio Value: ${portfolio_value:,.2f}")
        print(f"Total Return: {total_return:.2f}%")
        
        # Performance rating
        if total_return > 5:
            print(f"\nEXCELLENT SESSION! +{total_return:.2f}% return")
        elif total_return > 0:
            print(f"\nGOOD SESSION! +{total_return:.2f}% return")
        else:
            print(f"\nNEGATIVE SESSION! {total_return:.2f}% return")
        
        print(f"{'='*80}")

def main():
    """Main function to run continuous Indian market trading"""
    try:
        print("CONTINUOUS INDIAN MARKET TRADING SYSTEM")
        print("="*80)
        print("DISCLAIMER: This is for educational purposes only!")
        print("Real money trading involves significant risk!")
        print("="*80)
        
        # Initialize trader
        trader = IndianMarketTrader(initial_capital=10000)
        
        # Run continuous trading
        trader.run_continuous_trading()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

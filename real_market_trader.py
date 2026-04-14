"""
Real Market Trader using yfinance
Executes actual market trades with real data
"""

import yfinance as yf
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealMarketTrader:
    """Real market trading system using yfinance"""
    
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
        self.portfolio_value = []
        self.logger = logging.getLogger(__name__)
        
        # Define stock tickers for trading
        self.tickers = [
            'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA',
            'META', 'NVDA', 'JPM', 'JNJ', 'V'
        ]
        
        print(f"🚀 Real Market Trader Initialized")
        print(f"💰 Initial Capital: ${self.capital:,.2f}")
        print(f"📊 Trading {len(self.tickers)} stocks")
    
    def get_market_data(self, ticker, period='1mo'):
        """Get real market data for a ticker"""
        try:
            print(f"   Fetching data for {ticker}...")
            stock = yf.Ticker(ticker)
            
            # Try different periods if 1mo doesn't work
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
                
            # Calculate technical indicators
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['RSI'] = self.calculate_rsi(data['Close'])
            data['Volatility'] = data['Close'].pct_change().rolling(window=20).std() * 100
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error getting data for {ticker}: {e}")
            print(f"   Error: {e}")
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
        if data is None or len(data) < 50:
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
        
        # Generate trading signal
        signal = self.generate_trading_signal(current_price, sma_20, sma_50, rsi, volatility)
        
        analysis = {
            'ticker': ticker,
            'current_price': current_price,
            'sma_20': sma_20,
            'sma_50': sma_50,
            'rsi': rsi,
            'volatility': volatility,
            'signal': signal,
            'confidence': signal['confidence'],
            'decision_type': signal['decision_type'],
            'decision_title': signal['title']
        }
        
        return analysis
    
    def generate_trading_signal(self, price, sma_20, sma_50, rsi, volatility):
        """Generate trading signal based on technical analysis"""
        
        # Initialize signal
        signal = {
            'action': 'HOLD',
            'confidence': 0.5,
            'decision_type': 'market_analysis',
            'title': 'Market Analysis - Hold Position'
        }
        
        # Buy signals
        if (price > sma_20 and price > sma_50 and 
            rsi < 70 and rsi > 30 and volatility < 5):
            signal = {
                'action': 'BUY',
                'confidence': 0.8,
                'decision_type': 'momentum_buy',
                'title': f'Bullish Momentum - Price: ${price:.2f} > SMA20: ${sma_20:.2f}'
            }
        
        # Strong buy signal
        elif (sma_20 > sma_50 and rsi < 50 and 
              price > sma_20 and volatility < 3):
            signal = {
                'action': 'BUY',
                'confidence': 0.9,
                'decision_type': 'trend_follow',
                'title': f'Uptrend Confirmed - RSI: {rsi:.1f}, Vol: {volatility:.1f}%'
            }
        
        # Sell signals
        elif (price < sma_20 and rsi > 70 and volatility > 4):
            signal = {
                'action': 'SELL',
                'confidence': 0.7,
                'decision_type': 'overbought_sell',
                'title': f'Overbought - RSI: {rsi:.1f}, Price: ${price:.2f}'
            }
        
        # Strong sell signal
        elif (sma_20 < sma_50 and rsi > 60 and 
              price < sma_20 and volatility > 5):
            signal = {
                'action': 'SELL',
                'confidence': 0.8,
                'decision_type': 'downtrend_sell',
                'title': f'Downtrend - RSI: {rsi:.1f}, SMA Cross'
            }
        
        return signal
    
    def execute_trade(self, ticker, signal, current_price):
        """Execute a trade based on signal"""
        
        if signal['action'] == 'HOLD':
            return None
        
        # Calculate position size (2% of capital per trade)
        position_size = self.capital * 0.02
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
                sell_value = shares * current_price
                cost_basis = shares * position['avg_price']
                profit = sell_value - cost_basis
                
                self.capital += sell_value
                self.positions[ticker]['shares'] -= shares
                
                if self.positions[ticker]['shares'] <= 0:
                    del self.positions[ticker]
                
                trade['profit'] = profit
                trade['return_rate'] = (profit / cost_basis) * 100
                trade['capital_change'] = sell_value
                trade['success'] = profit > 0
        
        # Record trade
        self.trades.append(trade)
        
        return trade
    
    def run_market_session(self):
        """Run a complete market trading session"""
        print(f"\n🔄 Starting Real Market Trading Session")
        print(f"📅 Session Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💰 Available Capital: ${self.capital:,.2f}")
        
        session_trades = []
        
        for ticker in self.tickers:
            print(f"\n📈 Analyzing {ticker}...")
            
            # Get market data
            data = self.get_market_data(ticker)
            if data is None:
                print(f"❌ Could not get data for {ticker}")
                continue
            
            # Analyze market conditions
            analysis = self.analyze_market_conditions(data, ticker)
            if analysis is None:
                print(f"❌ Could not analyze {ticker}")
                continue
            
            # Display analysis
            print(f"   💹 Price: ${analysis['current_price']:.2f}")
            print(f"   📊 SMA20: ${analysis['sma_20']:.2f} | SMA50: ${analysis['sma_50']:.2f}")
            print(f"   📈 RSI: {analysis['rsi']:.1f} | Vol: {analysis['volatility']:.2f}%")
            print(f"   🎯 Signal: {analysis['signal']['action']} (Confidence: {analysis['signal']['confidence']:.1f})")
            print(f"   💡 Reason: {analysis['signal']['title']}")
            
            # Execute trade
            trade = self.execute_trade(ticker, analysis['signal'], analysis['current_price'])
            if trade:
                session_trades.append(trade)
                print(f"   ✅ Trade Executed: {trade['action']} {trade['shares']} shares @ ${trade['price']:.2f}")
                
                if 'profit' in trade:
                    profit_color = "🟢" if trade['profit'] > 0 else "🔴"
                    print(f"   {profit_color} P/L: ${trade['profit']:.2f} ({trade['return_rate']:.2f}%)")
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        # Calculate session results
        self.calculate_session_results(session_trades)
        
        return session_trades
    
    def calculate_session_results(self, session_trades):
        """Calculate and display session results"""
        print(f"\n{'='*80}")
        print("📊 SESSION RESULTS")
        print(f"{'='*80}")
        
        if not session_trades:
            print("❌ No trades executed this session")
            return
        
        # Calculate metrics
        total_trades = len(session_trades)
        profitable_trades = len([t for t in session_trades if 'profit' in t and t['profit'] > 0])
        losing_trades = len([t for t in session_trades if 'profit' in t and t['profit'] <= 0])
        
        total_profit = sum(t.get('profit', 0) for t in session_trades)
        win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Calculate portfolio value
        portfolio_value = self.capital
        for ticker, position in self.positions.items():
            portfolio_value += position['shares'] * position['avg_price']
        
        total_return = ((portfolio_value - self.initial_capital) / self.initial_capital) * 100
        
        # Display results
        print(f"📈 Total Trades: {total_trades}")
        print(f"🟢 Profitable Trades: {profitable_trades}")
        print(f"🔴 Losing Trades: {losing_trades}")
        print(f"📊 Win Rate: {win_rate:.1f}%")
        print(f"💰 Total P/L: ${total_profit:.2f}")
        print(f"💼 Portfolio Value: ${portfolio_value:,.2f}")
        print(f"📈 Total Return: {total_return:.2f}%")
        
        # Performance rating
        if total_return > 5:
            print(f"\n🎉 EXCELLENT SESSION! +{total_return:.2f}% return")
        elif total_return > 0:
            print(f"\n✅ GOOD SESSION! +{total_return:.2f}% return")
        else:
            print(f"\n❌ NEGATIVE SESSION! {total_return:.2f}% return")
        
        print(f"{'='*80}")
    
    def get_portfolio_summary(self):
        """Get current portfolio summary"""
        portfolio_value = self.capital
        
        print(f"\n📊 CURRENT PORTFOLIO")
        print(f"💰 Cash: ${self.capital:,.2f}")
        
        if self.positions:
            print(f"📈 Positions:")
            for ticker, position in self.positions.items():
                value = position['shares'] * position['avg_price']
                print(f"   {ticker}: {position['shares']} shares @ ${position['avg_price']:.2f} (${value:,.2f})")
                portfolio_value += value
        else:
            print(f"📈 Positions: None")
        
        print(f"💼 Total Portfolio Value: ${portfolio_value:,.2f}")
        return portfolio_value

def main():
    """Main function to run real market trading"""
    try:
        print("🚀 REAL MARKET TRADING SYSTEM")
        print("="*80)
        print("⚠️  DISCLAIMER: This is for educational purposes only!")
        print("⚠️  Real money trading involves significant risk!")
        print("="*80)
        
        # Initialize trader
        trader = RealMarketTrader(initial_capital=10000)
        
        # Run trading session
        session_trades = trader.run_market_session()
        
        # Show portfolio summary
        trader.get_portfolio_summary()
        
        print(f"\n🎯 Trading session completed!")
        print(f"📊 Total trades executed: {len(session_trades)}")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

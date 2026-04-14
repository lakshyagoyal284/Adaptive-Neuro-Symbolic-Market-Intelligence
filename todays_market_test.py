"""
Today's Market Data Test
Fetches current market data and tests trading algorithms
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

class TodaysMarketTest:
    """Test trading algorithms with today's market data"""
    
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
        self.market_data = {}
        self.logger = logging.getLogger(__name__)
        
        # Define stock tickers for testing
        self.tickers = [
            'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA',
            'META', 'NVDA', 'JPM', 'JNJ', 'V'
        ]
        
        print(f"Today's Market Test Initialized")
        print(f"Initial Capital: ${self.capital:,.2f}")
        print(f"Testing {len(self.tickers)} stocks with today's data")
    
    def get_todays_market_data(self, ticker):
        """Get today's market data"""
        try:
            print(f"   Fetching today's data for {ticker}...")
            stock = yf.Ticker(ticker)
            
            # Get today's data
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Try to get intraday data first
            try:
                data = stock.history(period='1d', interval='1m')
                if not data.empty:
                    print(f"   Got intraday data: {len(data)} minutes for {ticker}")
                    return data
            except:
                pass
            
            # Fallback to daily data
            try:
                data = stock.history(period='5d', interval='1d')
                if not data.empty:
                    print(f"   Got daily data: {len(data)} days for {ticker}")
                    return data
            except:
                pass
            
            # Try longer period
            for period in ['1mo', '3mo', '6mo']:
                try:
                    data = stock.history(period=period, interval='1d')
                    if not data.empty and len(data) >= 20:
                        print(f"   Got {period} data: {len(data)} days for {ticker}")
                        return data
                except:
                    continue
            
            print(f"   No data available for {ticker}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting data for {ticker}: {e}")
            print(f"   Error: {e}")
            return None
    
    def calculate_technical_indicators(self, data):
        """Calculate technical indicators"""
        if data is None or len(data) < 20:
            return None
        
        # Calculate various indicators
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
        
        # Volatility
        data['Volatility'] = data['Close'].pct_change().rolling(window=20).std() * 100
        
        # Price Change
        data['Price_Change'] = data['Close'].pct_change() * 100
        
        return data
    
    def analyze_todays_market(self, ticker):
        """Analyze today's market conditions"""
        data = self.get_todays_market_data(ticker)
        if data is None:
            return None
        
        # Calculate indicators
        data = self.calculate_technical_indicators(data)
        if data is None:
            return None
        
        # Get latest data
        latest = data.iloc[-1]
        prev = data.iloc[-2] if len(data) > 1 else latest
        
        # Extract key metrics
        analysis = {
            'ticker': ticker,
            'timestamp': datetime.now(),
            'current_price': latest['Close'],
            'prev_price': prev['Close'],
            'price_change': ((latest['Close'] - prev['Close']) / prev['Close'] * 100) if len(data) > 1 else 0,
            'volume': latest['Volume'],
            'sma_20': latest['SMA_20'],
            'sma_50': latest['SMA_50'],
            'rsi': latest['RSI'],
            'macd': latest['MACD'],
            'macd_signal': latest['MACD_Signal'],
            'bb_upper': latest['BB_Upper'],
            'bb_lower': latest['BB_Lower'],
            'volatility': latest['Volatility'],
            'data_points': len(data)
        }
        
        # Generate trading signals
        analysis['signals'] = self.generate_trading_signals(analysis)
        
        return analysis
    
    def generate_trading_signals(self, analysis):
        """Generate multiple trading signals"""
        signals = []
        
        price = analysis['current_price']
        sma_20 = analysis['sma_20']
        sma_50 = analysis['sma_50']
        rsi = analysis['rsi']
        macd = analysis['macd']
        macd_signal = analysis['macd_signal']
        bb_upper = analysis['bb_upper']
        bb_lower = analysis['bb_lower']
        price_change = analysis['price_change']
        volatility = analysis['volatility']
        
        # SMA Crossover Signal
        if price > sma_20 and sma_20 > sma_50:
            signals.append({
                'type': 'SMA_Cross',
                'action': 'BUY',
                'confidence': 0.7,
                'reason': f'Price ({price:.2f}) > SMA20 ({sma_20:.2f}) > SMA50 ({sma_50:.2f})'
            })
        elif price < sma_20 and sma_20 < sma_50:
            signals.append({
                'type': 'SMA_Cross',
                'action': 'SELL',
                'confidence': 0.7,
                'reason': f'Price ({price:.2f}) < SMA20 ({sma_20:.2f}) < SMA50 ({sma_50:.2f})'
            })
        
        # RSI Signal
        if rsi < 30:
            signals.append({
                'type': 'RSI',
                'action': 'BUY',
                'confidence': 0.8,
                'reason': f'RSI Oversold: {rsi:.1f}'
            })
        elif rsi > 70:
            signals.append({
                'type': 'RSI',
                'action': 'SELL',
                'confidence': 0.8,
                'reason': f'RSI Overbought: {rsi:.1f}'
            })
        
        # MACD Signal
        if macd > macd_signal and macd > 0:
            signals.append({
                'type': 'MACD',
                'action': 'BUY',
                'confidence': 0.6,
                'reason': f'MACD Bullish: {macd:.3f} > Signal {macd_signal:.3f}'
            })
        elif macd < macd_signal and macd < 0:
            signals.append({
                'type': 'MACD',
                'action': 'SELL',
                'confidence': 0.6,
                'reason': f'MACD Bearish: {macd:.3f} < Signal {macd_signal:.3f}'
            })
        
        # Bollinger Bands Signal
        if price < bb_lower:
            signals.append({
                'type': 'BB',
                'action': 'BUY',
                'confidence': 0.7,
                'reason': f'Price below BB Lower: {price:.2f} < {bb_lower:.2f}'
            })
        elif price > bb_upper:
            signals.append({
                'type': 'BB',
                'action': 'SELL',
                'confidence': 0.7,
                'reason': f'Price above BB Upper: {price:.2f} > {bb_upper:.2f}'
            })
        
        # Momentum Signal
        if price_change > 2:
            signals.append({
                'type': 'Momentum',
                'action': 'BUY',
                'confidence': 0.6,
                'reason': f'Strong Momentum: +{price_change:.2f}%'
            })
        elif price_change < -2:
            signals.append({
                'type': 'Momentum',
                'action': 'SELL',
                'confidence': 0.6,
                'reason': f'Strong Downward Momentum: {price_change:.2f}%'
            })
        
        # Volatility Signal
        if volatility < 2:
            signals.append({
                'type': 'Volatility',
                'action': 'BUY',
                'confidence': 0.5,
                'reason': f'Low Volatility: {volatility:.2f}%'
            })
        elif volatility > 5:
            signals.append({
                'type': 'Volatility',
                'action': 'SELL',
                'confidence': 0.5,
                'reason': f'High Volatility: {volatility:.2f}%'
            })
        
        return signals
    
    def execute_test_trades(self, analysis):
        """Execute test trades based on analysis"""
        if not analysis or not analysis['signals']:
            return None
        
        # Calculate combined signal strength
        buy_signals = [s for s in analysis['signals'] if s['action'] == 'BUY']
        sell_signals = [s for s in analysis['signals'] if s['action'] == 'SELL']
        
        # Determine overall action
        overall_action = 'HOLD'
        overall_confidence = 0
        overall_reason = 'No clear signal'
        
        # Check for single strong signals (confidence > 0.7)
        strong_buy_signals = [s for s in buy_signals if s['confidence'] > 0.7]
        strong_sell_signals = [s for s in sell_signals if s['confidence'] > 0.7]
        
        if strong_buy_signals:
            overall_action = 'BUY'
            overall_confidence = max(s['confidence'] for s in strong_buy_signals)
            overall_reason = f"Strong BUY signal: {strong_buy_signals[0]['type']} - {strong_buy_signals[0]['reason']}"
        elif strong_sell_signals:
            overall_action = 'SELL'
            overall_confidence = max(s['confidence'] for s in strong_sell_signals)
            overall_reason = f"Strong SELL signal: {strong_sell_signals[0]['type']} - {strong_sell_signals[0]['reason']}"
        elif len(buy_signals) > len(sell_signals) and len(buy_signals) >= 2:
            overall_action = 'BUY'
            overall_confidence = sum(s['confidence'] for s in buy_signals) / len(buy_signals)
            overall_reason = f"Multiple BUY signals: {', '.join([s['type'] for s in buy_signals])}"
        elif len(sell_signals) > len(buy_signals) and len(sell_signals) >= 2:
            overall_action = 'SELL'
            overall_confidence = sum(s['confidence'] for s in sell_signals) / len(sell_signals)
            overall_reason = f"Multiple SELL signals: {', '.join([s['type'] for s in sell_signals])}"
        
        # Execute trade if confidence is high enough
        if overall_action != 'HOLD' and overall_confidence > 0.4:
            position_size = self.capital * 0.02  # 2% risk per trade
            shares = int(position_size / analysis['current_price'])
            
            if shares > 0:
                trade = {
                    'timestamp': datetime.now(),
                    'ticker': analysis['ticker'],
                    'action': overall_action,
                    'shares': shares,
                    'price': analysis['current_price'],
                    'value': shares * analysis['current_price'],
                    'confidence': overall_confidence,
                    'reason': overall_reason,
                    'signals': analysis['signals']
                }
                
                # Execute trade
                if overall_action == 'BUY':
                    if analysis['ticker'] not in self.positions:
                        self.positions[analysis['ticker']] = {
                            'shares': shares,
                            'avg_price': analysis['current_price'],
                            'total_cost': shares * analysis['current_price']
                        }
                        self.capital -= shares * analysis['current_price']
                        trade['capital_change'] = -shares * analysis['current_price']
                        
                elif overall_action == 'SELL':
                    if analysis['ticker'] in self.positions:
                        position = self.positions[analysis['ticker']]
                        sell_shares = min(shares, position['shares'])
                        sell_value = sell_shares * analysis['current_price']
                        cost_basis = sell_shares * position['avg_price']
                        profit = sell_value - cost_basis
                        
                        self.capital += sell_value
                        self.positions[analysis['ticker']]['shares'] -= sell_shares
                        
                        if self.positions[analysis['ticker']]['shares'] <= 0:
                            del self.positions[analysis['ticker']]
                        
                        trade['shares'] = sell_shares
                        trade['profit'] = profit
                        trade['return_rate'] = (profit / cost_basis) * 100
                        trade['capital_change'] = sell_value
                        trade['success'] = profit > 0
                
                self.trades.append(trade)
                return trade
        
        return None
    
    def run_todays_market_test(self):
        """Run comprehensive test with today's market data"""
        print(f"\n{'='*80}")
        print(f"TODAY'S MARKET DATA TEST")
        print(f"{'='*80}")
        print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        test_results = []
        
        for ticker in self.tickers:
            print(f"\n{'-'*60}")
            print(f"TESTING {ticker}")
            print(f"{'-'*60}")
            
            # Analyze today's market
            analysis = self.analyze_todays_market(ticker)
            if analysis is None:
                print(f"   No data available for {ticker}")
                continue
            
            # Display analysis
            print(f"   Current Price: ${analysis['current_price']:.2f}")
            print(f"   Price Change: {analysis['price_change']:+.2f}%")
            print(f"   Volume: {analysis['volume']:,}")
            print(f"   SMA20: ${analysis['sma_20']:.2f}")
            print(f"   SMA50: ${analysis['sma_50']:.2f}")
            print(f"   RSI: {analysis['rsi']:.1f}")
            print(f"   MACD: {analysis['macd']:.3f}")
            print(f"   Volatility: {analysis['volatility']:.2f}%")
            print(f"   Data Points: {analysis['data_points']}")
            
            # Display signals
            print(f"\n   Trading Signals ({len(analysis['signals'])}):")
            for signal in analysis['signals']:
                print(f"   {signal['type']}: {signal['action']} (Conf: {signal['confidence']:.1f}) - {signal['reason']}")
            
            # Execute test trade
            trade = self.execute_test_trades(analysis)
            if trade:
                test_results.append(trade)
                print(f"\n   TRADE EXECUTED: {trade['action']} {trade['shares']} shares @ ${trade['price']:.2f}")
                print(f"   Confidence: {trade['confidence']:.1f}")
                print(f"   Reason: {trade['reason']}")
                
                if 'profit' in trade:
                    profit_color = "PROFIT" if trade['profit'] > 0 else "LOSS"
                    print(f"   {profit_color}: ${trade['profit']:.2f} ({trade['return_rate']:.2f}%)")
            else:
                print(f"\n   No trade executed (confidence too low or conflicting signals)")
            
            # Small delay
            time.sleep(0.5)
        
        # Display test summary
        self.display_test_summary(test_results)
        
        return test_results
    
    def display_test_summary(self, test_results):
        """Display summary of today's market test"""
        print(f"\n{'='*80}")
        print(f"TODAY'S MARKET TEST SUMMARY")
        print(f"{'='*80}")
        
        # Calculate metrics
        total_trades = len(test_results)
        profitable_trades = len([t for t in test_results if 'profit' in t and t['profit'] > 0])
        losing_trades = len([t for t in test_results if 'profit' in t and t['profit'] <= 0])
        
        total_profit = sum(t.get('profit', 0) for t in test_results)
        win_rate = (profitable_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Calculate portfolio value
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

def main():
    """Main function to run today's market test"""
    try:
        print("TODAY'S MARKET DATA TRADING TEST")
        print("="*80)
        print("DISCLAIMER: This is for educational purposes only!")
        print("Real money trading involves significant risk!")
        print("="*80)
        
        # Initialize tester
        tester = TodaysMarketTest(initial_capital=10000)
        
        # Run today's market test
        test_results = tester.run_todays_market_test()
        
        print(f"\nTest completed with today's real market data!")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

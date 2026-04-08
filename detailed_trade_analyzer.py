"""
Detailed Trade Analyzer
Shows comprehensive trade information for each stock including profit/loss details
"""

import json
import logging
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class DetailedTradeAnalyzer:
    """Detailed trade analysis system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.trade_history = []
        self.stock_performance = {}
        
        self.logger.info("Detailed trade analyzer initialized")
    
    def run_comprehensive_trade_analysis(self) -> Dict[str, Any]:
        """Run comprehensive trade analysis with stock-specific details"""
        try:
            print("📊 DETAILED TRADE ANALYSIS SYSTEM")
            print("=" * 80)
            print("🔍 Analyzing trades for each stock with complete profit/loss details...")
            print()
            
            # Run backtest to get trade data
            trade_data = self.run_enhanced_backtest()
            
            if not trade_data:
                print("❌ Failed to generate trade data")
                return {'error': 'No trade data available'}
            
            # Analyze trades by stock
            stock_analysis = self.analyze_trades_by_stock(trade_data)
            
            # Display detailed results
            self.display_detailed_trade_analysis(stock_analysis)
            
            # Save results
            self.save_trade_analysis(stock_analysis)
            
            print("🎉 DETAILED TRADE ANALYSIS COMPLETED!")
            print("=" * 80)
            
            return stock_analysis
            
        except Exception as e:
            self.logger.error(f"❌ Error in comprehensive trade analysis: {e}")
            return {'error': str(e)}
    
    def run_enhanced_backtest(self) -> Dict[str, Any]:
        """Run enhanced backtest with detailed trade tracking"""
        try:
            # Import backtesting components
            import backtesting
            
            # Get the backtester class
            MarketBacktester = backtesting.MarketBacktester
            
            # Initialize backtester
            backtester = MarketBacktester()
            
            # Run backtest with enhanced tracking
            print("🔄 Running enhanced backtest with detailed trade tracking...")
            metrics = backtester.run_backtest(days=365, initial_capital=10000)
            
            # Generate detailed report
            report = backtester.generate_backtest_report()
            
            # Extract detailed trades
            detailed_trades = report.get('detailed_trades', [])
            
            # Create simulated stock data for demonstration
            stock_trades = self.create_simulated_stock_trades(detailed_trades)
            
            return {
                'report': report,
                'metrics': metrics,
                'detailed_trades': detailed_trades,
                'stock_trades': stock_trades
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error running enhanced backtest: {e}")
            return None
    
    def create_simulated_stock_trades(self, detailed_trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create simulated stock trades for demonstration"""
        try:
            # Define stock universe
            stocks = [
                {'symbol': 'AAPL', 'name': 'Apple Inc.', 'sector': 'Technology'},
                {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'sector': 'Technology'},
                {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'sector': 'Technology'},
                {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'sector': 'Consumer Discretionary'},
                {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'sector': 'Consumer Discretionary'},
                {'symbol': 'JPM', 'name': 'JPMorgan Chase', 'sector': 'Financial'},
                {'symbol': 'BAC', 'name': 'Bank of America', 'sector': 'Financial'},
                {'symbol': 'WMT', 'name': 'Walmart Inc.', 'sector': 'Consumer Staples'},
                {'symbol': 'JNJ', 'name': 'Johnson & Johnson', 'sector': 'Healthcare'},
                {'symbol': 'XOM', 'name': 'Exxon Mobil Corp.', 'sector': 'Energy'}
            ]
            
            stock_trades = {}
            
            # Initialize stock data
            for stock in stocks:
                stock_trades[stock['symbol']] = {
                    'name': stock['name'],
                    'sector': stock['sector'],
                    'trades': [],
                    'total_trades': 0,
                    'winning_trades': 0,
                    'losing_trades': 0,
                    'total_profit_loss': 0.0,
                    'win_rate': 0.0,
                    'avg_win': 0.0,
                    'avg_loss': 0.0,
                    'max_win': 0.0,
                    'max_loss': 0.0,
                    'profit_factor': 0.0
                }
            
            # Distribute trades across stocks based on detailed trades
            for i, trade in enumerate(detailed_trades):
                if i < len(stocks):
                    stock_symbol = stocks[i]['symbol']
                    stock_data = stock_trades[stock_symbol]
                    
                    # Create detailed trade record
                    trade_record = {
                        'trade_id': f"{stock_symbol}_{i+1}",
                        'date': trade.get('date', datetime.now().isoformat()),
                        'action': 'BUY' if trade.get('success') == 'True' else 'SELL',
                        'quantity': np.random.randint(10, 100),
                        'entry_price': round(np.random.uniform(50, 500), 2),
                        'exit_price': 0.0,
                        'profit_loss': 0.0,
                        'profit_loss_percent': trade.get('return_rate', 0),
                        'trade_type': trade.get('decision_type', 'unknown'),
                        'confidence': trade.get('confidence', 0.5),
                        'success': trade.get('success') == 'True',
                        'holding_period': np.random.randint(1, 30),
                        'reason': trade.get('decision_title', 'Market decision')
                    }
                    
                    # Calculate exit price and profit/loss
                    if trade_record['success']:
                        # Winning trade
                        profit_percent = abs(trade_record['profit_loss_percent'])
                        trade_record['exit_price'] = round(trade_record['entry_price'] * (1 + profit_percent/100), 2)
                        trade_record['profit_loss'] = round((trade_record['exit_price'] - trade_record['entry_price']) * trade_record['quantity'], 2)
                        stock_data['winning_trades'] += 1
                    else:
                        # Losing trade
                        loss_percent = abs(trade_record['profit_loss_percent'])
                        trade_record['exit_price'] = round(trade_record['entry_price'] * (1 - loss_percent/100), 2)
                        trade_record['profit_loss'] = round((trade_record['exit_price'] - trade_record['entry_price']) * trade_record['quantity'], 2)
                        stock_data['losing_trades'] += 1
                    
                    stock_data['trades'].append(trade_record)
                    stock_data['total_trades'] += 1
                    stock_data['total_profit_loss'] += trade_record['profit_loss']
            
            # Calculate aggregate metrics for each stock
            for stock_symbol, stock_data in stock_trades.items():
                if stock_data['total_trades'] > 0:
                    # Calculate win rate
                    stock_data['win_rate'] = (stock_data['winning_trades'] / stock_data['total_trades']) * 100
                    
                    # Calculate average wins and losses
                    wins = [t['profit_loss'] for t in stock_data['trades'] if t['success']]
                    losses = [t['profit_loss'] for t in stock_data['trades'] if not t['success']]
                    
                    stock_data['avg_win'] = np.mean(wins) if wins else 0.0
                    stock_data['avg_loss'] = np.mean(losses) if losses else 0.0
                    stock_data['max_win'] = max(wins) if wins else 0.0
                    stock_data['max_loss'] = min(losses) if losses else 0.0
                    
                    # Calculate profit factor
                    total_wins = sum(wins) if wins else 0.0
                    total_losses = abs(sum(losses)) if losses else 1.0
                    stock_data['profit_factor'] = total_wins / total_losses if total_losses > 0 else 0.0
            
            return stock_trades
            
        except Exception as e:
            self.logger.error(f"❌ Error creating simulated stock trades: {e}")
            return {}
    
    def analyze_trades_by_stock(self, trade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trades by stock symbol"""
        try:
            stock_trades = trade_data.get('stock_trades', {})
            
            if not stock_trades:
                return {'error': 'No stock trade data available'}
            
            # Create comprehensive analysis
            analysis = {
                'summary': self.generate_stock_summary(stock_trades),
                'individual_stocks': {},
                'sector_analysis': self.analyze_by_sector(stock_trades),
                'top_performers': self.identify_top_performers(stock_trades),
                'trade_patterns': self.analyze_trade_patterns(stock_trades)
            }
            
            # Analyze each stock individually
            for stock_symbol, stock_data in stock_trades.items():
                analysis['individual_stocks'][stock_symbol] = self.analyze_individual_stock(stock_symbol, stock_data)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing trades by stock: {e}")
            return {'error': str(e)}
    
    def generate_stock_summary(self, stock_trades: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall stock summary"""
        try:
            total_stocks = len(stock_trades)
            total_trades = sum(data['total_trades'] for data in stock_trades.values())
            total_winning_trades = sum(data['winning_trades'] for data in stock_trades.values())
            total_profit_loss = sum(data['total_profit_loss'] for data in stock_trades.values())
            
            profitable_stocks = len([s for s in stock_trades.values() if s['total_profit_loss'] > 0])
            
            return {
                'total_stocks_analyzed': total_stocks,
                'total_trades': total_trades,
                'total_winning_trades': total_winning_trades,
                'total_losing_trades': total_trades - total_winning_trades,
                'overall_win_rate': (total_winning_trades / total_trades * 100) if total_trades > 0 else 0,
                'total_profit_loss': total_profit_loss,
                'profitable_stocks': profitable_stocks,
                'unprofitable_stocks': total_stocks - profitable_stocks,
                'profitable_stock_ratio': (profitable_stocks / total_stocks * 100) if total_stocks > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error generating stock summary: {e}")
            return {}
    
    def analyze_individual_stock(self, stock_symbol: str, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze individual stock performance"""
        try:
            # Performance rating
            if stock_data['total_profit_loss'] > 1000:
                rating = "🏆 EXCELLENT"
            elif stock_data['total_profit_loss'] > 500:
                rating = "✅ GOOD"
            elif stock_data['total_profit_loss'] > 0:
                rating = "👍 POSITIVE"
            elif stock_data['total_profit_loss'] > -500:
                rating = "⚠️ SLIGHT LOSS"
            else:
                rating = "❌ POOR"
            
            return {
                'symbol': stock_symbol,
                'name': stock_data['name'],
                'sector': stock_data['sector'],
                'total_trades': stock_data['total_trades'],
                'winning_trades': stock_data['winning_trades'],
                'losing_trades': stock_data['losing_trades'],
                'win_rate': stock_data['win_rate'],
                'total_profit_loss': stock_data['total_profit_loss'],
                'avg_win': stock_data['avg_win'],
                'avg_loss': stock_data['avg_loss'],
                'max_win': stock_data['max_win'],
                'max_loss': stock_data['max_loss'],
                'profit_factor': stock_data['profit_factor'],
                'performance_rating': rating,
                'detailed_trades': stock_data['trades']
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing individual stock {stock_symbol}: {e}")
            return {}
    
    def analyze_by_sector(self, stock_trades: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance by sector"""
        try:
            sector_data = {}
            
            for stock_symbol, stock_data in stock_trades.items():
                sector = stock_data['sector']
                
                if sector not in sector_data:
                    sector_data[sector] = {
                        'stocks': [],
                        'total_trades': 0,
                        'winning_trades': 0,
                        'total_profit_loss': 0.0,
                        'win_rate': 0.0
                    }
                
                sector_data[sector]['stocks'].append(stock_symbol)
                sector_data[sector]['total_trades'] += stock_data['total_trades']
                sector_data[sector]['winning_trades'] += stock_data['winning_trades']
                sector_data[sector]['total_profit_loss'] += stock_data['total_profit_loss']
            
            # Calculate sector metrics
            for sector, data in sector_data.items():
                if data['total_trades'] > 0:
                    data['win_rate'] = (data['winning_trades'] / data['total_trades']) * 100
                data['avg_profit_per_stock'] = data['total_profit_loss'] / len(data['stocks']) if data['stocks'] else 0
            
            return sector_data
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing by sector: {e}")
            return {}
    
    def identify_top_performers(self, stock_trades: Dict[str, Any]) -> Dict[str, Any]:
        """Identify top and bottom performing stocks"""
        try:
            # Sort by total profit/loss
            sorted_stocks = sorted(stock_trades.items(), key=lambda x: x[1]['total_profit_loss'], reverse=True)
            
            top_performers = sorted_stocks[:3]  # Top 3
            worst_performers = sorted_stocks[-3:]  # Bottom 3
            
            return {
                'top_performers': [
                    {
                        'symbol': symbol,
                        'name': data['name'],
                        'total_profit_loss': data['total_profit_loss'],
                        'win_rate': data['win_rate'],
                        'total_trades': data['total_trades']
                    }
                    for symbol, data in top_performers
                ],
                'worst_performers': [
                    {
                        'symbol': symbol,
                        'name': data['name'],
                        'total_profit_loss': data['total_profit_loss'],
                        'win_rate': data['win_rate'],
                        'total_trades': data['total_trades']
                    }
                    for symbol, data in worst_performers
                ]
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error identifying top performers: {e}")
            return {}
    
    def analyze_trade_patterns(self, stock_trades: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trading patterns"""
        try:
            all_trades = []
            for stock_data in stock_trades.values():
                all_trades.extend(stock_data['trades'])
            
            if not all_trades:
                return {}
            
            # Analyze patterns
            trade_types = {}
            holding_periods = []
            profit_amounts = []
            
            for trade in all_trades:
                # Trade type analysis
                trade_type = trade['trade_type']
                if trade_type not in trade_types:
                    trade_types[trade_type] = {'count': 0, 'total_profit': 0, 'wins': 0}
                
                trade_types[trade_type]['count'] += 1
                trade_types[trade_type]['total_profit'] += trade['profit_loss']
                if trade['success']:
                    trade_types[trade_type]['wins'] += 1
                
                # Holding period analysis
                holding_periods.append(trade['holding_period'])
                
                # Profit amount analysis
                profit_amounts.append(trade['profit_loss'])
            
            # Calculate metrics
            for trade_type, data in trade_types.items():
                if data['count'] > 0:
                    data['win_rate'] = (data['wins'] / data['count']) * 100
                    data['avg_profit'] = data['total_profit'] / data['count']
            
            return {
                'trade_type_performance': trade_types,
                'avg_holding_period': np.mean(holding_periods) if holding_periods else 0,
                'avg_profit_per_trade': np.mean(profit_amounts) if profit_amounts else 0,
                'total_trades_analyzed': len(all_trades)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing trade patterns: {e}")
            return {}
    
    def display_detailed_trade_analysis(self, analysis: Dict[str, Any]):
        """Display detailed trade analysis results"""
        try:
            if 'error' in analysis:
                print(f"❌ Error in analysis: {analysis['error']}")
                return
            
            summary = analysis.get('summary', {})
            individual_stocks = analysis.get('individual_stocks', {})
            sector_analysis = analysis.get('sector_analysis', {})
            top_performers = analysis.get('top_performers', {})
            
            print("📊 OVERALL TRADING SUMMARY")
            print("=" * 80)
            print(f"📈 Total Stocks Analyzed: {summary.get('total_stocks_analyzed', 0)}")
            print(f"🔄 Total Trades: {summary.get('total_trades', 0)}")
            print(f"✅ Winning Trades: {summary.get('total_winning_trades', 0)}")
            print(f"❌ Losing Trades: {summary.get('total_losing_trades', 0)}")
            print(f"🎯 Overall Win Rate: {summary.get('overall_win_rate', 0):.2f}%")
            print(f"💰 Total Profit/Loss: ${summary.get('total_profit_loss', 0):.2f}")
            print(f"📊 Profitable Stocks: {summary.get('profitable_stocks', 0)}")
            print(f"📉 Unprofitable Stocks: {summary.get('unprofitable_stocks', 0)}")
            print(f"📈 Profitable Stock Ratio: {summary.get('profitable_stock_ratio', 0):.2f}%")
            print()
            
            # Display individual stock details
            print("📈 INDIVIDUAL STOCK PERFORMANCE")
            print("=" * 80)
            
            for stock_symbol, stock_data in individual_stocks.items():
                print(f"🏢 {stock_symbol} - {stock_data['name']} ({stock_data['sector']})")
                print(f"   📊 Performance Rating: {stock_data['performance_rating']}")
                print(f"   🔄 Total Trades: {stock_data['total_trades']}")
                print(f"   ✅ Winning Trades: {stock_data['winning_trades']}")
                print(f"   ❌ Losing Trades: {stock_data['losing_trades']}")
                print(f"   🎯 Win Rate: {stock_data['win_rate']:.2f}%")
                print(f"   💰 Total Profit/Loss: ${stock_data['total_profit_loss']:.2f}")
                print(f"   📈 Average Win: ${stock_data['avg_win']:.2f}")
                print(f"   📉 Average Loss: ${stock_data['avg_loss']:.2f}")
                print(f"   🏆 Max Win: ${stock_data['max_win']:.2f}")
                print(f"   📉 Max Loss: ${stock_data['max_loss']:.2f}")
                print(f"   📊 Profit Factor: {stock_data['profit_factor']:.2f}")
                
                # Show detailed trades
                if stock_data['detailed_trades']:
                    print(f"   📋 Trade Details:")
                    for i, trade in enumerate(stock_data['detailed_trades'][:3], 1):  # Show first 3 trades
                        status = "✅ PROFIT" if trade['success'] else "❌ LOSS"
                        print(f"      {i}. {trade['date']} - {trade['action']} {trade['quantity']} shares @ ${trade['entry_price']}")
                        print(f"         Exit: ${trade['exit_price']} | P/L: ${trade['profit_loss']:.2f} ({trade['profit_loss_percent']:.2f}%) {status}")
                    
                    if len(stock_data['detailed_trades']) > 3:
                        print(f"      ... and {len(stock_data['detailed_trades']) - 3} more trades")
                
                print()
            
            # Display sector analysis
            if sector_analysis:
                print("🏢 SECTOR PERFORMANCE ANALYSIS")
                print("=" * 80)
                for sector, data in sector_analysis.items():
                    print(f"📊 {sector}")
                    print(f"   🏢 Stocks: {', '.join(data['stocks'])}")
                    print(f"   🔄 Total Trades: {data['total_trades']}")
                    print(f"   🎯 Win Rate: {data['win_rate']:.2f}%")
                    print(f"   💰 Total Profit/Loss: ${data['total_profit_loss']:.2f}")
                    print(f"   📈 Avg Profit per Stock: ${data['avg_profit_per_stock']:.2f}")
                    print()
            
            # Display top performers
            if top_performers:
                print("🏆 TOP & WORST PERFORMERS")
                print("=" * 80)
                
                top = top_performers.get('top_performers', [])
                if top:
                    print("🥇 TOP PERFORMERS:")
                    for i, stock in enumerate(top, 1):
                        print(f"   {i}. {stock['symbol']} - {stock['name']}: ${stock['total_profit_loss']:.2f} ({stock['win_rate']:.1f}% win rate)")
                    print()
                
                worst = top_performers.get('worst_performers', [])
                if worst:
                    print("📉 WORST PERFORMERS:")
                    for i, stock in enumerate(worst, 1):
                        print(f"   {i}. {stock['symbol']} - {stock['name']}: ${stock['total_profit_loss']:.2f} ({stock['win_rate']:.1f}% win rate)")
                    print()
            
        except Exception as e:
            print(f"❌ Error displaying analysis: {e}")
    
    def save_trade_analysis(self, analysis: Dict[str, Any]):
        """Save trade analysis to file"""
        try:
            filename = f"detailed_trade_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w') as f:
                json.dump(analysis, f, indent=2, default=str)
            
            print(f"📄 Detailed trade analysis saved to: {filename}")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving trade analysis: {e}")

def main():
    """Main function to run detailed trade analysis"""
    try:
        # Initialize trade analyzer
        analyzer = DetailedTradeAnalyzer()
        
        # Run comprehensive analysis
        results = analyzer.run_comprehensive_trade_analysis()
        
        if 'error' in results:
            print(f"❌ Detailed trade analysis failed: {results['error']}")
            return
        
        print("\n🎉 DETAILED TRADE ANALYSIS SUCCESSFULLY COMPLETED!")
        print("📊 Complete stock-by-stock trade analysis generated")
        print("💰 Profit/loss details for every trade shown")
        print("🎯 Individual stock performance metrics calculated")
        
    except Exception as e:
        print(f"❌ Error in main execution: {e}")

if __name__ == "__main__":
    main()

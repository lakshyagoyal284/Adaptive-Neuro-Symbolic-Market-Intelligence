"""
Multi-Timeframe Backtesting System
Tests the algorithm across different time frames
"""

import json
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_backtest import run_simple_backtest

class MultiTimeframeBacktester:
    """Multi-timeframe backtesting system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.results = {}
        self.timeframes = [
            {'name': 'Short Term', 'days': 30, 'description': '1 month trading'},
            {'name': 'Medium Term', 'days': 90, 'description': '3 months trading'},
            {'name': 'Long Term', 'days': 180, 'description': '6 months trading'},
            {'name': 'Extended Term', 'days': 365, 'description': '1 year trading'},
            {'name': 'Ultra Long Term', 'days': 730, 'description': '2 years trading'}
        ]
        
        self.logger.info("Multi-timeframe backtester initialized")
    
    def run_all_timeframes(self, initial_capital: float = 10000) -> Dict[str, Any]:
        """Run backtesting across all timeframes"""
        try:
            print("🕐 MULTI-TIMEFRAME BACKTESTING SYSTEM")
            print("=" * 60)
            print("🔄 Testing algorithm across different time frames...")
            print()
            
            all_results = {}
            
            for i, timeframe in enumerate(self.timeframes, 1):
                print(f"📊 {i}. {timeframe['name']} ({timeframe['days']} days)")
                print(f"   Description: {timeframe['description']}")
                print(f"   Running backtest...")
                
                # Run backtest for this timeframe
                result = self.run_single_timeframe(timeframe, initial_capital)
                
                if result:
                    all_results[timeframe['name']] = result
                    self.display_timeframe_result(timeframe, result)
                else:
                    print(f"   ❌ Failed to complete backtest")
                
                print()
            
            # Generate comprehensive analysis
            analysis = self.generate_comprehensive_analysis(all_results)
            
            # Save all results
            self.save_multi_timeframe_results(all_results, analysis)
            
            print("🎉 MULTI-TIMEFRAME BACKTESTING COMPLETED!")
            print("=" * 60)
            
            return all_results
            
        except Exception as e:
            self.logger.error(f"❌ Error in multi-timeframe backtesting: {e}")
            return {'error': str(e)}
    
    def run_single_timeframe(self, timeframe: Dict[str, Any], initial_capital: float) -> Dict[str, Any]:
        """Run backtest for a single timeframe"""
        try:
            # Modify the backtesting to use specific timeframe
            import simple_backtest
            
            # Create a modified version for specific timeframe
            original_backtest = simple_backtest.run_simple_backtest
            
            def run_timeframe_backtest():
                return original_backtest(days=timeframe['days'], initial_capital=initial_capital)
            
            # Run the backtest
            result = run_timeframe_backtest()
            
            # Add timeframe information
            if result:
                result['timeframe_info'] = {
                    'name': timeframe['name'],
                    'days': timeframe['days'],
                    'description': timeframe['description']
                }
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Error running {timeframe['name']} backtest: {e}")
            return None
    
    def display_timeframe_result(self, timeframe: Dict[str, Any], result: Dict[str, Any]):
        """Display results for a single timeframe"""
        try:
            summary = result.get('backtest_summary', {})
            trade_metrics = result.get('trade_metrics', {})
            
            total_return = summary.get('total_return', 0)
            win_rate = trade_metrics.get('win_rate', 0)
            sharpe_ratio = summary.get('sharpe_ratio', 0)
            profit_factor = trade_metrics.get('profit_factor', 0)
            total_trades = trade_metrics.get('total_trades', 0)
            
            # Determine performance status
            if total_return >= 15 and win_rate >= 60:
                status = "🎉 EXCELLENT"
            elif total_return >= 10 and win_rate >= 50:
                status = "✅ GOOD"
            elif total_return >= 5 and win_rate >= 40:
                status = "👍 ACCEPTABLE"
            elif total_return >= 0:
                status = "⚠️ NEEDS IMPROVEMENT"
            else:
                status = "❌ POOR"
            
            print(f"   📈 Total Return: {total_return:.2f}%")
            print(f"   🎯 Win Rate: {win_rate:.2f}%")
            print(f"   📊 Sharpe Ratio: {sharpe_ratio:.2f}")
            print(f"   💰 Profit Factor: {profit_factor:.2f}")
            print(f"   🔄 Total Trades: {total_trades}")
            print(f"   {status}")
            
        except Exception as e:
            print(f"   ❌ Error displaying results: {e}")
    
    def generate_comprehensive_analysis(self, all_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive analysis across all timeframes"""
        try:
            print("📊 GENERATING COMPREHENSIVE ANALYSIS...")
            
            if not all_results:
                return {'error': 'No results available for analysis'}
            
            # Aggregate metrics
            returns = []
            win_rates = []
            sharpe_ratios = []
            profit_factors = []
            trade_counts = []
            
            for timeframe_name, result in all_results.items():
                summary = result.get('backtest_summary', {})
                trade_metrics = result.get('trade_metrics', {})
                
                returns.append(summary.get('total_return', 0))
                win_rates.append(trade_metrics.get('win_rate', 0))
                sharpe_ratios.append(summary.get('sharpe_ratio', 0))
                profit_factors.append(trade_metrics.get('profit_factor', 0))
                trade_counts.append(trade_metrics.get('total_trades', 0))
            
            # Calculate statistics
            analysis = {
                'timeframes_tested': len(all_results),
                'performance_summary': {
                    'average_return': np.mean(returns),
                    'median_return': np.median(returns),
                    'best_return': max(returns),
                    'worst_return': min(returns),
                    'return_std': np.std(returns),
                    'average_win_rate': np.mean(win_rates),
                    'best_win_rate': max(win_rates),
                    'worst_win_rate': min(win_rates),
                    'average_sharpe_ratio': np.mean(sharpe_ratios),
                    'best_sharpe_ratio': max(sharpe_ratios),
                    'worst_sharpe_ratio': min(sharpe_ratios),
                    'average_profit_factor': np.mean(profit_factors),
                    'best_profit_factor': max(profit_factors),
                    'worst_profit_factor': min(profit_factors),
                    'total_trades': sum(trade_counts)
                },
                'consistency_analysis': {
                    'positive_return_ratio': len([r for r in returns if r > 0]) / len(returns),
                    'high_win_rate_ratio': len([w for w in win_rates if w >= 50]) / len(win_rates),
                    'profitable_ratio': len([p for p in profit_factors if p > 1.0]) / len(profit_factors),
                    'performance_consistency': 1 - (np.std(returns) / (np.mean(returns) + 1e-9))
                },
                'timeframe_rankings': self.rank_timeframes(all_results),
                'recommendations': self.generate_timeframe_recommendations(all_results)
            }
            
            # Display analysis
            self.display_comprehensive_analysis(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"❌ Error generating comprehensive analysis: {e}")
            return {'error': str(e)}
    
    def rank_timeframes(self, all_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rank timeframes by performance"""
        try:
            rankings = []
            
            for timeframe_name, result in all_results.items():
                summary = result.get('backtest_summary', {})
                trade_metrics = result.get('trade_metrics', {})
                
                total_return = summary.get('total_return', 0)
                win_rate = trade_metrics.get('win_rate', 0)
                sharpe_ratio = summary.get('sharpe_ratio', 0)
                profit_factor = trade_metrics.get('profit_factor', 0)
                
                # Calculate composite score
                score = (total_return * 0.4 + 
                        win_rate * 0.3 + 
                        sharpe_ratio * 10 * 0.2 +  # Scale Sharpe ratio
                        profit_factor * 5 * 0.1)    # Scale profit factor
                
                rankings.append({
                    'timeframe': timeframe_name,
                    'total_return': total_return,
                    'win_rate': win_rate,
                    'sharpe_ratio': sharpe_ratio,
                    'profit_factor': profit_factor,
                    'composite_score': score
                })
            
            # Sort by composite score (descending)
            rankings.sort(key=lambda x: x['composite_score'], reverse=True)
            
            return rankings
            
        except Exception as e:
            self.logger.error(f"❌ Error ranking timeframes: {e}")
            return []
    
    def generate_timeframe_recommendations(self, all_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on timeframe analysis"""
        try:
            recommendations = []
            
            # Analyze performance patterns
            rankings = self.rank_timeframes(all_results)
            
            if not rankings:
                return ["No data available for recommendations"]
            
            # Best performing timeframe
            best = rankings[0]
            recommendations.append(f"🏆 Best performing timeframe: {best['timeframe']} with {best['total_return']:.2f}% return")
            
            # Consistency analysis
            returns = [r['total_return'] for r in rankings]
            if len([r for r in returns if r > 0]) / len(returns) >= 0.8:
                recommendations.append("✅ Algorithm shows consistent positive performance across timeframes")
            else:
                recommendations.append("⚠️ Algorithm performance varies significantly across timeframes")
            
            # Trade frequency analysis
            trade_counts = []
            for result in all_results.values():
                trade_metrics = result.get('trade_metrics', {})
                trade_counts.append(trade_metrics.get('total_trades', 0))
            
            avg_trades_per_day = np.mean(trade_counts) / np.mean([tf['days'] for tf in self.timeframes[:len(trade_counts)]])
            
            if avg_trades_per_day < 0.1:
                recommendations.append("📊 Consider increasing trade frequency for better capital utilization")
            elif avg_trades_per_day > 1.0:
                recommendations.append("📊 Trade frequency is good - maintain current approach")
            else:
                recommendations.append("📊 Trade frequency is moderate - consider optimization")
            
            # Risk-adjusted performance
            sharpe_ratios = [r['sharpe_ratio'] for r in rankings]
            avg_sharpe = np.mean(sharpe_ratios)
            
            if avg_sharpe > 1.0:
                recommendations.append("🎯 Excellent risk-adjusted performance across timeframes")
            elif avg_sharpe > 0.5:
                recommendations.append("🎯 Good risk-adjusted performance - room for improvement")
            else:
                recommendations.append("⚠️ Poor risk-adjusted performance - focus on risk management")
            
            # Optimization suggestions
            if max(returns) - min(returns) > 20:
                recommendations.append("🔧 High performance variance - consider adaptive parameters for different timeframes")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"❌ Error generating recommendations: {e}")
            return ["Error generating recommendations"]
    
    def display_comprehensive_analysis(self, analysis: Dict[str, Any]):
        """Display comprehensive analysis results"""
        try:
            print("📊 COMPREHENSIVE ANALYSIS RESULTS:")
            print("=" * 60)
            
            summary = analysis.get('performance_summary', {})
            
            print(f"🎯 Performance Summary:")
            print(f"   Average Return: {summary.get('average_return', 0):.2f}%")
            print(f"   Best Return: {summary.get('best_return', 0):.2f}%")
            print(f"   Worst Return: {summary.get('worst_return', 0):.2f}%")
            print(f"   Average Win Rate: {summary.get('average_win_rate', 0):.2f}%")
            print(f"   Average Sharpe Ratio: {summary.get('average_sharpe_ratio', 0):.2f}")
            print(f"   Average Profit Factor: {summary.get('average_profit_factor', 0):.2f}")
            print(f"   Total Trades: {summary.get('total_trades', 0)}")
            
            consistency = analysis.get('consistency_analysis', {})
            print(f"\n📈 Consistency Analysis:")
            print(f"   Positive Return Ratio: {consistency.get('positive_return_ratio', 0):.2%}")
            print(f"   High Win Rate Ratio: {consistency.get('high_win_rate_ratio', 0):.2%}")
            print(f"   Profitable Ratio: {consistency.get('profitable_ratio', 0):.2%}")
            print(f"   Performance Consistency: {consistency.get('performance_consistency', 0):.2%}")
            
            rankings = analysis.get('timeframe_rankings', [])
            if rankings:
                print(f"\n🏆 Timeframe Rankings:")
                for i, ranking in enumerate(rankings, 1):
                    print(f"   {i}. {ranking['timeframe']}: {ranking['total_return']:.2f}% return (Score: {ranking['composite_score']:.2f})")
            
            recommendations = analysis.get('recommendations', [])
            if recommendations:
                print(f"\n💡 Recommendations:")
                for rec in recommendations:
                    print(f"   {rec}")
            
        except Exception as e:
            print(f"❌ Error displaying analysis: {e}")
    
    def save_multi_timeframe_results(self, all_results: Dict[str, Any], analysis: Dict[str, Any]):
        """Save multi-timeframe results to file"""
        try:
            filename = f"multi_timeframe_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            results_data = {
                'timestamp': datetime.now().isoformat(),
                'timeframes_tested': len(all_results),
                'individual_results': all_results,
                'comprehensive_analysis': analysis
            }
            
            with open(filename, 'w') as f:
                json.dump(results_data, f, indent=2, default=str)
            
            print(f"📄 Multi-timeframe results saved to: {filename}")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving results: {e}")

def main():
    """Main function to run multi-timeframe backtesting"""
    try:
        # Initialize multi-timeframe backtester
        backtester = MultiTimeframeBacktester()
        
        # Run all timeframes
        results = backtester.run_all_timeframes(initial_capital=10000)
        
        if 'error' in results:
            print(f"❌ Multi-timeframe backtesting failed: {results['error']}")
            return
        
        print("\n🎉 MULTI-TIMEFRAME BACKTESTING SUCCESSFULLY COMPLETED!")
        print("📊 Algorithm performance tested across multiple time horizons")
        print("🎯 Comprehensive analysis and recommendations generated")
        
    except Exception as e:
        print(f"❌ Error in main execution: {e}")

if __name__ == "__main__":
    main()

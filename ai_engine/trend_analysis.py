"""
Trend Analysis Module
This module handles trend detection, prediction, and analysis for market data
"""

import numpy as np
import pandas as pd
import logging
from typing import List, Dict, Tuple, Optional, Any
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrendDetector:
    """
    Detects trends in time series data using various statistical methods
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
    
    def detect_trend_direction(self, data: List[float], method: str = 'linear_regression') -> Dict[str, Any]:
        """
        Detect trend direction in time series data
        
        Args:
            data: List of numerical values
            method: Method for trend detection ('linear_regression', 'moving_average', 'mann_kendall')
        
        Returns:
            Dictionary with trend analysis results
        """
        try:
            if len(data) < 3:
                return {'direction': 'insufficient_data', 'strength': 0, 'confidence': 0}
            
            data_array = np.array(data)
            
            if method == 'linear_regression':
                return self._linear_regression_trend(data_array)
            elif method == 'moving_average':
                return self._moving_average_trend(data_array)
            elif method == 'mann_kendall':
                return self._mann_kendall_trend(data_array)
            else:
                return self._linear_regression_trend(data_array)
                
        except Exception as e:
            logger.error(f"Trend detection failed: {e}")
            return {'direction': 'error', 'strength': 0, 'confidence': 0, 'error': str(e)}
    
    def _linear_regression_trend(self, data: np.ndarray) -> Dict[str, Any]:
        """Detect trend using linear regression"""
        try:
            x = np.arange(len(data)).reshape(-1, 1)
            y = data
            
            model = LinearRegression()
            model.fit(x, y)
            
            slope = model.coef_[0]
            r2 = model.score(x, y)
            
            # Determine direction
            if slope > 0.01:
                direction = 'increasing'
            elif slope < -0.01:
                direction = 'decreasing'
            else:
                direction = 'stable'
            
            # Calculate strength based on slope magnitude
            strength = abs(slope)
            
            # Confidence based on R²
            confidence = r2
            
            return {
                'direction': direction,
                'strength': strength,
                'confidence': confidence,
                'slope': slope,
                'r_squared': r2,
                'method': 'linear_regression'
            }
        except Exception as e:
            logger.error(f"Linear regression trend detection failed: {e}")
            return {'direction': 'error', 'strength': 0, 'confidence': 0}
    
    def _moving_average_trend(self, data: np.ndarray, window_size: int = 3) -> Dict[str, Any]:
        """Detect trend using moving average comparison"""
        try:
            if len(data) < window_size * 2:
                return self._linear_regression_trend(data)
            
            # Calculate moving averages
            ma = pd.Series(data).rolling(window=window_size).mean().dropna()
            
            # Compare first and last moving average
            first_ma = ma.iloc[window_size-1]
            last_ma = ma.iloc[-1]
            
            change = last_ma - first_ma
            pct_change = (change / first_ma) * 100 if first_ma != 0 else 0
            
            # Determine direction
            if pct_change > 5:
                direction = 'increasing'
            elif pct_change < -5:
                direction = 'decreasing'
            else:
                direction = 'stable'
            
            # Strength based on percentage change
            strength = abs(pct_change) / 100
            
            # Confidence based on data consistency
            volatility = np.std(data) / np.mean(data) if np.mean(data) != 0 else 1
            confidence = max(0, 1 - volatility)
            
            return {
                'direction': direction,
                'strength': strength,
                'confidence': confidence,
                'percentage_change': pct_change,
                'window_size': window_size,
                'method': 'moving_average'
            }
        except Exception as e:
            logger.error(f"Moving average trend detection failed: {e}")
            return {'direction': 'error', 'strength': 0, 'confidence': 0}
    
    def _mann_kendall_trend(self, data: np.ndarray) -> Dict[str, Any]:
        """Mann-Kendall trend test (non-parametric)"""
        try:
            n = len(data)
            
            # Calculate Mann-Kendall test statistic
            s = 0
            for i in range(n - 1):
                for j in range(i + 1, n):
                    if data[j] > data[i]:
                        s += 1
                    elif data[j] < data[i]:
                        s -= 1
            
            # Calculate variance
            var_s = n * (n - 1) * (2 * n + 5) / 18
            
            # Calculate z-score
            if s > 0:
                z = (s - 1) / np.sqrt(var_s)
            elif s < 0:
                z = (s + 1) / np.sqrt(var_s)
            else:
                z = 0
            
            # Determine direction and significance
            alpha = 0.05  # significance level
            z_alpha = 1.96  # critical value for two-tailed test
            
            if abs(z) > z_alpha:
                if z > 0:
                    direction = 'increasing'
                else:
                    direction = 'decreasing'
                confidence = 1 - alpha
            else:
                direction = 'no_trend'
                confidence = alpha
            
            # Strength based on z-score magnitude
            strength = min(abs(z) / z_alpha, 1.0)
            
            return {
                'direction': direction,
                'strength': strength,
                'confidence': confidence,
                'mann_kendall_s': s,
                'z_score': z,
                'method': 'mann_kendall'
            }
        except Exception as e:
            logger.error(f"Mann-Kendall trend detection failed: {e}")
            return {'direction': 'error', 'strength': 0, 'confidence': 0}
    
    def detect_seasonality(self, data: List[float], period: int = 7) -> Dict[str, Any]:
        """
        Detect seasonal patterns in time series data
        
        Args:
            data: List of numerical values
            period: Expected seasonal period (e.g., 7 for weekly, 12 for monthly)
        
        Returns:
            Dictionary with seasonality analysis results
        """
        try:
            if len(data) < period * 2:
                return {'has_seasonality': False, 'strength': 0, 'period': period}
            
            data_array = np.array(data)
            
            # Calculate autocorrelation for the given period
            n = len(data_array)
            autocorr = []
            
            for lag in range(1, min(period + 1, n // 2)):
                if n - lag < 2:
                    break
                    
                series1 = data_array[:n - lag]
                series2 = data_array[lag:]
                
                correlation = np.corrcoef(series1, series2)[0, 1]
                autocorr.append(correlation)
            
            if not autocorr:
                return {'has_seasonality': False, 'strength': 0, 'period': period}
            
            # Find peak autocorrelation
            max_autocorr = max(autocorr)
            best_lag = autocorr.index(max_autocorr) + 1
            
            # Determine if seasonality exists
            threshold = 0.3  # Minimum autocorrelation to consider seasonal
            has_seasonality = max_autocorr > threshold
            strength = max_autocorr if has_seasonality else 0
            
            return {
                'has_seasonality': has_seasonality,
                'strength': strength,
                'detected_period': best_lag,
                'expected_period': period,
                'autocorrelations': autocorr,
                'max_autocorrelation': max_autocorr
            }
        except Exception as e:
            logger.error(f"Seasonality detection failed: {e}")
            return {'has_seasonality': False, 'strength': 0, 'error': str(e)}

class TrendPredictor:
    """
    Predicts future trends using machine learning models
    """
    
    def __init__(self):
        self.models = {
            'linear': LinearRegression(),
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        self.scaler = StandardScaler()
    
    def prepare_features(self, data: List[float], lookback: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare features for time series prediction
        
        Args:
            data: List of historical values
            lookback: Number of previous values to use as features
        
        Returns:
            Tuple of (X, y) arrays
        """
        try:
            if len(data) <= lookback:
                return np.array([]), np.array([])
            
            # Create sequences
            X, y = [], []
            for i in range(lookback, len(data)):
                X.append(data[i-lookback:i])
                y.append(data[i])
            
            return np.array(X), np.array(y)
        except Exception as e:
            logger.error(f"Feature preparation failed: {e}")
            return np.array([]), np.array([])
    
    def train_models(self, data: List[float], lookback: int = 5) -> Dict[str, Any]:
        """
        Train prediction models
        
        Args:
            data: Historical data for training
            lookback: Number of previous values to use as features
        
        Returns:
            Dictionary with training results
        """
        try:
            X, y = self.prepare_features(data, lookback)
            
            if len(X) == 0:
                return {'error': 'Insufficient data for training'}
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            training_results = {}
            
            for name, model in self.models.items():
                try:
                    # Train model
                    model.fit(X_scaled, y)
                    
                    # Make predictions
                    y_pred = model.predict(X_scaled)
                    
                    # Calculate metrics
                    mse = mean_squared_error(y, y_pred)
                    r2 = r2_score(y, y_pred)
                    
                    training_results[name] = {
                        'mse': mse,
                        'r2_score': r2,
                        'rmse': np.sqrt(mse),
                        'trained': True
                    }
                    
                    logger.info(f"Model {name} trained - R²: {r2:.3f}, RMSE: {np.sqrt(mse):.3f}")
                    
                except Exception as e:
                    logger.error(f"Failed to train model {name}: {e}")
                    training_results[name] = {'error': str(e), 'trained': False}
            
            return training_results
            
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            return {'error': str(e)}
    
    def predict_trend(self, data: List[float], steps_ahead: int = 5, model_name: str = 'random_forest') -> Dict[str, Any]:
        """
        Predict future trend values
        
        Args:
            data: Historical data
            steps_ahead: Number of future steps to predict
            model_name: Which model to use for prediction
        
        Returns:
            Dictionary with prediction results
        """
        try:
            if model_name not in self.models:
                return {'error': f'Unknown model: {model_name}'}
            
            model = self.models[model_name]
            lookback = 5  # Default lookback period
            
            X, y = self.prepare_features(data, lookback)
            
            if len(X) == 0:
                return {'error': 'Insufficient data for prediction'}
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Train model if not already trained
            try:
                model.fit(X_scaled, y)
            except:
                return {'error': 'Failed to train model for prediction'}
            
            # Make predictions
            predictions = []
            current_sequence = data[-lookback:]
            
            for _ in range(steps_ahead):
                # Prepare current sequence
                current_X = np.array(current_sequence[-lookback:]).reshape(1, -1)
                current_X_scaled = self.scaler.transform(current_X)
                
                # Predict next value
                next_pred = model.predict(current_X_scaled)[0]
                predictions.append(next_pred)
                
                # Update sequence
                current_sequence.append(next_pred)
            
            # Calculate prediction intervals (simple approach)
            residuals = y - model.predict(X_scaled)
            std_error = np.std(residuals)
            
            prediction_intervals = []
            for pred in predictions:
                lower = pred - 1.96 * std_error
                upper = pred + 1.96 * std_error
                prediction_intervals.append((lower, upper))
            
            # Detect trend in predictions
            trend_detector = TrendDetector()
            trend_analysis = trend_detector.detect_trend_direction(predictions)
            
            return {
                'predictions': predictions,
                'prediction_intervals': prediction_intervals,
                'steps_ahead': steps_ahead,
                'model_used': model_name,
                'trend_direction': trend_analysis['direction'],
                'trend_strength': trend_analysis['strength'],
                'std_error': std_error,
                'last_actual_value': data[-1] if data else None,
                'predicted_at': datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Trend prediction failed: {e}")
            return {'error': str(e)}

class MarketTrendAnalyzer:
    """
    Comprehensive market trend analyzer combining multiple analysis methods
    """
    
    def __init__(self):
        self.trend_detector = TrendDetector()
        self.trend_predictor = TrendPredictor()
    
    def analyze_keyword_trends(self, trend_data: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Analyze trends for multiple keywords
        
        Args:
            trend_data: Dictionary with trend data for each keyword
        
        Returns:
            Dictionary with comprehensive trend analysis
        """
        try:
            analysis_results = {}
            
            for keyword, data in trend_data.items():
                if 'timeline' not in data or not data['timeline']:
                    continue
                
                timeline = data['timeline']
                
                # Detect current trend
                current_trend = self.trend_detector.detect_trend_direction(timeline)
                
                # Detect seasonality
                seasonality = self.trend_detector.detect_seasonality(timeline)
                
                # Predict future trend
                prediction = self.trend_predictor.predict_trend(timeline, steps_ahead=7)
                
                # Calculate additional metrics
                volatility = np.std(timeline) if len(timeline) > 1 else 0
                avg_value = np.mean(timeline)
                growth_rate = ((timeline[-1] - timeline[0]) / timeline[0] * 100) if timeline[0] != 0 else 0
                
                analysis_results[keyword] = {
                    'current_value': timeline[-1] if timeline else 0,
                    'average_value': avg_value,
                    'volatility': volatility,
                    'growth_rate': growth_rate,
                    'current_trend': current_trend,
                    'seasonality': seasonality,
                    'prediction': prediction,
                    'data_points': len(timeline),
                    'analyzed_at': datetime.utcnow()
                }
            
            # Generate summary
            summary = self._generate_trend_summary(analysis_results)
            
            return {
                'keyword_analysis': analysis_results,
                'summary': summary,
                'total_keywords': len(analysis_results),
                'analysis_timestamp': datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Keyword trend analysis failed: {e}")
            return {'error': str(e)}
    
    def analyze_market_sentiment_trends(self, sentiment_data: List[Dict]) -> Dict[str, Any]:
        """
        Analyze trends in sentiment data over time
        
        Args:
            sentiment_data: List of sentiment analysis results with timestamps
        
        Returns:
            Dictionary with sentiment trend analysis
        """
        try:
            if not sentiment_data:
                return {'error': 'No sentiment data provided'}
            
            # Convert to DataFrame
            df = pd.DataFrame(sentiment_data)
            
            # Extract timestamps and compound scores
            timestamps = pd.to_datetime(df['sentiment_analyzed_at'])
            compound_scores = df['sentiment'].apply(lambda x: x.get('compound', 0) if isinstance(x, dict) else 0)
            
            # Sort by timestamp
            sorted_indices = np.argsort(timestamps)
            sorted_scores = compound_scores.iloc[sorted_indices].tolist()
            
            if len(sorted_scores) < 3:
                return {'error': 'Insufficient sentiment data for trend analysis'}
            
            # Detect trend
            sentiment_trend = self.trend_detector.detect_trend_direction(sorted_scores)
            
            # Predict future sentiment
            sentiment_prediction = self.trend_predictor.predict_trend(sorted_scores, steps_ahead=7)
            
            # Calculate sentiment volatility
            sentiment_volatility = np.std(sorted_scores)
            
            # Identify sentiment turning points
            turning_points = self._find_turning_points(sorted_scores)
            
            return {
                'sentiment_trend': sentiment_trend,
                'prediction': sentiment_prediction,
                'volatility': sentiment_volatility,
                'turning_points': turning_points,
                'data_points': len(sorted_scores),
                'time_span_days': (timestamps.max() - timestamps.min()).days,
                'analyzed_at': datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Sentiment trend analysis failed: {e}")
            return {'error': str(e)}
    
    def _generate_trend_summary(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate summary statistics for trend analysis"""
        try:
            if not analysis_results:
                return {}
            
            # Count trends by direction
            trend_directions = {}
            volatilities = []
            growth_rates = []
            
            for keyword, data in analysis_results.items():
                direction = data['current_trend']['direction']
                trend_directions[direction] = trend_directions.get(direction, 0) + 1
                volatilities.append(data['volatility'])
                growth_rates.append(data['growth_rate'])
            
            summary = {
                'trend_distribution': trend_directions,
                'average_volatility': np.mean(volatilities) if volatilities else 0,
                'average_growth_rate': np.mean(growth_rates) if growth_rates else 0,
                'top_performing_keywords': [],
                'declining_keywords': [],
                'high_volatility_keywords': []
            }
            
            # Find top performing and declining keywords
            for keyword, data in analysis_results.items():
                if data['growth_rate'] > 20:
                    summary['top_performing_keywords'].append(keyword)
                elif data['growth_rate'] < -20:
                    summary['declining_keywords'].append(keyword)
                
                if data['volatility'] > np.percentile(volatilities, 75):
                    summary['high_volatility_keywords'].append(keyword)
            
            return summary
            
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            return {}
    
    def _find_turning_points(self, data: List[float], window_size: int = 3) -> List[int]:
        """Find turning points in time series data"""
        try:
            if len(data) < window_size * 2:
                return []
            
            turning_points = []
            
            for i in range(window_size, len(data) - window_size):
                before_window = data[i-window_size:i]
                after_window = data[i+1:i+1+window_size]
                
                before_avg = np.mean(before_window)
                after_avg = np.mean(after_window)
                
                # Check for significant change in direction
                if abs(after_avg - before_avg) > np.std(data) * 0.5:
                    turning_points.append(i)
            
            return turning_points
            
        except Exception as e:
            logger.error(f"Turning point detection failed: {e}")
            return []

# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = MarketTrendAnalyzer()
    
    # Test trend detection
    test_data = [10, 12, 15, 14, 18, 20, 22, 21, 25, 28, 30, 32]
    print("Testing trend detection...")
    trend_result = analyzer.trend_detector.detect_trend_direction(test_data)
    print(f"Trend direction: {trend_result['direction']}, Strength: {trend_result['strength']:.3f}")
    
    # Test trend prediction
    print("\nTesting trend prediction...")
    prediction = analyzer.trend_predictor.predict_trend(test_data, steps_ahead=5)
    print(f"Predictions: {[round(p, 2) for p in prediction['predictions']]}")
    print(f"Predicted trend: {prediction['trend_direction']}")
    
    # Test keyword trend analysis
    print("\nTesting keyword trend analysis...")
    sample_trend_data = {
        'AI market': {
            'timeline': [45, 48, 52, 55, 58, 62, 65, 68, 70, 73, 75, 78],
            'volume': [1000, 1200, 1100, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100]
        },
        'cryptocurrency': {
            'timeline': [80, 75, 70, 72, 68, 65, 63, 60, 58, 55, 52, 50],
            'volume': [2000, 1800, 1600, 1700, 1500, 1400, 1300, 1200, 1100, 1000, 900, 800]
        }
    }
    
    keyword_analysis = analyzer.analyze_keyword_trends(sample_trend_data)
    print(f"Analyzed {keyword_analysis['total_keywords']} keywords")
    for keyword, data in keyword_analysis['keyword_analysis'].items():
        print(f"{keyword}: Trend = {data['current_trend']['direction']}, Growth = {data['growth_rate']:.1f}%")

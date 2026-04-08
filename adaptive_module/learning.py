"""
Adaptive Learning Module
This module implements machine learning capabilities to improve system performance over time
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import json
import os
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LearningType(Enum):
    """Types of learning the system can perform"""
    RULE_OPTIMIZATION = "rule_optimization"
    SENTIMENT_IMPROVEMENT = "sentiment_improvement"
    TREND_PREDICTION = "trend_prediction"
    DECISION_ACCURACY = "decision_accuracy"
    ANOMALY_DETECTION = "anomaly_detection"

class ModelType(Enum):
    """Types of ML models"""
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"

@dataclass
class LearningResult:
    """Data class representing learning results"""
    learning_type: LearningType
    model_type: ModelType
    accuracy_score: float
    improvement_score: float
    old_performance: float
    new_performance: float
    model_path: str
    features_used: List[str]
    training_samples: int
    timestamp: datetime
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'learning_type': self.learning_type.value,
            'model_type': self.model_type.value,
            'accuracy_score': self.accuracy_score,
            'improvement_score': self.improvement_score,
            'old_performance': self.old_performance,
            'new_performance': self.new_performance,
            'model_path': self.model_path,
            'features_used': self.features_used,
            'training_samples': self.training_samples,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }

class AdaptiveLearningEngine:
    """
    Main adaptive learning engine that improves system performance over time
    """
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.learning_history: List[LearningResult] = []
        
        # Create model directory if it doesn't exist
        os.makedirs(model_dir, exist_ok=True)
        
        # Initialize learning configurations
        self.learning_configs = {
            LearningType.RULE_OPTIMIZATION: {
                'model_type': ModelType.CLASSIFICATION,
                'features': ['market_growth', 'sentiment_score', 'volatility', 'competitor_activity'],
                'target': 'rule_success',
                'min_samples': 50
            },
            LearningType.SENTIMENT_IMPROVEMENT: {
                'model_type': ModelType.REGRESSION,
                'features': ['text_length', 'keyword_density', 'source_reliability'],
                'target': 'sentiment_accuracy',
                'min_samples': 100
            },
            LearningType.TREND_PREDICTION: {
                'model_type': ModelType.REGRESSION,
                'features': ['historical_trend', 'volume', 'volatility', 'seasonal_factor'],
                'target': 'future_trend',
                'min_samples': 30
            },
            LearningType.DECISION_ACCURACY: {
                'model_type': ModelType.CLASSIFICATION,
                'features': ['decision_priority', 'confidence_score', 'market_conditions'],
                'target': 'decision_outcome',
                'min_samples': 25
            }
        }
        
        # Load existing models
        self._load_existing_models()
    
    def _load_existing_models(self):
        """Load existing trained models"""
        try:
            for learning_type in LearningType:
                model_path = os.path.join(self.model_dir, f"{learning_type.value}_model.joblib")
                scaler_path = os.path.join(self.model_dir, f"{learning_type.value}_scaler.joblib")
                
                if os.path.exists(model_path):
                    self.models[learning_type] = joblib.load(model_path)
                    logger.info(f"Loaded model for {learning_type.value}")
                
                if os.path.exists(scaler_path):
                    self.scalers[learning_type] = joblib.load(scaler_path)
                    
        except Exception as e:
            logger.error(f"Error loading existing models: {e}")
    
    def learn_from_data(self, 
                       learning_type: LearningType, 
                       training_data: List[Dict[str, Any]]) -> Optional[LearningResult]:
        """
        Train a model from collected data
        
        Args:
            learning_type: Type of learning to perform
            training_data: Training data samples
        
        Returns:
            LearningResult if training successful, None otherwise
        """
        try:
            logger.info(f"Starting learning for {learning_type.value}")
            
            config = self.learning_configs.get(learning_type)
            if not config:
                logger.error(f"No configuration found for {learning_type.value}")
                return None
            
            # Check minimum samples
            if len(training_data) < config['min_samples']:
                logger.warning(f"Insufficient data for {learning_type.value}. Need {config['min_samples']}, got {len(training_data)}")
                return None
            
            # Prepare data
            X, y = self._prepare_training_data(training_data, config)
            
            if X is None or y is None:
                logger.error(f"Failed to prepare training data for {learning_type.value}")
                return None
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = self._create_model(config['model_type'])
            model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            predictions = model.predict(X_test_scaled)
            
            if config['model_type'] == ModelType.CLASSIFICATION:
                accuracy = accuracy_score(y_test, predictions)
                performance_score = accuracy
            else:
                mse = mean_squared_error(y_test, predictions)
                accuracy = 1 - (mse / np.var(y_test))  # Normalized MSE
                performance_score = accuracy
            
            # Calculate improvement
            old_performance = self._get_previous_performance(learning_type)
            improvement = performance_score - old_performance if old_performance > 0 else 0
            
            # Save model
            model_path = os.path.join(self.model_dir, f"{learning_type.value}_model.joblib")
            scaler_path = os.path.join(self.model_dir, f"{learning_type.value}_scaler.joblib")
            
            joblib.dump(model, model_path)
            joblib.dump(scaler, scaler_path)
            
            # Store in memory
            self.models[learning_type] = model
            self.scalers[learning_type] = scaler
            
            # Create learning result
            result = LearningResult(
                learning_type=learning_type,
                model_type=config['model_type'],
                accuracy_score=accuracy,
                improvement_score=improvement,
                old_performance=old_performance,
                new_performance=performance_score,
                model_path=model_path,
                features_used=config['features'],
                training_samples=len(training_data),
                timestamp=datetime.utcnow(),
                metadata={
                    'config': config,
                    'test_samples': len(X_test),
                    'cross_val_score': self._calculate_cross_val_score(model, X_train_scaled, y_train)
                }
            )
            
            self.learning_history.append(result)
            logger.info(f"Successfully trained model for {learning_type.value}. Accuracy: {accuracy:.3f}, Improvement: {improvement:.3f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in learning process for {learning_type.value}: {e}")
            return None
    
    def _prepare_training_data(self, 
                              training_data: List[Dict[str, Any]], 
                              config: Dict[str, Any]) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """Prepare training data features and targets"""
        try:
            # Convert to DataFrame
            df = pd.DataFrame(training_data)
            
            # Extract features
            feature_columns = config['features']
            target_column = config['target']
            
            # Check if all required columns exist
            missing_features = [col for col in feature_columns if col not in df.columns]
            if missing_features:
                logger.error(f"Missing feature columns: {missing_features}")
                return None, None
            
            if target_column not in df.columns:
                logger.error(f"Missing target column: {target_column}")
                return None, None
            
            # Extract features and target
            X = df[feature_columns].values
            y = df[target_column].values
            
            # Handle categorical targets for classification
            if config['model_type'] == ModelType.CLASSIFICATION:
                if y.dtype == 'object':
                    encoder = LabelEncoder()
                    y = encoder.fit_transform(y)
                    self.encoders[config['target']] = encoder
            
            # Remove rows with missing values
            mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
            X = X[mask]
            y = y[mask]
            
            if len(X) == 0:
                logger.error("No valid training samples after cleaning")
                return None, None
            
            return X, y
            
        except Exception as e:
            logger.error(f"Error preparing training data: {e}")
            return None, None
    
    def _create_model(self, model_type: ModelType):
        """Create appropriate ML model"""
        if model_type == ModelType.CLASSIFICATION:
            return RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == ModelType.REGRESSION:
            return RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    def _get_previous_performance(self, learning_type: LearningType) -> float:
        """Get previous performance for comparison"""
        try:
            previous_results = [r for r in self.learning_history if r.learning_type == learning_type]
            if previous_results:
                return max(r.new_performance for r in previous_results)
            return 0.0
        except:
            return 0.0
    
    def _calculate_cross_val_score(self, model, X, y) -> float:
        """Calculate cross-validation score"""
        try:
            scores = cross_val_score(model, X, y, cv=5)
            return float(np.mean(scores))
        except:
            return 0.0
    
    def predict(self, 
                learning_type: LearningType, 
                input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Make predictions using trained models
        
        Args:
            learning_type: Type of learning model to use
            input_data: Input data for prediction
        
        Returns:
            Prediction results or None if prediction fails
        """
        try:
            if learning_type not in self.models:
                logger.warning(f"No trained model available for {learning_type.value}")
                return None
            
            config = self.learning_configs.get(learning_type)
            if not config:
                return None
            
            # Prepare input features
            features = []
            for feature in config['features']:
                if feature in input_data:
                    features.append(input_data[feature])
                else:
                    logger.warning(f"Missing feature {feature} for prediction")
                    return None
            
            # Convert to numpy array and reshape
            X = np.array(features).reshape(1, -1)
            
            # Scale features
            if learning_type in self.scalers:
                X = self.scalers[learning_type].transform(X)
            
            # Make prediction
            model = self.models[learning_type]
            prediction = model.predict(X)[0]
            
            # Get prediction probability for classification
            prediction_proba = None
            if config['model_type'] == ModelType.CLASSIFICATION and hasattr(model, 'predict_proba'):
                prediction_proba = model.predict_proba(X)[0].tolist()
            
            # Decode categorical predictions
            if config['model_type'] == ModelType.CLASSIFICATION and config['target'] in self.encoders:
                encoder = self.encoders[config['target']]
                prediction = encoder.inverse_transform([prediction])[0]
                if prediction_proba:
                    classes = encoder.classes_.tolist()
                    prediction_proba = dict(zip(classes, prediction_proba))
            
            result = {
                'prediction': prediction,
                'prediction_proba': prediction_proba,
                'learning_type': learning_type.value,
                'model_type': config['model_type'].value,
                'features_used': config['features'],
                'input_features': dict(zip(config['features'], features)),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error making prediction for {learning_type.value}: {e}")
            return None
    
    def optimize_rules(self, 
                      rule_execution_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Optimize rule parameters based on execution history
        
        Args:
            rule_execution_history: History of rule executions with outcomes
        
        Returns:
            List of optimized rule configurations
        """
        try:
            logger.info("Optimizing rules based on execution history")
            
            # Group by rule
            rule_groups = {}
            for execution in rule_execution_history:
                rule_id = execution.get('rule_id')
                if rule_id:
                    if rule_id not in rule_groups:
                        rule_groups[rule_id] = []
                    rule_groups[rule_id].append(execution)
            
            optimizations = []
            
            for rule_id, executions in rule_groups.items():
                if len(executions) < 10:  # Need sufficient data
                    continue
                
                # Analyze execution patterns
                success_rate = sum(1 for e in executions if e.get('success', False)) / len(executions)
                
                # Find optimal threshold values
                optimizations.append(self._optimize_rule_thresholds(rule_id, executions, success_rate))
            
            logger.info(f"Generated {len(optimizations)} rule optimizations")
            return optimizations
            
        except Exception as e:
            logger.error(f"Error optimizing rules: {e}")
            return []
    
    def _optimize_rule_thresholds(self, 
                                 rule_id: str, 
                                 executions: List[Dict[str, Any]], 
                                 current_success_rate: float) -> Dict[str, Any]:
        """Optimize threshold values for a specific rule"""
        try:
            # Extract context data
            contexts = [e.get('context_snapshot', {}) for e in executions if e.get('context_snapshot')]
            
            if not contexts:
                return {'rule_id': rule_id, 'optimization': 'insufficient_data'}
            
            # Convert to DataFrame
            df = pd.DataFrame(contexts)
            
            # Find numerical columns that could be thresholds
            numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            optimizations = {}
            
            for col in numerical_cols:
                if len(df[col].unique()) < 2:  # Need variation
                    continue
                
                # Try different threshold values
                values = sorted(df[col].unique())
                best_threshold = None
                best_score = current_success_rate
                
                for i in range(1, len(values)):
                    threshold = (values[i-1] + values[i]) / 2
                    
                    # Calculate success rate with this threshold
                    success_count = 0
                    total_count = 0
                    
                    for j, execution in enumerate(executions):
                        if j < len(contexts):
                            context_value = contexts[j].get(col)
                            if context_value is not None:
                                total_count += 1
                                # Simulate rule with new threshold
                                if self._simulate_rule_condition(col, threshold, context_value):
                                    if execution.get('success', False):
                                        success_count += 1
                    
                    if total_count > 0:
                        new_success_rate = success_count / total_count
                        if new_success_rate > best_score:
                            best_score = new_success_rate
                            best_threshold = threshold
                
                if best_threshold is not None and best_score > current_success_rate:
                    optimizations[col] = {
                        'current_threshold': 'N/A',
                        'optimized_threshold': best_threshold,
                        'improvement': best_score - current_success_rate,
                        'new_success_rate': best_score
                    }
            
            return {
                'rule_id': rule_id,
                'current_success_rate': current_success_rate,
                'optimizations': optimizations,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error optimizing rule {rule_id}: {e}")
            return {'rule_id': rule_id, 'error': str(e)}
    
    def _simulate_rule_condition(self, column: str, threshold: float, value: float) -> bool:
        """Simulate rule condition with new threshold"""
        # Simple threshold simulation - can be enhanced
        if 'growth' in column.lower() or 'increase' in column.lower():
            return value > threshold
        elif 'sentiment' in column.lower():
            return value > threshold
        else:
            return value > threshold
    
    def detect_anomalies(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect anomalies in market data
        
        Args:
            data: Market data to analyze
        
        Returns:
            List of detected anomalies
        """
        try:
            logger.info("Detecting anomalies in market data")
            
            if not data:
                return []
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Get numerical columns
            numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            anomalies = []
            
            for col in numerical_cols:
                if len(df[col].unique()) < 3:  # Need sufficient variation
                    continue
                
                # Calculate statistics
                mean = df[col].mean()
                std = df[col].std()
                
                # Detect outliers (3 sigma rule)
                outliers = df[np.abs(df[col] - mean) > 3 * std]
                
                for idx, row in outliers.iterrows():
                    anomaly = {
                        'type': 'statistical_outlier',
                        'column': col,
                        'value': row[col],
                        'expected_range': [mean - 3*std, mean + 3*std],
                        'z_score': (row[col] - mean) / std,
                        'timestamp': row.get('timestamp', datetime.utcnow().isoformat()),
                        'severity': 'high' if abs((row[col] - mean) / std) > 4 else 'medium'
                    }
                    anomalies.append(anomaly)
            
            # Detect trend anomalies
            if len(data) >= 10:
                trend_anomalies = self._detect_trend_anomalies(df, numerical_cols)
                anomalies.extend(trend_anomalies)
            
            logger.info(f"Detected {len(anomalies)} anomalies")
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return []
    
    def _detect_trend_anomalies(self, df: pd.DataFrame, numerical_cols: List[str]) -> List[Dict[str, Any]]:
        """Detect trend anomalies in time series data"""
        anomalies = []
        
        try:
            for col in numerical_cols:
                if len(df[col]) < 10:
                    continue
                
                # Calculate moving average
                window = min(5, len(df[col]) // 2)
                if window < 2:
                    continue
                
                moving_avg = df[col].rolling(window=window).mean()
                
                # Find sudden changes
                for i in range(window, len(df)):
                    current_value = df[col].iloc[i]
                    avg_value = moving_avg.iloc[i]
                    
                    if pd.notna(avg_value):
                        change_percent = abs((current_value - avg_value) / avg_value) * 100
                        
                        if change_percent > 50:  # Significant change
                            anomaly = {
                                'type': 'trend_anomaly',
                                'column': col,
                                'current_value': current_value,
                                'expected_value': avg_value,
                                'change_percent': change_percent,
                                'timestamp': df.iloc[i].get('timestamp', datetime.utcnow().isoformat()),
                                'severity': 'high' if change_percent > 100 else 'medium'
                            }
                            anomalies.append(anomaly)
            
        except Exception as e:
            logger.error(f"Error detecting trend anomalies: {e}")
        
        return anomalies
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of learning activities"""
        try:
            if not self.learning_history:
                return {'total_learning_sessions': 0}
            
            # Group by learning type
            type_counts = {}
            type_performance = {}
            
            for result in self.learning_history:
                type_val = result.learning_type.value
                type_counts[type_val] = type_counts.get(type_val, 0) + 1
                type_performance[type_val] = type_performance.get(type_val, [])
                type_performance[type_val].append(result.accuracy_score)
            
            # Calculate statistics
            summary = {
                'total_learning_sessions': len(self.learning_history),
                'learning_types': type_counts,
                'average_performance_by_type': {},
                'best_performing_type': None,
                'total_improvements': sum(r.improvement_score for r in self.learning_history if r.improvement_score > 0),
                'models_trained': list(self.models.keys()),
                'last_learning': self.learning_history[-1].timestamp.isoformat() if self.learning_history else None
            }
            
            # Calculate average performance by type
            for type_val, scores in type_performance.items():
                summary['average_performance_by_type'][type_val] = np.mean(scores)
            
            # Find best performing type
            if summary['average_performance_by_type']:
                best_type = max(summary['average_performance_by_type'].items(), key=lambda x: x[1])
                summary['best_performing_type'] = {
                    'type': best_type[0],
                    'performance': best_type[1]
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating learning summary: {e}")
            return {'error': str(e)}
    
    def export_learning_history(self, limit: int = 100) -> Dict[str, Any]:
        """Export learning history"""
        try:
            recent_history = self.learning_history[-limit:] if limit > 0 else self.learning_history
            
            return {
                'learning_history': [r.to_dict() for r in recent_history],
                'total_exported': len(recent_history),
                'exported_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error exporting learning history: {e}")
            return {'error': str(e)}

# Example usage
if __name__ == "__main__":
    # Initialize learning engine
    engine = AdaptiveLearningEngine()
    
    # Test learning with sample data
    sample_training_data = [
        {
            'market_growth': 25,
            'sentiment_score': 0.4,
            'volatility': 15,
            'competitor_activity': 3,
            'rule_success': 1
        },
        {
            'market_growth': -5,
            'sentiment_score': -0.2,
            'volatility': 35,
            'competitor_activity': 8,
            'rule_success': 0
        },
        {
            'market_growth': 40,
            'sentiment_score': 0.6,
            'volatility': 20,
            'competitor_activity': 2,
            'rule_success': 1
        }
    ] * 20  # Repeat to get more samples
    
    print("Testing adaptive learning...")
    
    # Test rule optimization learning
    result = engine.learn_from_data(LearningType.RULE_OPTIMIZATION, sample_training_data)
    if result:
        print(f"Learning successful for {result.learning_type.value}")
        print(f"Accuracy: {result.accuracy_score:.3f}")
        print(f"Improvement: {result.improvement_score:.3f}")
    
    # Test prediction
    test_input = {
        'market_growth': 30,
        'sentiment_score': 0.5,
        'volatility': 18,
        'competitor_activity': 4
    }
    
    prediction = engine.predict(LearningType.RULE_OPTIMIZATION, test_input)
    if prediction:
        print(f"\nPrediction: {prediction['prediction']}")
        print(f"Confidence: {prediction.get('prediction_proba', 'N/A')}")
    
    # Test anomaly detection
    sample_data = [
        {'market_growth': 25, 'sentiment_score': 0.4, 'timestamp': datetime.utcnow().isoformat()},
        {'market_growth': 30, 'sentiment_score': 0.5, 'timestamp': datetime.utcnow().isoformat()},
        {'market_growth': 200, 'sentiment_score': 0.9, 'timestamp': datetime.utcnow().isoformat()},  # Anomaly
        {'market_growth': 28, 'sentiment_score': 0.3, 'timestamp': datetime.utcnow().isoformat()}
    ]
    
    anomalies = engine.detect_anomalies(sample_data)
    print(f"\nDetected {len(anomalies)} anomalies")
    for anomaly in anomalies:
        print(f"- {anomaly['type']} in {anomaly['column']}: {anomaly['value']}")
    
    # Test learning summary
    summary = engine.get_learning_summary()
    print(f"\nLearning summary:")
    print(f"Total learning sessions: {summary['total_learning_sessions']}")
    print(f"Models trained: {[m.value for m in summary['models_trained']]}")

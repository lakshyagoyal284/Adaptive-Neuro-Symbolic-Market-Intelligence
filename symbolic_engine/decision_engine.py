"""
Decision Engine Module
This module combines rule-based reasoning with AI insights to make market intelligence decisions
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum
import json
import numpy as np
from dataclasses import dataclass

from .rules import RuleEngine, MarketRule

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DecisionType(Enum):
    """Types of decisions the engine can make"""
    INVESTMENT = "investment"
    MARKETING = "marketing"
    COMPETITIVE = "competitive"
    RISK_MANAGEMENT = "risk_management"
    OPPORTUNITY = "opportunity"
    ALERT = "alert"

class DecisionPriority(Enum):
    """Priority levels for decisions"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class ConfidenceLevel(Enum):
    """Confidence levels for decisions"""
    VERY_HIGH = "very_high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"

@dataclass
class Decision:
    """Data class representing a market intelligence decision"""
    decision_id: str
    decision_type: DecisionType
    title: str
    description: str
    recommendation: str
    priority: DecisionPriority
    confidence: ConfidenceLevel
    confidence_score: float
    supporting_factors: List[str]
    risk_factors: List[str]
    data_sources: List[str]
    rules_triggered: List[str]
    timestamp: datetime
    context_snapshot: Dict[str, Any]
    action_items: List[str]
    expected_outcome: str
    time_horizon: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert decision to dictionary"""
        return {
            'decision_id': self.decision_id,
            'decision_type': self.decision_type.value,
            'title': self.title,
            'description': self.description,
            'recommendation': self.recommendation,
            'priority': self.priority.value,
            'confidence': self.confidence.value,
            'confidence_score': self.confidence_score,
            'supporting_factors': self.supporting_factors,
            'risk_factors': self.risk_factors,
            'data_sources': self.data_sources,
            'rules_triggered': self.rules_triggered,
            'timestamp': self.timestamp.isoformat(),
            'context_snapshot': self.context_snapshot,
            'action_items': self.action_items,
            'expected_outcome': self.expected_outcome,
            'time_horizon': self.time_horizon
        }

class DecisionEngine:
    """
    Main decision engine that combines rules and AI insights
    """
    
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.decision_history: List[Decision] = []
        self.decision_templates = self._initialize_decision_templates()
        self.confidence_thresholds = {
            ConfidenceLevel.VERY_HIGH: 0.9,
            ConfidenceLevel.HIGH: 0.7,
            ConfidenceLevel.MEDIUM: 0.5,
            ConfidenceLevel.LOW: 0.3,
            ConfidenceLevel.VERY_LOW: 0.0
        }
    
    def _initialize_decision_templates(self) -> Dict[str, Dict]:
        """Initialize decision templates for different scenarios"""
        return {
            'high_growth_investment': {
                'decision_type': DecisionType.INVESTMENT,
                'title_template': 'Investment Opportunity: High Market Growth Detected',
                'description_template': 'Market analysis indicates strong growth potential',
                'recommendation_template': 'Consider investment in {market_segment}. Growth rate: {market_growth}%',
                'priority': DecisionPriority.HIGH,
                'action_items': [
                    'Conduct detailed market analysis',
                    'Evaluate investment options',
                    'Assess risk factors',
                    'Set investment timeline'
                ],
                'expected_outcome': 'Capital appreciation based on market growth',
                'time_horizon': '6-12 months'
            },
            
            'negative_sentiment_marketing': {
                'decision_type': DecisionType.MARKETING,
                'title_template': 'Marketing Action Required: Negative Sentiment Alert',
                'description_template': 'Negative market sentiment requires immediate attention',
                'recommendation_template': 'Implement marketing improvement strategies. Negative sentiment: {negative_sentiment}%',
                'priority': DecisionPriority.HIGH,
                'action_items': [
                    'Analyze sentiment drivers',
                    'Develop marketing campaign',
                    'Monitor competitor responses',
                    'Measure sentiment improvement'
                ],
                'expected_outcome': 'Improved brand perception and market sentiment',
                'time_horizon': '3-6 months'
            },
            
            'competitor_price_response': {
                'decision_type': DecisionType.COMPETITIVE,
                'title_template': 'Competitive Response: Price Action Detected',
                'description_template': 'Competitor pricing changes require strategic response',
                'recommendation_template': 'Consider product launch or price adjustment. Competitor price increase: {competitor_price_increase}%',
                'priority': DecisionPriority.MEDIUM,
                'action_items': [
                    'Analyze competitor pricing strategy',
                    'Evaluate price elasticity',
                    'Consider product differentiation',
                    'Monitor market reaction'
                ],
                'expected_outcome': 'Maintained competitive position',
                'time_horizon': '1-3 months'
            },
            
            'high_demand_opportunity': {
                'decision_type': DecisionType.OPPORTUNITY,
                'title_template': 'Market Opportunity: High Demand Detected',
                'description_template': 'Strong market demand indicates expansion opportunity',
                'recommendation_template': 'Expand market presence. Demand score: {trend_demand}',
                'priority': DecisionPriority.HIGH,
                'action_items': [
                    'Assess production capacity',
                    'Evaluate distribution channels',
                    'Develop expansion strategy',
                    'Monitor demand sustainability'
                ],
                'expected_outcome': 'Increased market share and revenue',
                'time_horizon': '3-9 months'
            },
            
            'volatility_risk_alert': {
                'decision_type': DecisionType.RISK_MANAGEMENT,
                'title_template': 'Risk Alert: High Market Volatility',
                'description_template': 'Market volatility requires risk management action',
                'recommendation_template': 'Implement risk mitigation strategies. Volatility: {market_volatility}%',
                'priority': DecisionPriority.CRITICAL,
                'action_items': [
                    'Review portfolio allocation',
                    'Implement hedging strategies',
                    'Increase monitoring frequency',
                    'Prepare contingency plans'
                ],
                'expected_outcome': 'Reduced portfolio risk and volatility exposure',
                'time_horizon': 'Immediate'
            }
        }
    
    def make_decision(self, 
                     context: Dict[str, Any], 
                     ai_insights: Optional[Dict[str, Any]] = None) -> List[Decision]:
        """
        Make market intelligence decisions based on rules and AI insights
        
        Args:
            context: Market data context
            ai_insights: AI analysis results (sentiment, trends, etc.)
        
        Returns:
            List of decisions
        """
        try:
            logger.info("Making market intelligence decisions...")
            
            # Evaluate rules
            rule_results = self.rule_engine.evaluate_rules(context)
            
            # Combine context with AI insights
            enhanced_context = self._enhance_context_with_ai(context, ai_insights)
            
            # Generate decisions based on rule results
            decisions = []
            
            for rule_result in rule_results:
                if not rule_result.get('success', False):
                    continue
                
                decision = self._create_decision_from_rule(rule_result, enhanced_context)
                if decision:
                    decisions.append(decision)
            
            # Generate composite decisions from multiple rules
            composite_decisions = self._generate_composite_decisions(rule_results, enhanced_context)
            decisions.extend(composite_decisions)
            
            # Rank decisions by priority and confidence
            decisions = self._rank_decisions(decisions)
            
            # Store decisions in history
            self.decision_history.extend(decisions)
            
            logger.info(f"Generated {len(decisions)} decisions")
            return decisions
            
        except Exception as e:
            logger.error(f"Error making decisions: {e}")
            return []
    
    def _enhance_context_with_ai(self, context: Dict[str, Any], ai_insights: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Enhance context with AI insights"""
        enhanced_context = context.copy()
        
        if not ai_insights:
            return enhanced_context
        
        # Add sentiment insights
        if 'sentiment_analysis' in ai_insights:
            sentiment = ai_insights['sentiment_analysis']
            enhanced_context.update({
                'sentiment_score': sentiment.get('average_sentiment', 0),
                'sentiment_trend': sentiment.get('overall_trend', 'stable'),
                'positive_percentage': sentiment.get('positive_percentage', 0),
                'negative_percentage': sentiment.get('negative_percentage', 0)
            })
        
        # Add trend insights
        if 'trend_analysis' in ai_insights:
            trends = ai_insights['trend_analysis']
            enhanced_context.update({
                'trend_volatility': trends.get('volatility', 0),
                'trend_growth_rate': trends.get('growth_rate', 0)
            })
        
        # Add keyword-specific insights
        if 'keyword_analysis' in ai_insights:
            keyword_data = ai_insights['keyword_analysis']
            for keyword, data in keyword_data.items():
                enhanced_context[f'{keyword}_trend'] = data.get('current_trend', {}).get('direction', 'stable')
                enhanced_context[f'{keyword}_growth'] = data.get('growth_rate', 0)
        
        return enhanced_context
    
    def _create_decision_from_rule(self, rule_result: Dict[str, Any], context: Dict[str, Any]) -> Optional[Decision]:
        """Create a decision from a rule result"""
        try:
            rule_id = rule_result['rule_id']
            rule = self.rule_engine.get_rule(rule_id)
            
            if not rule:
                return None
            
            # Find matching template
            template_key = self._find_template_key(rule_id)
            template = self.decision_templates.get(template_key)
            
            if not template:
                # Create generic decision
                template = {
                    'decision_type': DecisionType.ALERT,
                    'title_template': f'Alert: {rule.name}',
                    'description_template': rule.description,
                    'recommendation_template': rule_result['action'],
                    'priority': DecisionPriority.MEDIUM,
                    'action_items': ['Monitor situation', 'Take appropriate action'],
                    'expected_outcome': 'Situation resolution',
                    'time_horizon': 'Immediate'
                }
            
            # Calculate confidence
            confidence_score = self._calculate_confidence(rule, context)
            confidence = self._map_confidence_score(confidence_score)
            
            # Extract factors
            supporting_factors, risk_factors = self._extract_factors(rule, context)
            
            # Create decision
            decision = Decision(
                decision_id=f"decision_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{rule_id}",
                decision_type=template['decision_type'],
                title=template['title_template'].format(**context),
                description=template['description_template'],
                recommendation=template['recommendation_template'].format(**context),
                priority=template['priority'],
                confidence=confidence,
                confidence_score=confidence_score,
                supporting_factors=supporting_factors,
                risk_factors=risk_factors,
                data_sources=self._identify_data_sources(context),
                rules_triggered=[rule_id],
                timestamp=datetime.utcnow(),
                context_snapshot={k: v for k, v in context.items() 
                                 if k in ['market_growth', 'sentiment_score', 'competitor_price_increase', 
                                         'trend_demand', 'market_volatility']},
                action_items=template['action_items'],
                expected_outcome=template['expected_outcome'],
                time_horizon=template['time_horizon']
            )
            
            return decision
            
        except Exception as e:
            logger.error(f"Error creating decision from rule: {e}")
            return None
    
    def _find_template_key(self, rule_id: str) -> str:
        """Find the appropriate template key for a rule"""
        template_mapping = {
            'high_growth_investment': 'high_growth_investment',
            'negative_sentiment_alert': 'negative_sentiment_marketing',
            'competitor_price_response': 'competitor_price_response',
            'high_demand_opportunity': 'high_demand_opportunity',
            'volatility_risk_alert': 'volatility_risk_alert',
            'positive_sentiment_investment': 'high_growth_investment'
        }
        
        return template_mapping.get(rule_id, 'generic')
    
    def _calculate_confidence(self, rule: MarketRule, context: Dict[str, Any]) -> float:
        """Calculate confidence score for a decision"""
        try:
            # Base confidence from rule success rate
            base_confidence = rule.get_success_rate() / 100
            
            # Adjust based on data quality
            data_quality = self._assess_data_quality(context)
            
            # Adjust based on context consistency
            context_consistency = self._assess_context_consistency(context)
            
            # Combine factors
            confidence = (base_confidence * 0.4 + data_quality * 0.3 + context_consistency * 0.3)
            
            return min(1.0, max(0.0, confidence))
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.5  # Default confidence
    
    def _assess_data_quality(self, context: Dict[str, Any]) -> float:
        """Assess the quality of context data"""
        try:
            # Check for required variables
            required_vars = ['market_growth', 'sentiment_score']
            present_vars = sum(1 for var in required_vars if var in context and context[var] is not None)
            
            # Check data ranges
            range_score = 0
            for var in required_vars:
                if var in context and context[var] is not None:
                    value = context[var]
                    if isinstance(value, (int, float)):
                        if var == 'market_growth' and -100 <= value <= 100:
                            range_score += 1
                        elif var == 'sentiment_score' and -1 <= value <= 1:
                            range_score += 1
            
            # Calculate quality score
            quality_score = (present_vars + range_score) / (len(required_vars) * 2)
            return min(1.0, quality_score)
            
        except Exception as e:
            logger.error(f"Error assessing data quality: {e}")
            return 0.5
    
    def _assess_context_consistency(self, context: Dict[str, Any]) -> float:
        """Assess consistency of context data"""
        try:
            consistency_score = 0.5  # Base score
            
            # Check for logical consistency
            if 'market_growth' in context and 'sentiment_score' in context:
                growth = context['market_growth']
                sentiment = context['sentiment_score']
                
                # High growth with negative sentiment might indicate inconsistency
                if growth > 30 and sentiment < -0.3:
                    consistency_score -= 0.2
                # High growth with positive sentiment is consistent
                elif growth > 20 and sentiment > 0.3:
                    consistency_score += 0.2
            
            # Check volatility consistency
            if 'market_volatility' in context:
                volatility = context['market_volatility']
                if volatility > 50:  # Very high volatility might indicate unreliable data
                    consistency_score -= 0.1
            
            return max(0.0, min(1.0, consistency_score))
            
        except Exception as e:
            logger.error(f"Error assessing context consistency: {e}")
            return 0.5
    
    def _map_confidence_score(self, score: float) -> ConfidenceLevel:
        """Map confidence score to confidence level"""
        for level, threshold in self.confidence_thresholds.items():
            if score >= threshold:
                return level
        return ConfidenceLevel.VERY_LOW
    
    def _extract_factors(self, rule: MarketRule, context: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Extract supporting and risk factors from context"""
        supporting_factors = []
        risk_factors = []
        
        try:
            # Analyze market growth
            if 'market_growth' in context:
                growth = context['market_growth']
                if growth > 30:
                    supporting_factors.append(f"Strong market growth ({growth}%)")
                elif growth < -10:
                    risk_factors.append(f"Negative market growth ({growth}%)")
            
            # Analyze sentiment
            if 'sentiment_score' in context:
                sentiment = context['sentiment_score']
                if sentiment > 0.3:
                    supporting_factors.append(f"Positive market sentiment ({sentiment:.2f})")
                elif sentiment < -0.3:
                    risk_factors.append(f"Negative market sentiment ({sentiment:.2f})")
            
            # Analyze volatility
            if 'market_volatility' in context:
                volatility = context['market_volatility']
                if volatility > 25:
                    risk_factors.append(f"High market volatility ({volatility}%)")
                elif volatility < 10:
                    supporting_factors.append(f"Low market volatility ({volatility}%)")
            
            # Analyze competitor activity
            if 'competitor_price_increase' in context:
                price_increase = context['competitor_price_increase']
                if price_increase > 10:
                    supporting_factors.append(f"Significant competitor price increase ({price_increase}%)")
            
            # Analyze demand
            if 'trend_demand' in context:
                demand = context['trend_demand']
                if demand > 70:
                    supporting_factors.append(f"High market demand (score: {demand})")
            
        except Exception as e:
            logger.error(f"Error extracting factors: {e}")
        
        return supporting_factors, risk_factors
    
    def _identify_data_sources(self, context: Dict[str, Any]) -> List[str]:
        """Identify data sources based on context"""
        sources = []
        
        if any(key in context for key in ['market_growth', 'market_volatility']):
            sources.append('market_data')
        
        if any(key in context for key in ['sentiment_score', 'positive_percentage', 'negative_percentage']):
            sources.append('sentiment_analysis')
        
        if any(key in context for key in ['trend_demand', 'trend_growth_rate']):
            sources.append('trend_analysis')
        
        if any(key in context for key in ['competitor_price_increase', 'market_share']):
            sources.append('competitor_intelligence')
        
        return sources or ['unknown']
    
    def _generate_composite_decisions(self, rule_results: List[Dict], context: Dict[str, Any]) -> List[Decision]:
        """Generate composite decisions from multiple rule results"""
        composite_decisions = []
        
        try:
            # Check for investment opportunity (positive growth + sentiment)
            growth_rules = [r for r in rule_results if 'growth' in r.get('rule_id', '').lower()]
            sentiment_rules = [r for r in rule_results if 'sentiment' in r.get('rule_id', '').lower()]
            
            if growth_rules and sentiment_rules:
                # Strong investment opportunity
                if any('high_growth' in r.get('rule_id', '') for r in growth_rules):
                    decision = Decision(
                        decision_id=f"composite_investment_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                        decision_type=DecisionType.INVESTMENT,
                        title="Strong Investment Opportunity: Growth and Sentiment Alignment",
                        description="Multiple indicators suggest strong investment potential",
                        recommendation="Strong buy recommendation based on growth and sentiment alignment",
                        priority=DecisionPriority.HIGH,
                        confidence=ConfidenceLevel.HIGH,
                        confidence_score=0.8,
                        supporting_factors=["Market growth indicators", "Positive sentiment analysis"],
                        risk_factors=["Market volatility", "External economic factors"],
                        data_sources=['market_data', 'sentiment_analysis'],
                        rules_triggered=[r['rule_id'] for r in growth_rules + sentiment_rules],
                        timestamp=datetime.utcnow(),
                        context_snapshot=context,
                        action_items=["Conduct detailed investment analysis", "Portfolio allocation", "Risk assessment"],
                        expected_outcome="Strong investment returns",
                        time_horizon="6-12 months"
                    )
                    composite_decisions.append(decision)
            
            # Check for risk scenario (negative indicators)
            negative_rules = [r for r in rule_results if any(neg in r.get('rule_id', '').lower() 
                            for neg in ['negative', 'volatility', 'risk'])]
            
            if len(negative_rules) >= 2:
                decision = Decision(
                    decision_id=f"composite_risk_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                    decision_type=DecisionType.RISK_MANAGEMENT,
                    title="High Risk Alert: Multiple Negative Indicators",
                    description="Multiple risk factors detected requiring immediate attention",
                    recommendation="Implement comprehensive risk management strategies",
                    priority=DecisionPriority.CRITICAL,
                    confidence=ConfidenceLevel.HIGH,
                    confidence_score=0.85,
                    supporting_factors=["Early warning detection"],
                    risk_factors=["Multiple negative market indicators", "High volatility"],
                    data_sources=['market_data', 'sentiment_analysis', 'trend_analysis'],
                    rules_triggered=[r['rule_id'] for r in negative_rules],
                    timestamp=datetime.utcnow(),
                    context_snapshot=context,
                    action_items=["Immediate portfolio review", "Risk mitigation implementation", "Increased monitoring"],
                    expected_outcome="Risk exposure reduction",
                    time_horizon="Immediate"
                )
                composite_decisions.append(decision)
            
        except Exception as e:
            logger.error(f"Error generating composite decisions: {e}")
        
        return composite_decisions
    
    def _rank_decisions(self, decisions: List[Decision]) -> List[Decision]:
        """Rank decisions by priority and confidence"""
        def sort_key(decision):
            priority_score = 5 - decision.priority.value  # Lower value = higher priority
            confidence_score = decision.confidence_score
            return (priority_score, confidence_score)
        
        return sorted(decisions, key=sort_key, reverse=True)
    
    def get_decision_summary(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get summary of recent decisions"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
            recent_decisions = [d for d in self.decision_history if d.timestamp > cutoff_time]
            
            if not recent_decisions:
                return {'total_decisions': 0, 'time_window_hours': time_window_hours}
            
            # Count by decision type
            type_counts = {}
            priority_counts = {}
            confidence_counts = {}
            
            for decision in recent_decisions:
                # Count by type
                type_counts[decision.decision_type.value] = type_counts.get(decision.decision_type.value, 0) + 1
                
                # Count by priority
                priority_counts[decision.priority.value] = priority_counts.get(decision.priority.value, 0) + 1
                
                # Count by confidence
                confidence_counts[decision.confidence.value] = confidence_counts.get(decision.confidence.value, 0) + 1
            
            # Calculate average confidence
            avg_confidence = sum(d.confidence_score for d in recent_decisions) / len(recent_decisions)
            
            # Get top decisions
            top_decisions = sorted(recent_decisions, 
                                 key=lambda d: (5 - d.priority.value, d.confidence_score), 
                                 reverse=True)[:5]
            
            return {
                'total_decisions': len(recent_decisions),
                'time_window_hours': time_window_hours,
                'decision_types': type_counts,
                'priority_distribution': priority_counts,
                'confidence_distribution': confidence_counts,
                'average_confidence': round(avg_confidence, 3),
                'top_decisions': [d.to_dict() for d in top_decisions],
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating decision summary: {e}")
            return {'error': str(e)}
    
    def export_decisions(self, limit: int = 100) -> Dict[str, Any]:
        """Export recent decisions"""
        try:
            recent_decisions = self.decision_history[-limit:] if limit > 0 else self.decision_history
            
            return {
                'decisions': [d.to_dict() for d in recent_decisions],
                'total_exported': len(recent_decisions),
                'exported_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error exporting decisions: {e}")
            return {'error': str(e)}

# Example usage
if __name__ == "__main__":
    # Initialize decision engine
    engine = DecisionEngine()
    
    # Test decision making
    test_context = {
        'market_growth': 35,
        'sentiment_score': 0.4,
        'negative_sentiment': 25,
        'competitor_price_increase': 15,
        'trend_demand': 75,
        'market_share': 12,
        'market_volatility': 30
    }
    
    test_ai_insights = {
        'sentiment_analysis': {
            'average_sentiment': 0.4,
            'overall_trend': 'improving',
            'positive_percentage': 65,
            'negative_percentage': 25
        },
        'trend_analysis': {
            'volatility': 0.15,
            'growth_rate': 12.5
        }
    }
    
    print("Testing decision engine...")
    decisions = engine.make_decision(test_context, test_ai_insights)
    print(f"Generated {len(decisions)} decisions:")
    
    for decision in decisions:
        print(f"\nDecision: {decision.title}")
        print(f"Type: {decision.decision_type.value}")
        print(f"Priority: {decision.priority.value}")
        print(f"Confidence: {decision.confidence.value} ({decision.confidence_score:.2f})")
        print(f"Recommendation: {decision.recommendation}")
        print(f"Supporting factors: {decision.supporting_factors}")
        print(f"Risk factors: {decision.risk_factors}")
    
    # Test decision summary
    print("\nDecision summary:")
    summary = engine.get_decision_summary()
    print(f"Total decisions: {summary['total_decisions']}")
    print(f"Average confidence: {summary.get('average_confidence', 0):.3f}")

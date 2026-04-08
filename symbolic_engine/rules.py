"""
Business Rules Module
This module defines and manages business rules for market intelligence decision making
"""

import re
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from enum import Enum
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RuleType(Enum):
    """Enumeration of different rule types"""
    CONDITIONAL = "conditional"
    THRESHOLD = "threshold"
    COMPARISON = "comparison"
    TEMPORAL = "temporal"
    COMPOSITE = "composite"

class RulePriority(Enum):
    """Enumeration of rule priorities"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class RuleStatus(Enum):
    """Enumeration of rule statuses"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    TESTING = "testing"
    DEPRECATED = "deprecated"

class MarketRule:
    """
    Individual business rule for market intelligence
    """
    
    def __init__(self, 
                 rule_id: str,
                 name: str,
                 description: str,
                 condition: str,
                 action: str,
                 rule_type: RuleType = RuleType.CONDITIONAL,
                 priority: RulePriority = RulePriority.MEDIUM,
                 status: RuleStatus = RuleStatus.ACTIVE,
                 parameters: Optional[Dict] = None):
        """
        Initialize a market rule
        
        Args:
            rule_id: Unique identifier for the rule
            name: Human-readable name
            description: Detailed description of the rule
            condition: Condition expression (will be evaluated)
            action: Action to take when condition is met
            rule_type: Type of rule
            priority: Priority level
            status: Current status
            parameters: Additional parameters for the rule
        """
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.condition = condition
        self.action = action
        self.rule_type = rule_type
        self.priority = priority
        self.status = status
        self.parameters = parameters or {}
        
        # Execution tracking
        self.execution_count = 0
        self.success_count = 0
        self.last_executed = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def evaluate_condition(self, context: Dict[str, Any]) -> bool:
        """
        Evaluate the rule condition against provided context
        
        Args:
            context: Dictionary containing market data and variables
        
        Returns:
            True if condition is met, False otherwise
        """
        try:
            if self.status != RuleStatus.ACTIVE:
                return False
            
            # Create safe evaluation environment
            safe_context = self._create_safe_context(context)
            
            # Evaluate condition
            result = eval(self.condition, {"__builtins__": {}}, safe_context)
            
            # Update execution tracking
            self.execution_count += 1
            self.last_executed = datetime.utcnow()
            
            if result:
                self.success_count += 1
            
            logger.debug(f"Rule {self.rule_id} evaluated: {result}")
            return bool(result)
            
        except Exception as e:
            logger.error(f"Error evaluating rule {self.rule_id}: {e}")
            return False
    
    def _create_safe_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a safe evaluation context with allowed functions"""
        safe_context = context.copy()
        
        # Add safe mathematical functions
        safe_context.update({
            'abs': abs,
            'min': min,
            'max': max,
            'len': len,
            'sum': sum,
            'any': any,
            'all': all,
            'round': round,
            'float': float,
            'int': int,
            'str': str,
            # Market-specific helper functions
            'avg': lambda x: sum(x) / len(x) if x else 0,
            'percentage': lambda part, whole: (part / whole * 100) if whole else 0,
            'is_positive': lambda x: x > 0,
            'is_negative': lambda x: x < 0,
            'is_between': lambda val, low, high: low <= val <= high,
            'is_increasing': lambda seq: all(seq[i] <= seq[i+1] for i in range(len(seq)-1)),
            'is_decreasing': lambda seq: all(seq[i] >= seq[i+1] for i in range(len(seq)-1)),
            # Add missing competitor_activity_growth variable
            'competitor_activity_growth': context.get('competitor_activity_growth', 0),
            'competitor_activity_count': context.get('competitor_activity_count', 0),
            # Add all required context variables
            'market_growth': context.get('market_growth', 0),
            'sentiment_score': context.get('sentiment_score', 0),
            'market_volatility': context.get('market_volatility', 0),
            'negative_sentiment': context.get('negative_sentiment', 0),
            'trend_demand': context.get('trend_demand', 0),
            'competitor_price_increase': context.get('competitor_price_increase', 0),
            'market_share': context.get('market_share', 0),
            'is_negative': lambda x: x < 0,
            'in_range': lambda x, low, high: low <= x <= high,
        })
        
        return safe_context
    
    def execute_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the rule action
        
        Args:
            context: Market data context
        
        Returns:
            Dictionary with action results
        """
        try:
            # Parse action template
            action_result = self._parse_action_template(context)
            
            result = {
                'rule_id': self.rule_id,
                'rule_name': self.name,
                'action': action_result,
                'executed_at': datetime.utcnow(),
                'success': True,
                'context_snapshot': {k: v for k, v in context.items() 
                                  if k in ['market_growth', 'sentiment_score', 'competitor_price', 'trend_demand']}
            }
            
            logger.info(f"Rule {self.rule_id} executed successfully: {action_result}")
            return result
            
        except Exception as e:
            logger.error(f"Error executing action for rule {self.rule_id}: {e}")
            return {
                'rule_id': self.rule_id,
                'rule_name': self.name,
                'error': str(e),
                'executed_at': datetime.utcnow(),
                'success': False
            }
    
    def _parse_action_template(self, context: Dict[str, Any]) -> str:
        """Parse action template with context variables"""
        action = self.action
        
        # Replace variables in action template
        for key, value in context.items():
            if isinstance(value, (int, float)):
                action = action.replace(f'{{{key}}}', str(value))
            elif isinstance(value, str):
                action = action.replace(f'{{{key}}}', value)
        
        return action
    
    def get_success_rate(self) -> float:
        """Calculate rule success rate"""
        if self.execution_count == 0:
            return 0.0
        return (self.success_count / self.execution_count) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert rule to dictionary representation"""
        return {
            'rule_id': self.rule_id,
            'name': self.name,
            'description': self.description,
            'condition': self.condition,
            'action': self.action,
            'rule_type': self.rule_type.value,
            'priority': self.priority.value,
            'status': self.status.value,
            'parameters': self.parameters,
            'execution_count': self.execution_count,
            'success_count': self.success_count,
            'success_rate': self.get_success_rate(),
            'last_executed': self.last_executed.isoformat() if self.last_executed else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class RuleEngine:
    """
    Main rule engine for managing and executing business rules
    """
    
    def __init__(self):
        self.rules: Dict[str, MarketRule] = {}
        self.rule_categories = {
            'investment': [],
            'marketing': [],
            'competitive': [],
            'trend': [],
            'risk': []
        }
        self.execution_history: List[Dict] = []
        
        # Initialize default rules
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """Initialize default market intelligence rules"""
        default_rules = [
            MarketRule(
                rule_id="high_growth_investment",
                name="High Growth Investment Alert",
                description="Trigger when market growth exceeds 30%",
                condition="market_growth > 15",
                action="Recommend investment in market segment. Growth: {market_growth}%",
                rule_type=RuleType.THRESHOLD,
                priority=RulePriority.HIGH
            ),
            
            MarketRule(
                rule_id="negative_sentiment_alert",
                name="Negative Sentiment Alert",
                description="Trigger when negative sentiment exceeds 40%",
                condition="negative_sentiment > 40",
                action="Suggest marketing improvement strategies. Negative sentiment: {negative_sentiment}%",
                rule_type=RuleType.THRESHOLD,
                priority=RulePriority.HIGH
            ),
            
            MarketRule(
                rule_id="competitor_price_response",
                name="Competitor Price Response",
                description="Trigger when competitor price increases significantly",
                condition="competitor_price_increase > 10",
                action="Consider product launch or price adjustment. Competitor price increase: {competitor_price_increase}%",
                rule_type=RuleType.THRESHOLD,
                priority=RulePriority.MEDIUM
            ),
            
            MarketRule(
                rule_id="high_demand_opportunity",
                name="High Demand Opportunity",
                description="Trigger when trend demand is high",
                condition="trend_demand > 70",
                action="Highlight market opportunity for expansion. Demand score: {trend_demand}",
                rule_type=RuleType.THRESHOLD,
                priority=RulePriority.HIGH
            ),
            
            MarketRule(
                rule_id="low_market_share_alert",
                name="Low Market Share Alert",
                description="Trigger when market share is below threshold",
                condition="market_share < 15",
                action="Analyze competitive position and strategy. Current market share: {market_share}%",
                rule_type=RuleType.THRESHOLD,
                priority=RulePriority.MEDIUM
            ),
            
            MarketRule(
                rule_id="positive_sentiment_investment",
                name="Positive Sentiment Investment",
                description="Invest when both growth and sentiment are positive",
                condition="market_growth > 15 and sentiment_score > 0.3",
                action="Strong buy recommendation. Growth: {market_growth}%, Sentiment: {sentiment_score}",
                rule_type=RuleType.COMPOSITE,
                priority=RulePriority.HIGH
            ),
            
            MarketRule(
                rule_id="volatility_risk_alert",
                name="Volatility Risk Alert",
                description="Alert on high market volatility",
                condition="market_volatility > 25",
                action="High volatility detected. Risk management advised. Volatility: {market_volatility}%",
                rule_type=RuleType.THRESHOLD,
                priority=RulePriority.CRITICAL
            ),
            
            MarketRule(
                rule_id="competitor_activity_surge",
                name="Competitor Activity Surge",
                description="Monitor competitor activity spikes",
                condition="competitor_activity_count > 5 and competitor_activity_growth > 50",
                action="Increased competitor activity detected. Competitive analysis recommended.",
                rule_type=RuleType.COMPOSITE,
                priority=RulePriority.MEDIUM
            )
        ]
        
        for rule in default_rules:
            self.add_rule(rule)
        
        logger.info(f"Initialized {len(default_rules)} default rules")
    
    def add_rule(self, rule: MarketRule) -> bool:
        """
        Add a new rule to the engine
        
        Args:
            rule: MarketRule instance to add
        
        Returns:
            True if rule added successfully, False otherwise
        """
        try:
            if rule.rule_id in self.rules:
                logger.warning(f"Rule {rule.rule_id} already exists. Updating...")
                self.rules[rule.rule_id] = rule
            else:
                self.rules[rule.rule_id] = rule
            
            # Categorize rule based on keywords
            self._categorize_rule(rule)
            
            logger.info(f"Added rule: {rule.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add rule {rule.rule_id}: {e}")
            return False
    
    def _categorize_rule(self, rule: MarketRule):
        """Categorize rule based on its content"""
        categories = {
            'investment': ['investment', 'growth', 'buy', 'sell'],
            'marketing': ['marketing', 'sentiment', 'brand'],
            'competitive': ['competitor', 'competition', 'market share'],
            'trend': ['trend', 'demand', 'opportunity'],
            'risk': ['risk', 'volatility', 'alert']
        }
        
        rule_text = f"{rule.name} {rule.description} {rule.action}".lower()
        
        for category, keywords in categories.items():
            if any(keyword in rule_text for keyword in keywords):
                if rule.rule_id not in self.rule_categories[category]:
                    self.rule_categories[category].append(rule.rule_id)
    
    def remove_rule(self, rule_id: str) -> bool:
        """
        Remove a rule from the engine
        
        Args:
            rule_id: ID of rule to remove
        
        Returns:
            True if rule removed successfully, False otherwise
        """
        try:
            if rule_id not in self.rules:
                logger.warning(f"Rule {rule_id} not found")
                return False
            
            # Remove from categories
            for category_rules in self.rule_categories.values():
                if rule_id in category_rules:
                    category_rules.remove(rule_id)
            
            # Remove from rules
            del self.rules[rule_id]
            
            logger.info(f"Removed rule: {rule_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove rule {rule_id}: {e}")
            return False
    
    def get_rule(self, rule_id: str) -> Optional[MarketRule]:
        """Get a rule by ID"""
        return self.rules.get(rule_id)
    
    def get_rules_by_category(self, category: str) -> List[MarketRule]:
        """Get all rules in a specific category"""
        rule_ids = self.rule_categories.get(category, [])
        return [self.rules[rule_id] for rule_id in rule_ids if rule_id in self.rules]
    
    def get_active_rules(self) -> List[MarketRule]:
        """Get all active rules"""
        return [rule for rule in self.rules.values() if rule.status == RuleStatus.ACTIVE]
    
    def evaluate_rules(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evaluate all active rules against provided context
        
        Args:
            context: Market data context
        
        Returns:
            List of rule execution results
        """
        results = []
        active_rules = self.get_active_rules()
        
        # Sort rules by priority
        active_rules.sort(key=lambda r: r.priority.value)
        
        for rule in active_rules:
            try:
                if rule.evaluate_condition(context):
                    result = rule.execute_action(context)
                    # Add priority to result
                    result_with_priority = {
                        'rule_id': rule.rule_id,
                        'action': result,
                        'priority': rule.priority.value,  # Add priority field
                        'priority_name': rule.priority.name  # Add priority name
                    }
                    results.append(result_with_priority)
                    
                    # Add to execution history
                    self.execution_history.append({
                        'rule_id': rule.rule_id,
                        'context': context,
                        'result': result_with_priority,
                        'timestamp': datetime.utcnow()
                    })
                    
            except Exception as e:
                logger.error(f"Error evaluating rule {rule.rule_id}: {e}")
                results.append({
                    'rule_id': rule.rule_id,
                    'error': str(e),
                    'success': False
                })
        
        logger.info(f"Evaluated {len(active_rules)} rules, {len(results)} triggered")
        return results
    
    def get_rule_statistics(self) -> Dict[str, Any]:
        """Get statistics about rule performance"""
        try:
            total_rules = len(self.rules)
            active_rules = len(self.get_active_rules())
            
            if total_rules == 0:
                return {'total_rules': 0}
            
            # Calculate execution statistics
            total_executions = sum(rule.execution_count for rule in self.rules.values())
            total_successes = sum(rule.success_count for rule in self.rules.values())
            overall_success_rate = (total_successes / total_executions * 100) if total_executions > 0 else 0
            
            # Category statistics
            category_stats = {}
            for category, rule_ids in self.rule_categories.items():
                category_rules = [self.rules[rule_id] for rule_id in rule_ids if rule_id in self.rules]
                category_stats[category] = {
                    'rule_count': len(category_rules),
                    'active_count': len([r for r in category_rules if r.status == RuleStatus.ACTIVE]),
                    'avg_success_rate': sum(r.get_success_rate() for r in category_rules) / len(category_rules) if category_rules else 0
                }
            
            # Top performing rules
            top_rules = sorted(self.rules.values(), key=lambda r: r.get_success_rate(), reverse=True)[:5]
            
            return {
                'total_rules': total_rules,
                'active_rules': active_rules,
                'total_executions': total_executions,
                'total_successes': total_successes,
                'overall_success_rate': overall_success_rate,
                'category_statistics': category_stats,
                'top_performing_rules': [r.to_dict() for r in top_rules],
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate rule statistics: {e}")
            return {'error': str(e)}
    
    def export_rules(self) -> Dict[str, Any]:
        """Export all rules to dictionary format"""
        return {
            'rules': {rule_id: rule.to_dict() for rule_id, rule in self.rules.items()},
            'categories': self.rule_categories,
            'exported_at': datetime.utcnow().isoformat()
        }
    
    def import_rules(self, rules_data: Dict[str, Any]) -> bool:
        """Import rules from dictionary format"""
        try:
            imported_count = 0
            
            for rule_id, rule_dict in rules_data.get('rules', {}).items():
                # Convert dictionaries back to enums
                rule_type = RuleType(rule_dict['rule_type'])
                priority = RulePriority(rule_dict['priority'])
                status = RuleStatus(rule_dict['status'])
                
                # Create rule object
                rule = MarketRule(
                    rule_id=rule_dict['rule_id'],
                    name=rule_dict['name'],
                    description=rule_dict['description'],
                    condition=rule_dict['condition'],
                    action=rule_dict['action'],
                    rule_type=rule_type,
                    priority=priority,
                    status=status,
                    parameters=rule_dict.get('parameters', {})
                )
                
                # Restore execution statistics
                rule.execution_count = rule_dict.get('execution_count', 0)
                rule.success_count = rule_dict.get('success_count', 0)
                
                if rule_dict.get('last_executed'):
                    rule.last_executed = datetime.fromisoformat(rule_dict['last_executed'])
                
                if rule_dict.get('created_at'):
                    rule.created_at = datetime.fromisoformat(rule_dict['created_at'])
                
                if rule_dict.get('updated_at'):
                    rule.updated_at = datetime.fromisoformat(rule_dict['updated_at'])
                
                self.add_rule(rule)
                imported_count += 1
            
            logger.info(f"Imported {imported_count} rules")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import rules: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Initialize rule engine
    engine = RuleEngine()
    
    # Test rule evaluation
    test_context = {
        'market_growth': 35,
        'sentiment_score': 0.4,
        'negative_sentiment': 25,
        'competitor_price_increase': 15,
        'trend_demand': 75,
        'market_share': 12,
        'market_volatility': 30
    }
    
    print("Testing rule evaluation...")
    results = engine.evaluate_rules(test_context)
    print(f"Triggered {len(results)} rules:")
    for result in results:
        if result.get('success'):
            print(f"- {result['rule_name']}: {result['action']}")
    
    # Test rule statistics
    print("\nRule statistics:")
    stats = engine.get_rule_statistics()
    print(f"Total rules: {stats['total_rules']}")
    print(f"Active rules: {stats['active_rules']}")
    print(f"Overall success rate: {stats['overall_success_rate']:.1f}%")
    
    # Test custom rule
    custom_rule = MarketRule(
        rule_id="test_rule",
        name="Test Rule",
        description="A test rule for demonstration",
        condition="market_growth > 50",
        action="High growth alert! Growth: {market_growth}%",
        priority=RulePriority.CRITICAL
    )
    
    engine.add_rule(custom_rule)
    print(f"\nAdded custom rule: {custom_rule.name}")
    
    # Test with high growth context
    high_growth_context = test_context.copy()
    high_growth_context['market_growth'] = 55
    
    results = engine.evaluate_rules(high_growth_context)
    print(f"High growth context triggered {len(results)} rules")

"""
API Routes for Adaptive Neuro-Symbolic Market Intelligence System
This module contains all API route definitions
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from .database import get_db
from .models import (
    MarketData, MarketDataCreate, MarketDataResponse,
    CompetitorData, CompetitorDataCreate, CompetitorDataResponse,
    Recommendation, RecommendationCreate, RecommendationResponse,
    TrendAnalysis, TrendAnalysisCreate, TrendAnalysisResponse
)

# Configure logging
logger = logging.getLogger(__name__)

# Import system components
try:
    from ..data_collection.api_fetch import DataCollectionManager
    from ..data_collection.scraper import MarketScraper, CompetitorMonitor
    from ..ai_engine.sentiment import SentimentAnalyzer, MarketSentimentAnalyzer
    from ..ai_engine.trend_analysis import MarketTrendAnalyzer
    from ..symbolic_engine.rules import RuleEngine, MarketRule
    from ..symbolic_engine.decision_engine import DecisionEngine
    from ..adaptive_module.learning import AdaptiveLearningEngine, LearningType
except ImportError:
    # Handle relative imports for development
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from data_collection.api_fetch import DataCollectionManager
    from data_collection.scraper import MarketScraper, CompetitorMonitor
    from ai_engine.sentiment import SentimentAnalyzer, MarketSentimentAnalyzer
    from ai_engine.trend_analysis import MarketTrendAnalyzer
    from symbolic_engine.rules import RuleEngine, MarketRule
    from symbolic_engine.decision_engine import DecisionEngine
    from adaptive_module.learning import AdaptiveLearningEngine, LearningType

# Initialize system components
data_manager = DataCollectionManager()
scraper = MarketScraper()
competitor_monitor = CompetitorMonitor()
sentiment_analyzer = SentimentAnalyzer()
market_sentiment_analyzer = MarketSentimentAnalyzer()
trend_analyzer = MarketTrendAnalyzer()
rule_engine = RuleEngine()
decision_engine = DecisionEngine()
learning_engine = AdaptiveLearningEngine()

# Market Data Routes
market_data_router = APIRouter()

@market_data_router.get("/", response_model=List[MarketDataResponse])
async def get_market_data(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get market data with pagination and filtering"""
    try:
        query = db.query(MarketData)
        
        if category:
            query = query.filter(MarketData.category == category)
        
        market_data = query.offset(skip).limit(limit).all()
        return market_data
    except Exception as e:
        logger.error(f"Error getting market data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve market data")

@market_data_router.post("/", response_model=MarketDataResponse)
async def create_market_data(
    market_data: MarketDataCreate,
    db: Session = Depends(get_db)
):
    """Create new market data entry"""
    try:
        db_market_data = MarketData(**market_data.dict())
        db.add(db_market_data)
        db.commit()
        db.refresh(db_market_data)
        return db_market_data
    except Exception as e:
        logger.error(f"Error creating market data: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create market data")

@market_data_router.post("/collect")
async def collect_market_data(
    background_tasks: BackgroundTasks,
    source: str = Query("reuters"),
    max_articles: int = Query(10, ge=1, le=50)
):
    """Collect market data from external sources"""
    try:
        def collect_task():
            articles = scraper.scrape_news_headlines(source, max_articles)
            logger.info(f"Collected {len(articles)} articles from {source}")
        
        background_tasks.add_task(collect_task)
        
        return {
            "message": f"Data collection started from {source}",
            "max_articles": max_articles,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error starting data collection: {e}")
        raise HTTPException(status_code=500, detail="Failed to start data collection")

# Competitor Intelligence Routes
competitor_router = APIRouter()

@competitor_router.get("/", response_model=List[CompetitorDataResponse])
async def get_competitor_data(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    competitor_name: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get competitor intelligence data"""
    try:
        query = db.query(CompetitorData)
        
        if competitor_name:
            query = query.filter(CompetitorData.competitor_name == competitor_name)
        
        competitor_data = query.offset(skip).limit(limit).all()
        return competitor_data
    except Exception as e:
        logger.error(f"Error getting competitor data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve competitor data")

@competitor_router.post("/", response_model=CompetitorDataResponse)
async def create_competitor_data(
    competitor_data: CompetitorDataCreate,
    db: Session = Depends(get_db)
):
    """Create new competitor data entry"""
    try:
        db_competitor_data = CompetitorData(**competitor_data.dict())
        db.add(db_competitor_data)
        db.commit()
        db.refresh(db_competitor_data)
        return db_competitor_data
    except Exception as e:
        logger.error(f"Error creating competitor data: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create competitor data")

@competitor_router.post("/monitor")
async def monitor_competitors(background_tasks: BackgroundTasks):
    """Monitor all configured competitors"""
    try:
        def monitor_task():
            competitor_data = competitor_monitor.monitor_all_competitors()
            logger.info(f"Monitored {len(competitor_data)} competitors")
        
        background_tasks.add_task(monitor_task)
        
        return {
            "message": "Competitor monitoring started",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error starting competitor monitoring: {e}")
        raise HTTPException(status_code=500, detail="Failed to start competitor monitoring")

# Recommendation Routes
recommendation_router = APIRouter()

@recommendation_router.get("/", response_model=List[RecommendationResponse])
async def get_recommendations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get recommendations with filtering"""
    try:
        query = db.query(Recommendation)
        
        if status:
            query = query.filter(Recommendation.status == status)
        
        if priority:
            query = query.filter(Recommendation.priority == priority)
        
        recommendations = query.offset(skip).limit(limit).all()
        return recommendations
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recommendations")

@recommendation_router.post("/", response_model=RecommendationResponse)
async def create_recommendation(
    recommendation: RecommendationCreate,
    db: Session = Depends(get_db)
):
    """Create new recommendation"""
    try:
        db_recommendation = Recommendation(**recommendation.dict())
        db.add(db_recommendation)
        db.commit()
        db.refresh(db_recommendation)
        return db_recommendation
    except Exception as e:
        logger.error(f"Error creating recommendation: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create recommendation")

@recommendation_router.put("/{recommendation_id}/status")
async def update_recommendation_status(
    recommendation_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update recommendation status"""
    try:
        recommendation = db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if not recommendation:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        
        recommendation.status = status
        if status == "implemented":
            recommendation.implemented_date = datetime.utcnow()
        
        db.commit()
        return {"message": "Recommendation status updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating recommendation status: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update recommendation status")

# Trend Analysis Routes
trend_router = APIRouter()

@trend_router.get("/", response_model=List[TrendAnalysisResponse])
async def get_trend_analysis(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get trend analysis data"""
    try:
        query = db.query(TrendAnalysis)
        
        if keyword:
            query = query.filter(TrendAnalysis.keyword == keyword)
        
        trend_data = query.offset(skip).limit(limit).all()
        return trend_data
    except Exception as e:
        logger.error(f"Error getting trend analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve trend analysis")

@trend_router.post("/", response_model=TrendAnalysisResponse)
async def create_trend_analysis(
    trend_data: TrendAnalysisCreate,
    db: Session = Depends(get_db)
):
    """Create new trend analysis entry"""
    try:
        db_trend_data = TrendAnalysis(**trend_data.dict())
        db.add(db_trend_data)
        db.commit()
        db.refresh(db_trend_data)
        return db_trend_data
    except Exception as e:
        logger.error(f"Error creating trend analysis: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create trend analysis")

@trend_router.post("/analyze")
async def analyze_trends(keywords: List[str]):
    """Analyze trends for specified keywords"""
    try:
        trend_data = data_manager.collect_trends_only(keywords)
        
        # Process with AI engine
        analysis_results = trend_analyzer.analyze_keyword_trends(trend_data)
        
        return {
            "keywords": keywords,
            "analysis": analysis_results,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing trends: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze trends")

# AI Analysis Routes
analysis_router = APIRouter()

@analysis_router.post("/sentiment")
async def analyze_sentiment(text: str):
    """Analyze sentiment of text"""
    try:
        sentiment_result = sentiment_analyzer.analyze_sentiment_ensemble(text)
        
        return {
            "text": text,
            "sentiment": sentiment_result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze sentiment")

@analysis_router.post("/sentiment/batch")
async def analyze_sentiment_batch(texts: List[str]):
    """Analyze sentiment for multiple texts"""
    try:
        sentiment_results = sentiment_analyzer.batch_analyze_sentiment(texts)
        summary = sentiment_analyzer.get_sentiment_summary(sentiment_results)
        
        return {
            "texts_count": len(texts),
            "results": sentiment_results,
            "summary": summary,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing batch sentiment: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze batch sentiment")

@analysis_router.post("/news-sentiment")
async def analyze_news_sentiment(background_tasks: BackgroundTasks):
    """Analyze sentiment for recent news"""
    try:
        def analyze_news_task():
            news_data = data_manager.collect_news_only()
            analyzed_news = market_sentiment_analyzer.analyze_news_sentiment(news_data)
            logger.info(f"Analyzed sentiment for {len(analyzed_news)} news articles")
        
        background_tasks.add_task(analyze_news_task)
        
        return {
            "message": "News sentiment analysis started",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error starting news sentiment analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to start news sentiment analysis")

# Business Rules Routes
rule_router = APIRouter()

@rule_router.get("/")
async def get_rules():
    """Get all business rules"""
    try:
        rules = [rule.to_dict() for rule in rule_engine.rules.values()]
        
        return {
            "rules": rules,
            "total_count": len(rules),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting rules: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve rules")

@rule_router.get("/{rule_id}")
async def get_rule(rule_id: str):
    """Get specific rule by ID"""
    try:
        rule = rule_engine.get_rule(rule_id)
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        
        return rule.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting rule: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve rule")

@rule_router.post("/evaluate")
async def evaluate_rules(context: Dict[str, Any]):
    """Evaluate rules against provided context"""
    try:
        results = rule_engine.evaluate_rules(context)
        
        return {
            "context": context,
            "results": results,
            "triggered_count": len(results),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error evaluating rules: {e}")
        raise HTTPException(status_code=500, detail="Failed to evaluate rules")

@rule_router.get("/statistics")
async def get_rule_statistics():
    """Get rule execution statistics"""
    try:
        stats = rule_engine.get_rule_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error getting rule statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve rule statistics")

# Decision Engine Routes
decision_router = APIRouter()

@decision_router.post("/make")
async def make_decisions(
    context: Dict[str, Any],
    ai_insights: Optional[Dict[str, Any]] = None
):
    """Make market intelligence decisions"""
    try:
        decisions = decision_engine.make_decision(context, ai_insights)
        
        return {
            "context": context,
            "ai_insights": ai_insights,
            "decisions": [decision.to_dict() for decision in decisions],
            "decision_count": len(decisions),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error making decisions: {e}")
        raise HTTPException(status_code=500, detail="Failed to make decisions")

@decision_router.get("/history")
async def get_decision_history(
    hours: int = Query(24, ge=1, le=168)  # Last 1 hour to 1 week
):
    """Get decision history"""
    try:
        summary = decision_engine.get_decision_summary(hours)
        return summary
    except Exception as e:
        logger.error(f"Error getting decision history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve decision history")

@decision_router.get("/export")
async def export_decisions(limit: int = Query(100, ge=1, le=1000)):
    """Export decision history"""
    try:
        export_data = decision_engine.export_decisions(limit)
        return export_data
    except Exception as e:
        logger.error(f"Error exporting decisions: {e}")
        raise HTTPException(status_code=500, detail="Failed to export decisions")

# Adaptive Learning Routes
learning_router = APIRouter()

@learning_router.post("/train/{learning_type}")
async def train_model(
    learning_type: str,
    training_data: List[Dict[str, Any]]
):
    """Train adaptive learning model"""
    try:
        # Convert string to enum
        learning_type_enum = LearningType(learning_type)
        
        result = learning_engine.learn_from_data(learning_type_enum, training_data)
        
        if result:
            return result.to_dict()
        else:
            raise HTTPException(status_code=400, detail="Training failed")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid learning type")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error training model: {e}")
        raise HTTPException(status_code=500, detail="Failed to train model")

@learning_router.post("/predict/{learning_type}")
async def make_prediction(
    learning_type: str,
    input_data: Dict[str, Any]
):
    """Make prediction using trained model"""
    try:
        learning_type_enum = LearningType(learning_type)
        
        prediction = learning_engine.predict(learning_type_enum, input_data)
        
        if prediction:
            return prediction
        else:
            raise HTTPException(status_code=400, detail="Prediction failed")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid learning type")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        raise HTTPException(status_code=500, detail="Failed to make prediction")

@learning_router.post("/optimize-rules")
async def optimize_rules(rule_execution_history: List[Dict[str, Any]]):
    """Optimize rule parameters"""
    try:
        optimizations = learning_engine.optimize_rules(rule_execution_history)
        
        return {
            "optimizations": optimizations,
            "optimization_count": len(optimizations),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error optimizing rules: {e}")
        raise HTTPException(status_code=500, detail="Failed to optimize rules")

@learning_router.post("/detect-anomalies")
async def detect_anomalies(data: List[Dict[str, Any]]):
    """Detect anomalies in data"""
    try:
        anomalies = learning_engine.detect_anomalies(data)
        
        return {
            "anomalies": anomalies,
            "anomaly_count": len(anomalies),
            "data_points": len(data),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error detecting anomalies: {e}")
        raise HTTPException(status_code=500, detail="Failed to detect anomalies")

@learning_router.get("/summary")
async def get_learning_summary():
    """Get learning summary"""
    try:
        summary = learning_engine.get_learning_summary()
        return summary
    except Exception as e:
        logger.error(f"Error getting learning summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve learning summary")

@learning_router.get("/history")
async def get_learning_history(limit: int = Query(100, ge=1, le=1000)):
    """Get learning history"""
    try:
        history = learning_engine.export_learning_history(limit)
        return history
    except Exception as e:
        logger.error(f"Error getting learning history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve learning history")

"""
FastAPI Main Application for Adaptive Neuro-Symbolic Market Intelligence System
This is the main entry point for the REST API backend
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import asyncio
from contextlib import asynccontextmanager

# Import modules
from .database import get_db, init_database, test_connection
from .models import (
    MarketDataResponse, CompetitorDataResponse, 
    RecommendationResponse, TrendAnalysisResponse
)
from .routes import (
    market_data_router, competitor_router, 
    recommendation_router, trend_router, analysis_router,
    rule_router, decision_router, learning_router
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Adaptive Market Intelligence System...")
    
    # Test database connection
    if not test_connection():
        logger.error("Failed to connect to database")
        raise Exception("Database connection failed")
    
    # Initialize database
    init_database()
    logger.info("Database initialized successfully")
    
    # Initialize background tasks
    app.state.background_tasks = []
    
    yield
    
    # Shutdown
    logger.info("Shutting down Adaptive Market Intelligence System...")

# Create FastAPI application
app = FastAPI(
    title="Adaptive Neuro-Symbolic Market Intelligence System",
    description="An intelligent market analysis system combining AI and symbolic reasoning",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(market_data_router, prefix="/api/v1/market", tags=["Market Data"])
app.include_router(competitor_router, prefix="/api/v1/competitor", tags=["Competitor Intelligence"])
app.include_router(recommendation_router, prefix="/api/v1/recommendations", tags=["Recommendations"])
app.include_router(trend_router, prefix="/api/v1/trends", tags=["Trend Analysis"])
app.include_router(analysis_router, prefix="/api/v1/analysis", tags=["AI Analysis"])
app.include_router(rule_router, prefix="/api/v1/rules", tags=["Business Rules"])
app.include_router(decision_router, prefix="/api/v1/decisions", tags=["Decision Engine"])
app.include_router(learning_router, prefix="/api/v1/learning", tags=["Adaptive Learning"])

# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_status = test_connection()
        
        return {
            "status": "healthy" if db_status else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected" if db_status else "disconnected",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """Root endpoint with system information"""
    return {
        "message": "Adaptive Neuro-Symbolic Market Intelligence System",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "health": "/health",
            "market_data": "/api/v1/market",
            "competitor": "/api/v1/competitor",
            "recommendations": "/api/v1/recommendations",
            "trends": "/api/v1/trends",
            "analysis": "/api/v1/analysis",
            "rules": "/api/v1/rules",
            "decisions": "/api/v1/decisions",
            "learning": "/api/v1/learning",
            "docs": "/docs"
        }
    }

# System status endpoint
@app.get("/api/v1/status", tags=["System"])
async def system_status():
    """Get detailed system status"""
    try:
        from ..data_collection.api_fetch import DataCollectionManager
        from ..ai_engine.sentiment import SentimentAnalyzer
        from ..symbolic_engine.decision_engine import DecisionEngine
        from ..adaptive_module.learning import AdaptiveLearningEngine
        
        # Initialize components
        data_manager = DataCollectionManager()
        sentiment_analyzer = SentimentAnalyzer()
        decision_engine = DecisionEngine()
        learning_engine = AdaptiveLearningEngine()
        
        # Get component status
        status = {
            "system": {
                "status": "running",
                "uptime": "N/A",  # Could be calculated from start time
                "timestamp": datetime.utcnow().isoformat()
            },
            "database": {
                "status": "connected" if test_connection() else "disconnected"
            },
            "components": {
                "data_collection": "initialized",
                "sentiment_analysis": "initialized",
                "trend_analysis": "initialized",
                "rule_engine": "initialized",
                "decision_engine": "initialized",
                "adaptive_learning": "initialized"
            },
            "statistics": {
                "rules_loaded": len(decision_engine.rule_engine.rules),
                "learning_sessions": len(learning_engine.learning_history),
                "recent_decisions": len(decision_engine.decision_history)
            }
        }
        
        return status
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system status")

# Background task for data collection
@app.post("/api/v1/collect-data", tags=["Data Collection"])
async def trigger_data_collection(background_tasks: BackgroundTasks):
    """Trigger background data collection"""
    try:
        def collect_data_task():
            """Background task for data collection"""
            try:
                from ..data_collection.api_fetch import DataCollectionManager
                from ..ai_engine.sentiment import MarketSentimentAnalyzer
                from ..backend.database import get_db
                
                logger.info("Starting background data collection...")
                
                # Initialize components
                data_manager = DataCollectionManager()
                sentiment_analyzer = MarketSentimentAnalyzer()
                
                # Collect data
                collected_data = data_manager.collect_all_data(['market', 'technology', 'finance'])
                
                # Analyze sentiment
                if collected_data['news_data']:
                    analyzed_news = sentiment_analyzer.analyze_news_sentiment(collected_data['news_data'])
                    logger.info(f"Analyzed sentiment for {len(analyzed_news)} news articles")
                
                # Store in database (implementation needed)
                logger.info("Data collection completed successfully")
                
            except Exception as e:
                logger.error(f"Background data collection failed: {e}")
        
        # Add background task
        background_tasks.add_task(collect_data_task)
        
        return {
            "message": "Data collection started",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "processing"
        }
        
    except Exception as e:
        logger.error(f"Failed to start data collection: {e}")
        raise HTTPException(status_code=500, detail="Failed to start data collection")

# Comprehensive analysis endpoint
@app.post("/api/v1/comprehensive-analysis", tags=["Analysis"])
async def comprehensive_analysis(background_tasks: BackgroundTasks):
    """Trigger comprehensive market analysis"""
    try:
        def analysis_task():
            """Background task for comprehensive analysis"""
            try:
                from ..data_collection.api_fetch import DataCollectionManager
                from ..ai_engine.sentiment import MarketSentimentAnalyzer
                from ..ai_engine.trend_analysis import MarketTrendAnalyzer
                from ..symbolic_engine.decision_engine import DecisionEngine
                from ..backend.database import get_db
                
                logger.info("Starting comprehensive analysis...")
                
                # Initialize components
                data_manager = DataCollectionManager()
                sentiment_analyzer = MarketSentimentAnalyzer()
                trend_analyzer = MarketTrendAnalyzer()
                decision_engine = DecisionEngine()
                
                # Collect data
                collected_data = data_manager.collect_all_data(['market', 'technology', 'finance'])
                
                # Analyze sentiment
                sentiment_results = {}
                if collected_data['news_data']:
                    analyzed_news = sentiment_analyzer.analyze_news_sentiment(collected_data['news_data'])
                    sentiment_results['news'] = sentiment_analyzer.sentiment_analyzer.get_sentiment_summary(
                        [news.get('sentiment', {}) for news in analyzed_news]
                    )
                
                if collected_data['social_data']:
                    analyzed_social = sentiment_analyzer.analyze_social_sentiment(collected_data['social_data'])
                    sentiment_results['social'] = sentiment_analyzer.sentiment_analyzer.get_sentiment_summary(
                        [post.get('sentiment', {}) for post in analyzed_social]
                    )
                
                # Analyze trends
                trend_results = {}
                if collected_data['trend_data']:
                    trend_results = trend_analyzer.analyze_keyword_trends(collected_data['trend_data'])
                
                # Create context for decision making
                context = {
                    'market_growth': 25,  # Would be calculated from actual data
                    'sentiment_score': sentiment_results.get('news', {}).get('average_sentiment', 0),
                    'negative_sentiment': sentiment_results.get('news', {}).get('negative_percentage', 0),
                    'trend_demand': 70,  # Would be calculated from trend data
                    'market_volatility': 20
                }
                
                # Make decisions
                decisions = decision_engine.make_decision(context, {
                    'sentiment_analysis': sentiment_results,
                    'trend_analysis': trend_results
                })
                
                logger.info(f"Comprehensive analysis completed. Generated {len(decisions)} decisions")
                
            except Exception as e:
                logger.error(f"Comprehensive analysis failed: {e}")
        
        # Add background task
        background_tasks.add_task(analysis_task)
        
        return {
            "message": "Comprehensive analysis started",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "processing"
        }
        
    except Exception as e:
        logger.error(f"Failed to start comprehensive analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to start comprehensive analysis")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": str(exc)}
    )

# Custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

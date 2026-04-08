"""
Database Models for Adaptive Neuro-Symbolic Market Intelligence System
This file contains SQLAlchemy ORM models for all database tables
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, DECIMAL, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class MarketData(Base):
    """Model for storing market news and data"""
    __tablename__ = 'market_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(100), nullable=False)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String(500))
    published_date = Column(DateTime)
    collected_date = Column(DateTime, default=datetime.utcnow)
    category = Column(String(50))
    sentiment_score = Column(Float)
    keywords = Column(JSON)
    
    def __repr__(self):
        return f"<MarketData(id={self.id}, title='{self.title[:50]}...', source='{self.source}')>"

class CompetitorData(Base):
    """Model for storing competitor intelligence"""
    __tablename__ = 'competitor_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    competitor_name = Column(String(100), nullable=False)
    product_name = Column(String(100))
    price = Column(DECIMAL(10, 2))
    market_share = Column(Float)
    activity_type = Column(String(50))
    description = Column(Text)
    recorded_date = Column(DateTime, default=datetime.utcnow)
    source = Column(String(100))
    
    def __repr__(self):
        return f"<CompetitorData(id={self.id}, competitor='{self.competitor_name}', activity='{self.activity_type}')>"

class TrendAnalysis(Base):
    """Model for storing trend analysis results"""
    __tablename__ = 'trend_analysis'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(100), nullable=False)
    trend_score = Column(Float)
    volume = Column(Integer)
    growth_rate = Column(Float)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    source = Column(String(50))
    
    def __repr__(self):
        return f"<TrendAnalysis(id={self.id}, keyword='{self.keyword}', score={self.trend_score})>"

class MarketPrediction(Base):
    """Model for storing market predictions"""
    __tablename__ = 'market_predictions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    prediction_type = Column(String(50), nullable=False)
    prediction_value = Column(Float)
    confidence_score = Column(Float)
    factors = Column(JSON)
    created_date = Column(DateTime, default=datetime.utcnow)
    actual_value = Column(Float)
    accuracy_score = Column(Float)
    
    def __repr__(self):
        return f"<MarketPrediction(id={self.id}, type='{self.prediction_type}', value={self.prediction_value})>"

class Rule(Base):
    """Model for storing business rules"""
    __tablename__ = 'rules'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_name = Column(String(100), nullable=False)
    condition_expression = Column(Text, nullable=False)
    action = Column(Text, nullable=False)
    priority = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with rule executions
    executions = relationship("RuleExecution", back_populates="rule")
    
    def __repr__(self):
        return f"<Rule(id={self.id}, name='{self.rule_name}', active={self.is_active})>"

class RuleExecution(Base):
    """Model for tracking rule execution history"""
    __tablename__ = 'rule_executions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_id = Column(Integer, ForeignKey('rules.id'))
    execution_date = Column(DateTime, default=datetime.utcnow)
    input_data = Column(JSON)
    result = Column(Text)
    success = Column(Boolean)
    
    # Relationship with rule
    rule = relationship("Rule", back_populates="executions")
    
    def __repr__(self):
        return f"<RuleExecution(id={self.id}, rule_id={self.rule_id}, success={self.success})>"

class Recommendation(Base):
    """Model for storing system recommendations"""
    __tablename__ = 'recommendations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    recommendation_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(String(20), default='medium')
    confidence_score = Column(Float)
    generated_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='pending')
    implemented_date = Column(DateTime)
    impact_score = Column(Float)
    
    def __repr__(self):
        return f"<Recommendation(id={self.id}, type='{self.recommendation_type}', status='{self.status}')>"

class LearningHistory(Base):
    """Model for tracking system learning and improvements"""
    __tablename__ = 'learning_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    learning_type = Column(String(50), nullable=False)
    old_value = Column(JSON)
    new_value = Column(JSON)
    improvement_score = Column(Float)
    learning_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)
    
    def __repr__(self):
        return f"<LearningHistory(id={self.id}, type='{self.learning_type}', score={self.improvement_score})>"

class SystemConfig(Base):
    """Model for storing system configuration"""
    __tablename__ = 'system_config'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(String(100), unique=True, nullable=False)
    config_value = Column(Text)
    description = Column(Text)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SystemConfig(id={self.id}, key='{self.config_key}')>"

# Pydantic models for API serialization
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class MarketDataBase(BaseModel):
    source: str
    title: str
    content: str
    url: Optional[str] = None
    published_date: Optional[datetime] = None
    category: Optional[str] = None
    sentiment_score: Optional[float] = None
    keywords: Optional[Dict[str, Any]] = None

class MarketDataCreate(MarketDataBase):
    pass

class MarketDataResponse(MarketDataBase):
    id: int
    collected_date: datetime
    
    class Config:
        from_attributes = True

class CompetitorDataBase(BaseModel):
    competitor_name: str
    product_name: Optional[str] = None
    price: Optional[float] = None
    market_share: Optional[float] = None
    activity_type: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None

class CompetitorDataCreate(CompetitorDataBase):
    pass

class CompetitorDataResponse(CompetitorDataBase):
    id: int
    recorded_date: datetime
    
    class Config:
        from_attributes = True

class RecommendationBase(BaseModel):
    recommendation_type: str
    title: str
    description: Optional[str] = None
    priority: str = 'medium'
    confidence_score: Optional[float] = None

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationResponse(RecommendationBase):
    id: int
    generated_date: datetime
    status: str
    implemented_date: Optional[datetime] = None
    impact_score: Optional[float] = None
    
    class Config:
        from_attributes = True

class TrendAnalysisBase(BaseModel):
    keyword: str
    trend_score: Optional[float] = None
    volume: Optional[int] = None
    growth_rate: Optional[float] = None
    source: Optional[str] = None

class TrendAnalysisCreate(TrendAnalysisBase):
    pass

class TrendAnalysisResponse(TrendAnalysisBase):
    id: int
    analysis_date: datetime
    
    class Config:
        from_attributes = True

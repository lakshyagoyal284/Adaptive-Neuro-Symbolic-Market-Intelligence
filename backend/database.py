"""
Database Connection and Configuration Module
This file handles database connections, session management, and configuration
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv
import logging
from typing import Generator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
# For local development with XAMPP MySQL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+mysqlconnector://root:@localhost/market_intelligence"
)

# Alternative: Use SQLite for development/testing
# DATABASE_URL = "sqlite:///./market_intelligence.db"

# Create database engine
try:
    if DATABASE_URL.startswith("sqlite"):
        # SQLite configuration
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=True  # Set to False in production
        )
    else:
        # MySQL configuration
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=True  # Set to False in production
        )
    
    logger.info("Database engine created successfully")
    
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db() -> Generator[Session, None, None]:
    """
    Database dependency for FastAPI
    Provides a database session for each request
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def init_database():
    """
    Initialize database by creating all tables
    Call this function when starting the application
    """
    try:
        from .models import Base
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Initialize default data if needed
        init_default_data()
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def init_default_data():
    """
    Initialize default configuration and rules
    """
    try:
        from .models import SystemConfig, Rule
        
        db = SessionLocal()
        
        # Check if default config exists
        existing_config = db.query(SystemConfig).first()
        if not existing_config:
            # Insert default configuration
            default_configs = [
                SystemConfig(
                    config_key="sentiment_threshold",
                    config_value="0.3",
                    description="Threshold for positive sentiment"
                ),
                SystemConfig(
                    config_key="growth_threshold",
                    config_value="30",
                    description="Percentage threshold for market growth"
                ),
                SystemConfig(
                    config_key="negative_sentiment_threshold",
                    config_value="40",
                    description="Threshold for negative sentiment alerts"
                ),
                SystemConfig(
                    config_key="data_collection_interval",
                    config_value="60",
                    description="Data collection interval in minutes"
                ),
                SystemConfig(
                    config_key="model_retrain_interval",
                    config_value="24",
                    description="Model retraining interval in hours"
                )
            ]
            
            db.add_all(default_configs)
            logger.info("Default system configuration inserted")
        
        # Check if default rules exist
        existing_rules = db.query(Rule).first()
        if not existing_rules:
            # Insert default rules
            default_rules = [
                Rule(
                    rule_name="High Growth Investment",
                    condition_expression="market_growth > 30",
                    action="Recommend investment in market segment",
                    priority=1
                ),
                Rule(
                    rule_name="Negative Sentiment Alert",
                    condition_expression="negative_sentiment > 40",
                    action="Suggest marketing improvement strategies",
                    priority=2
                ),
                Rule(
                    rule_name="Competitor Price Response",
                    condition_expression="competitor_price_increase > 10",
                    action="Consider product launch or price adjustment",
                    priority=2
                ),
                Rule(
                    rule_name="High Demand Opportunity",
                    condition_expression="trend_demand > 70",
                    action="Highlight market opportunity for expansion",
                    priority=1
                ),
                Rule(
                    rule_name="Low Market Share Alert",
                    condition_expression="market_share < 15",
                    action="Analyze competitive position and strategy",
                    priority=3
                )
            ]
            
            db.add_all(default_rules)
            logger.info("Default business rules inserted")
        
        db.commit()
        db.close()
        
    except Exception as e:
        logger.error(f"Failed to initialize default data: {e}")
        db.rollback()
        raise

class DatabaseManager:
    """
    Database utility class for common operations
    """
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    def execute_raw_query(self, query: str, params: dict = None):
        """Execute raw SQL query"""
        session = self.get_session()
        try:
            result = session.execute(query, params or {})
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            logger.error(f"Raw query execution failed: {e}")
            raise
        finally:
            session.close()
    
    def backup_database(self, backup_path: str):
        """Create database backup (MySQL only)"""
        if DATABASE_URL.startswith("mysql"):
            try:
                import subprocess
                
                # Extract connection details from DATABASE_URL
                # Format: mysql+mysqlconnector://user:password@host/database
                import re
                match = re.match(r'mysql\+mysqlconnector://([^:]+):?([^@]*)@([^/]+)/(.+)', DATABASE_URL)
                if match:
                    user, password, host, database = match.groups()
                    
                    # Create backup command
                    cmd = f'mysqldump -u {user} -p{password} -h {host} {database} > {backup_path}'
                    
                    # Execute backup
                    subprocess.run(cmd, shell=True, check=True)
                    logger.info(f"Database backup created at {backup_path}")
                    return True
                else:
                    logger.error("Invalid DATABASE_URL format for backup")
                    return False
                    
            except Exception as e:
                logger.error(f"Database backup failed: {e}")
                return False
        else:
            logger.warning("Backup only supported for MySQL databases")
            return False
    
    def get_database_stats(self):
        """Get database statistics"""
        session = self.get_session()
        try:
            from .models import MarketData, CompetitorData, TrendAnalysis, Recommendations
            
            stats = {
                "market_data_count": session.query(MarketData).count(),
                "competitor_data_count": session.query(CompetitorData).count(),
                "trend_analysis_count": session.query(TrendAnalysis).count(),
                "recommendations_count": session.query(Recommendations).count(),
                "database_size": self._get_database_size()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {}
        finally:
            session.close()
    
    def _get_database_size(self):
        """Get database size in MB"""
        try:
            if DATABASE_URL.startswith("mysql"):
                session = self.get_session()
                result = session.execute("SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'DB Size in MB' FROM information_schema.tables WHERE table_schema = 'market_intelligence'")
                size = result.fetchone()[0]
                session.close()
                return float(size) if size else 0
            else:
                return 0
        except:
            return 0

# Create global database manager instance
db_manager = DatabaseManager()

# Test database connection
def test_connection():
    """Test database connection"""
    try:
        session = SessionLocal()
        session.execute("SELECT 1")
        session.close()
        logger.info("Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

if __name__ == "__main__":
    # Test database connection and initialization
    if test_connection():
        init_database()
        print("Database initialized successfully")
    else:
        print("Database connection failed")

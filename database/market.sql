-- Adaptive Neuro-Symbolic Market Intelligence System Database Schema

-- Create database
CREATE DATABASE IF NOT EXISTS market_intelligence;
USE market_intelligence;

-- Market Data Table
CREATE TABLE market_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    url VARCHAR(500),
    published_date DATETIME,
    collected_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    category VARCHAR(50),
    sentiment_score FLOAT,
    keywords JSON,
    INDEX idx_published_date (published_date),
    INDEX idx_category (category),
    INDEX idx_sentiment (sentiment_score)
);

-- Competitor Data Table
CREATE TABLE competitor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    competitor_name VARCHAR(100) NOT NULL,
    product_name VARCHAR(100),
    price DECIMAL(10,2),
    market_share FLOAT,
    activity_type VARCHAR(50),
    description TEXT,
    recorded_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100),
    INDEX idx_competitor (competitor_name),
    INDEX idx_recorded_date (recorded_date)
);

-- Trend Analysis Table
CREATE TABLE trend_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(100) NOT NULL,
    trend_score FLOAT,
    volume INT,
    growth_rate FLOAT,
    analysis_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(50),
    INDEX idx_keyword (keyword),
    INDEX idx_analysis_date (analysis_date)
);

-- Market Predictions Table
CREATE TABLE market_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prediction_type VARCHAR(50) NOT NULL,
    prediction_value FLOAT,
    confidence_score FLOAT,
    factors JSON,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    actual_value FLOAT,
    accuracy_score FLOAT,
    INDEX idx_prediction_type (prediction_type),
    INDEX idx_created_date (created_date)
);

-- Rules Table
CREATE TABLE rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rule_name VARCHAR(100) NOT NULL,
    condition_expression TEXT NOT NULL,
    action TEXT NOT NULL,
    priority INT DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_rule_name (rule_name),
    INDEX idx_priority (priority)
);

-- Rule Executions Table
CREATE TABLE rule_executions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rule_id INT,
    execution_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    input_data JSON,
    result TEXT,
    success BOOLEAN,
    FOREIGN KEY (rule_id) REFERENCES rules(id),
    INDEX idx_rule_id (rule_id),
    INDEX idx_execution_date (execution_date)
);

-- Recommendations Table
CREATE TABLE recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recommendation_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium',
    confidence_score FLOAT,
    generated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    implemented_date DATETIME,
    impact_score FLOAT,
    INDEX idx_type (recommendation_type),
    INDEX idx_status (status),
    INDEX idx_generated_date (generated_date)
);

-- Learning History Table
CREATE TABLE learning_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    learning_type VARCHAR(50) NOT NULL,
    old_value JSON,
    new_value JSON,
    improvement_score FLOAT,
    learning_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    INDEX idx_learning_type (learning_type),
    INDEX idx_learning_date (learning_date)
);

-- System Configuration Table
CREATE TABLE system_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    description TEXT,
    updated_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_config_key (config_key)
);

-- Insert default configuration
INSERT INTO system_config (config_key, config_value, description) VALUES
('sentiment_threshold', '0.3', 'Threshold for positive sentiment'),
('growth_threshold', '30', 'Percentage threshold for market growth'),
('negative_sentiment_threshold', '40', 'Threshold for negative sentiment alerts'),
('data_collection_interval', '60', 'Data collection interval in minutes'),
('model_retrain_interval', '24', 'Model retraining interval in hours');

-- Insert default rules
INSERT INTO rules (rule_name, condition_expression, action, priority) VALUES
('High Growth Investment', 'market_growth > 30', 'Recommend investment in market segment', 1),
('Negative Sentiment Alert', 'negative_sentiment > 40', 'Suggest marketing improvement strategies', 2),
('Competitor Price Response', 'competitor_price_increase > 10', 'Consider product launch or price adjustment', 2),
('High Demand Opportunity', 'trend_demand > 70', 'Highlight market opportunity for expansion', 1),
('Low Market Share Alert', 'market_share < 15', 'Analyze competitive position and strategy', 3);

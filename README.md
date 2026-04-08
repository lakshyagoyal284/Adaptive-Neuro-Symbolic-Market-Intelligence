# Adaptive Neuro-Symbolic Market Intelligence System

An intelligent market analysis system that combines neural AI capabilities with symbolic reasoning to provide comprehensive market intelligence insights.

## 🧠 Overview

This system integrates multiple AI approaches to collect, analyze, and interpret market data:

- **Neural Intelligence**: Sentiment analysis, trend prediction, and pattern recognition
- **Symbolic Intelligence**: Rule-based decision engine with business logic
- **Adaptive Learning**: Machine learning models that improve over time
- **Real-time Dashboard**: Interactive web interface for visualization

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Data Collection│    │   AI Engine     │    │ Symbolic Engine│
│                 │    │                 │    │                 │
│ • Web Scraping  │───▶│ • Sentiment     │───▶│ • Rules Engine  │
│ • API Fetching  │    │   Analysis      │    │ • Decision      │
│ • Social Media  │    │ • Trend         │    │   Engine        │
│                 │    │   Prediction    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Adaptive Learning│
                    │                 │
                    │ • Model Training│
                    │ • Optimization  │
                    │ • Anomaly       │
                    │   Detection     │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Dashboard     │
                    │                 │
                    │ • Streamlit UI  │
                    │ • Visualizations│
                    │ • Reports       │
                    └─────────────────┘
```

## 🚀 Features

### Data Collection Layer
- **News Scraping**: Collect market news from multiple sources (Reuters, Bloomberg, CNBC)
- **API Integration**: Fetch data from NewsAPI, Google Trends, Alpha Vantage
- **Social Media Monitoring**: Track sentiment from Twitter and other platforms
- **Competitor Intelligence**: Monitor competitor activities and pricing

### Neural Intelligence Layer
- **Sentiment Analysis**: Multi-model ensemble approach (VADER, TextBlob, custom)
- **Trend Analysis**: Statistical and ML-based trend detection and prediction
- **Market Prediction**: Time series forecasting for market indicators
- **Keyword Extraction**: Identify trending topics and market drivers

### Symbolic Intelligence Layer
- **Business Rules**: Configurable rule engine with priority-based execution
- **Decision Making**: Context-aware decision generation
- **Risk Assessment**: Automated risk evaluation and alerts
- **Recommendation System**: Actionable insights and recommendations

### Adaptive Learning Layer
- **Model Training**: Continuous learning from new data
- **Rule Optimization**: Automatically improve rule parameters
- **Anomaly Detection**: Identify unusual market patterns
- **Performance Tracking**: Monitor and improve system accuracy

### Market Intelligence Dashboard
- **Real-time Monitoring**: Live market data and sentiment tracking
- **Interactive Visualizations**: Charts, graphs, and trend analysis
- **Decision History**: Track and analyze past decisions
- **System Configuration**: Manage rules, settings, and data sources

## 📋 Requirements

### System Requirements
- Python 3.8+
- MySQL 5.7+ or 8.0+
- 4GB+ RAM
- 10GB+ disk space

### Python Dependencies
See `requirements.txt` for complete list:

```bash
# Backend Framework
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0

# Database
mysql-connector-python==8.2.0
sqlalchemy==2.0.23

# AI/NLP Libraries
openai==1.3.7
transformers==4.36.0
torch==2.1.1
nltk==3.8.1
textblob==0.17.1
vaderSentiment==3.3.2

# Web Scraping
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.2

# Data Processing
pandas==2.1.4
numpy==1.25.2
scikit-learn==1.3.2

# Dashboard
streamlit==1.28.2
plotly==5.17.0
```

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd adaptive_market_intelligence
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Database
```bash
# Install MySQL (XAMPP recommended for Windows)
# Start MySQL service

# Create database and tables
mysql -u root -p < database/market.sql
```

### 4. Configure Environment Variables
Create `.env` file in project root:
```env
# Database Configuration
DATABASE_URL=mysql+mysqlconnector://root:password@localhost/market_intelligence

# API Keys (optional - system will work with simulated data)
NEWS_API_KEY=your_news_api_key_here
ALPHA_VANTAGE_KEY=your_alpha_vantage_key_here
TWITTER_BEARER_TOKEN=your_twitter_token_here

# OpenAI (optional - for advanced NLP)
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Initialize the System
```bash
# Test database connection
python backend/database.py

# Run initial setup (optional)
python -c "from backend.database import init_database; init_database()"
```

## 🚀 Running the System

### Start the Backend API
```bash
cd backend
python main.py
```
The API will be available at `http://localhost:8000`

### Start the Dashboard
```bash
cd dashboard
streamlit run app.py
```
The dashboard will be available at `http://localhost:8501`

### API Documentation
- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## 📊 Usage Guide

### 1. Data Collection
```python
# Collect news data
from data_collection.api_fetch import DataCollectionManager

manager = DataCollectionManager()
data = manager.collect_all_data(['market', 'technology', 'finance'])
```

### 2. Sentiment Analysis
```python
# Analyze sentiment
from ai_engine.sentiment import SentimentAnalyzer

analyzer = SentimentAnalyzer()
result = analyzer.analyze_sentiment_ensemble("Market is showing strong growth")
```

### 3. Rule Evaluation
```python
# Evaluate business rules
from symbolic_engine.rules import RuleEngine

engine = RuleEngine()
context = {'market_growth': 35, 'sentiment_score': 0.4}
results = engine.evaluate_rules(context)
```

### 4. Decision Making
```python
# Make market decisions
from symbolic_engine.decision_engine import DecisionEngine

decision_engine = DecisionEngine()
decisions = decision_engine.make_decision(context)
```

### 5. Adaptive Learning
```python
# Train models
from adaptive_module.learning import AdaptiveLearningEngine

learning_engine = AdaptiveLearningEngine()
result = learning_engine.learn_from_data(LearningType.RULE_OPTIMIZATION, training_data)
```

## 🎯 Key Components

### Data Collection
- **News Sources**: Reuters, Bloomberg, CNBC, MarketWatch
- **Market Data**: Alpha Vantage API for stock prices and indices
- **Trend Data**: Google Trends for keyword popularity
- **Social Media**: Twitter API for sentiment tracking

### AI Models
- **Sentiment Analysis**: Ensemble of VADER, TextBlob, and custom market-specific models
- **Trend Prediction**: Random Forest and Linear Regression models
- **Anomaly Detection**: Statistical methods and machine learning
- **Classification**: Rule success prediction and decision outcome prediction

### Business Rules
- **Investment Rules**: Market growth and sentiment-based investment recommendations
- **Marketing Rules**: Sentiment-based marketing improvement suggestions
- **Competitive Rules**: Competitor activity and price change responses
- **Risk Rules**: Volatility and anomaly-based risk alerts

### Dashboard Features
- **Real-time Monitoring**: Live data updates and alerts
- **Interactive Charts**: Sentiment trends, market analysis, decision history
- **Rule Management**: Configure and test business rules
- **System Status**: Monitor component health and performance

## 🔧 Configuration

### Database Configuration
Edit `backend/database.py` to modify database settings:
```python
DATABASE_URL = "mysql+mysqlconnector://user:password@localhost/market_intelligence"
```

### API Configuration
Modify data collection settings in `data_collection/api_fetch.py`:
```python
# Add new news sources
self.news_sources = {
    'reuters': 'https://www.reuters.com/markets',
    'your_source': 'https://your-source.com'
}
```

### Rule Configuration
Add custom rules in `symbolic_engine/rules.py`:
```python
custom_rule = MarketRule(
    rule_id="custom_rule",
    name="Custom Market Rule",
    condition="market_growth > 50 and sentiment_score > 0.5",
    action="Strong buy recommendation"
)
engine.add_rule(custom_rule)
```

## 📈 Performance Monitoring

### System Metrics
- API response times
- Database query performance
- Model accuracy scores
- Rule execution statistics

### Learning Analytics
- Model training history
- Performance improvements
- Anomaly detection accuracy
- Decision success rates

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure MySQL is running
   - Check database credentials in `.env`
   - Verify database and tables exist

2. **API Rate Limiting**
   - Check API key quotas
   - Implement request delays
   - Use cached data when possible

3. **Memory Issues**
   - Increase system RAM
   - Optimize data processing
   - Use batch processing for large datasets

4. **Dashboard Not Loading**
   - Ensure backend API is running
   - Check network connectivity
   - Verify API endpoint URLs

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black .
flake8 .
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting guide

## 🗺️ Roadmap

### Version 1.1 (Planned)
- [ ] Enhanced ML models
- [ ] More data sources
- [ ] Advanced visualizations
- [ ] Mobile dashboard

### Version 1.2 (Planned)
- [ ] Real-time streaming
- [ ] Advanced analytics
- [ ] Custom report generation
- [ ] API rate limiting

### Version 2.0 (Future)
- [ ] Multi-tenant support
- [ ] Cloud deployment
- [ ] Advanced security
- [ ] Microservices architecture

## 📊 Architecture Diagram

```mermaid
graph TB
    A[Web Dashboard] --> B[FastAPI Backend]
    B --> C[Database Layer]
    B --> D[Data Collection]
    B --> E[AI Engine]
    B --> F[Symbolic Engine]
    B --> G[Adaptive Learning]
    
    D --> D1[Web Scraping]
    D --> D2[API Integration]
    D --> D3[Social Media]
    
    E --> E1[Sentiment Analysis]
    E --> E2[Trend Prediction]
    E --> E3[Pattern Recognition]
    
    F --> F1[Rules Engine]
    F --> F2[Decision Engine]
    F --> F3[Risk Assessment]
    
    G --> G1[Model Training]
    G --> G2[Optimization]
    G --> G3[Anomaly Detection]
    
    C --> C1[Market Data]
    C --> C2[Rules]
    C --> C3[Decisions]
    C --> C4[Learning History]
```

## 📚 API Documentation

### Endpoints

#### Market Data
- `GET /api/v1/market/` - Get market data
- `POST /api/v1/market/` - Create market data entry
- `POST /api/v1/market/collect` - Trigger data collection

#### AI Analysis
- `POST /api/v1/analysis/sentiment` - Analyze sentiment
- `POST /api/v1/analysis/sentiment/batch` - Batch sentiment analysis
- `POST /api/v1/analysis/news-sentiment` - Analyze news sentiment

#### Rules & Decisions
- `GET /api/v1/rules/` - Get business rules
- `POST /api/v1/rules/evaluate` - Evaluate rules
- `POST /api/v1/decisions/make` - Make decisions

#### Learning
- `POST /api/v1/learning/train/{type}` - Train models
- `POST /api/v1/learning/predict/{type}` - Make predictions
- `POST /api/v1/learning/detect-anomalies` - Detect anomalies

For complete API documentation, visit `http://localhost:8000/docs`

---

**Built with ❤️ using Python, FastAPI, Streamlit, and Modern AI Technologies**

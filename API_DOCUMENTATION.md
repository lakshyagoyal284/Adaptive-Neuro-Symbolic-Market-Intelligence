# API Documentation

## Overview

The Adaptive Neuro-Symbolic Market Intelligence System provides a comprehensive RESTful API for accessing market intelligence capabilities. The API is built using FastAPI and provides automatic interactive documentation.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. In production deployments, API keys or OAuth tokens should be implemented.

## Response Format

All API responses follow a consistent JSON format:

### Success Response
```json
{
  "data": {...},
  "message": "Success",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Error Response
```json
{
  "detail": "Error description",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## Endpoints

### System Endpoints

#### Health Check
```http
GET /health
```

Check system health and API status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "database": "connected",
  "version": "1.0.0"
}
```

#### System Status
```http
GET /api/v1/status
```

Get detailed system status and statistics.

**Response:**
```json
{
  "system": {
    "status": "running",
    "timestamp": "2024-01-01T12:00:00.000Z"
  },
  "database": {
    "status": "connected"
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
    "rules_loaded": 8,
    "learning_sessions": 5,
    "recent_decisions": 12
  }
}
```

### Market Data Endpoints

#### Get Market Data
```http
GET /api/v1/market/
```

Retrieve market data with pagination and filtering.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records (default: 100, max: 1000)
- `category` (string, optional): Filter by category

**Response:**
```json
[
  {
    "id": 1,
    "source": "Reuters",
    "title": "Market shows strong growth",
    "content": "Article content...",
    "url": "https://reuters.com/article/1",
    "published_date": "2024-01-01T10:00:00.000Z",
    "category": "market_news",
    "sentiment_score": 0.75,
    "keywords": ["market", "growth", "investment"],
    "collected_date": "2024-01-01T12:00:00.000Z"
  }
]
```

#### Create Market Data
```http
POST /api/v1/market/
```

Create new market data entry.

**Request Body:**
```json
{
  "source": "Reuters",
  "title": "Market shows strong growth",
  "content": "Article content...",
  "url": "https://example.com",
  "published_date": "2024-01-01T10:00:00.000Z",
  "category": "market_news",
  "sentiment_score": 0.75,
  "keywords": ["market", "growth"]
}
```

#### Collect Market Data
```http
POST /api/v1/market/collect
```

Trigger background data collection from external sources.

**Query Parameters:**
- `source` (string, optional): News source (default: "reuters")
- `max_articles` (int, optional): Maximum articles to collect (default: 10)

**Response:**
```json
{
  "message": "Data collection started from reuters",
  "max_articles": 10,
  "timestamp": "2024-01-01T12:00:00.000Z",
  "status": "processing"
}
```

### Competitor Intelligence Endpoints

#### Get Competitor Data
```http
GET /api/v1/competitor/
```

Retrieve competitor intelligence data.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Maximum number of records
- `competitor_name` (string, optional): Filter by competitor name

**Response:**
```json
[
  {
    "id": 1,
    "competitor_name": "TechCorp",
    "product_name": "Cloud Platform",
    "price": 99.99,
    "market_share": 15.5,
    "activity_type": "Product Launch",
    "description": "New cloud platform launched",
    "source": "Web Monitoring",
    "recorded_date": "2024-01-01T12:00:00.000Z"
  }
]
```

#### Create Competitor Data
```http
POST /api/v1/competitor/
```

Create new competitor data entry.

**Request Body:**
```json
{
  "competitor_name": "TechCorp",
  "product_name": "Cloud Platform",
  "price": 99.99,
  "market_share": 15.5,
  "activity_type": "Product Launch",
  "description": "New cloud platform launched",
  "source": "Web Monitoring"
}
```

#### Monitor Competitors
```http
POST /api/v1/competitor/monitor
```

Trigger background competitor monitoring.

**Response:**
```json
{
  "message": "Competitor monitoring started",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### AI Analysis Endpoints

#### Analyze Sentiment
```http
POST /api/v1/analysis/sentiment
```

Analyze sentiment of provided text.

**Request Body:**
```json
{
  "text": "The market is showing strong growth with positive investor sentiment."
}
```

**Response:**
```json
{
  "text": "The market is showing strong growth with positive investor sentiment.",
  "sentiment": {
    "compound": 0.75,
    "positive": 0.6,
    "negative": 0.1,
    "neutral": 0.3,
    "confidence": 0.85,
    "keywords": ["market", "growth", "positive", "investor", "sentiment"],
    "analysis_method": "ensemble"
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### Batch Sentiment Analysis
```http
POST /api/v1/analysis/sentiment/batch
```

Analyze sentiment for multiple texts.

**Request Body:**
```json
{
  "texts": [
    "Market is showing strong growth",
    "Investor confidence is high",
    "Volatility remains a concern"
  ]
}
```

**Response:**
```json
{
  "texts_count": 3,
  "results": [
    {
      "compound": 0.75,
      "positive": 0.6,
      "negative": 0.1,
      "neutral": 0.3,
      "confidence": 0.85
    }
  ],
  "summary": {
    "total_texts": 3,
    "average_sentiment": 0.45,
    "positive_percentage": 66.7,
    "negative_percentage": 16.7,
    "neutral_percentage": 16.7
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### Analyze News Sentiment
```http
POST /api/v1/analysis/news-sentiment
```

Trigger sentiment analysis for recent news.

**Response:**
```json
{
  "message": "News sentiment analysis started",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Trend Analysis Endpoints

#### Get Trend Analysis
```http
GET /api/v1/trends/
```

Retrieve trend analysis data.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Maximum number of records
- `keyword` (string, optional): Filter by keyword

**Response:**
```json
[
  {
    "id": 1,
    "keyword": "AI market",
    "trend_score": 75.5,
    "volume": 50000,
    "growth_rate": 25.3,
    "source": "Google Trends",
    "analysis_date": "2024-01-01T12:00:00.000Z"
  }
]
```

#### Analyze Trends
```http
POST /api/v1/trends/analyze
```

Analyze trends for specified keywords.

**Request Body:**
```json
["AI market", "cryptocurrency", "stock market"]
```

**Response:**
```json
{
  "keywords": ["AI market", "cryptocurrency", "stock market"],
  "analysis": {
    "keyword_analysis": {
      "AI market": {
        "current_value": 75.5,
        "growth_rate": 25.3,
        "current_trend": {
          "direction": "increasing",
          "strength": 0.8,
          "confidence": 0.9
        },
        "prediction": {
          "predictions": [78, 80, 82, 85, 87],
          "trend_direction": "increasing"
        }
      }
    },
    "summary": {
      "total_keywords": 3,
      "average_growth_rate": 18.7,
      "top_performing_keywords": ["AI market"],
      "declining_keywords": []
    }
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Business Rules Endpoints

#### Get Rules
```http
GET /api/v1/rules/
```

Retrieve all business rules.

**Response:**
```json
{
  "rules": [
    {
      "rule_id": "high_growth_investment",
      "name": "High Growth Investment Alert",
      "description": "Trigger when market growth exceeds 30%",
      "condition": "market_growth > 30",
      "action": "Recommend investment in market segment",
      "rule_type": "threshold",
      "priority": 2,
      "status": "active",
      "execution_count": 15,
      "success_count": 12,
      "success_rate": 80.0
    }
  ],
  "total_count": 8,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### Get Specific Rule
```http
GET /api/v1/rules/{rule_id}
```

Retrieve specific rule by ID.

#### Evaluate Rules
```http
POST /api/v1/rules/evaluate
```

Evaluate rules against provided context.

**Request Body:**
```json
{
  "market_growth": 35,
  "sentiment_score": 0.4,
  "negative_sentiment": 25,
  "trend_demand": 70,
  "market_volatility": 20
}
```

**Response:**
```json
{
  "context": {
    "market_growth": 35,
    "sentiment_score": 0.4
  },
  "results": [
    {
      "rule_id": "high_growth_investment",
      "rule_name": "High Growth Investment Alert",
      "action": "Recommend investment in market segment. Growth: 35%",
      "success": true,
      "executed_at": "2024-01-01T12:00:00.000Z"
    }
  ],
  "triggered_count": 2,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### Get Rule Statistics
```http
GET /api/v1/rules/statistics
```

Get rule execution statistics.

**Response:**
```json
{
  "total_rules": 8,
  "active_rules": 8,
  "total_executions": 150,
  "total_successes": 120,
  "overall_success_rate": 80.0,
  "category_statistics": {
    "investment": {
      "rule_count": 3,
      "active_count": 3,
      "avg_success_rate": 85.0
    }
  },
  "top_performing_rules": [...],
  "generated_at": "2024-01-01T12:00:00.000Z"
}
```

### Decision Engine Endpoints

#### Make Decisions
```http
POST /api/v1/decisions/make
```

Make market intelligence decisions.

**Request Body:**
```json
{
  "market_growth": 35,
  "sentiment_score": 0.4,
  "ai_insights": {
    "sentiment_analysis": {
      "average_sentiment": 0.4,
      "overall_trend": "improving"
    }
  }
}
```

**Response:**
```json
{
  "context": {
    "market_growth": 35,
    "sentiment_score": 0.4
  },
  "ai_insights": {...},
  "decisions": [
    {
      "decision_id": "decision_20240101_120000_high_growth_investment",
      "decision_type": "investment",
      "title": "Investment Opportunity: High Market Growth Detected",
      "recommendation": "Consider investment in market segment. Growth: 35%",
      "priority": "high",
      "confidence": "high",
      "confidence_score": 0.8,
      "supporting_factors": ["Strong market growth (35%)", "Positive market sentiment (0.40)"],
      "risk_factors": ["Market volatility (20%)"],
      "rules_triggered": ["high_growth_investment"],
      "timestamp": "2024-01-01T12:00:00.000Z"
    }
  ],
  "decision_count": 2,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### Get Decision History
```http
GET /api/v1/decisions/history
```

Get recent decision history.

**Query Parameters:**
- `hours` (int, optional): Hours of history to retrieve (default: 24)

**Response:**
```json
{
  "total_decisions": 15,
  "time_window_hours": 24,
  "decision_types": {
    "investment": 8,
    "marketing": 4,
    "risk_management": 3
  },
  "priority_distribution": {
    "high": 6,
    "medium": 7,
    "low": 2
  },
  "average_confidence": 0.75,
  "top_decisions": [...],
  "generated_at": "2024-01-01T12:00:00.000Z"
}
```

### Adaptive Learning Endpoints

#### Train Model
```http
POST /api/v1/learning/train/{learning_type}
```

Train adaptive learning model.

**Path Parameters:**
- `learning_type` (string): Type of learning (rule_optimization, sentiment_improvement, trend_prediction, decision_accuracy)

**Request Body:**
```json
[
  {
    "market_growth": 25,
    "sentiment_score": 0.4,
    "volatility": 15,
    "competitor_activity": 3,
    "rule_success": 1
  }
]
```

**Response:**
```json
{
  "learning_type": "rule_optimization",
  "model_type": "classification",
  "accuracy_score": 0.85,
  "improvement_score": 0.15,
  "old_performance": 0.70,
  "new_performance": 0.85,
  "model_path": "models/rule_optimization_model.joblib",
  "features_used": ["market_growth", "sentiment_score", "volatility", "competitor_activity"],
  "training_samples": 100,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### Make Prediction
```http
POST /api/v1/learning/predict/{learning_type}
```

Make prediction using trained model.

**Path Parameters:**
- `learning_type` (string): Type of learning model

**Request Body:**
```json
{
  "market_growth": 30,
  "sentiment_score": 0.5,
  "volatility": 18,
  "competitor_activity": 4
}
```

**Response:**
```json
{
  "prediction": 1,
  "prediction_proba": {
    "0": 0.2,
    "1": 0.8
  },
  "learning_type": "rule_optimization",
  "model_type": "classification",
  "features_used": ["market_growth", "sentiment_score", "volatility", "competitor_activity"],
  "input_features": {
    "market_growth": 30,
    "sentiment_score": 0.5,
    "volatility": 18,
    "competitor_activity": 4
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### Detect Anomalies
```http
POST /api/v1/learning/detect-anomalies
```

Detect anomalies in provided data.

**Request Body:**
```json
[
  {
    "market_growth": 25,
    "sentiment_score": 0.4,
    "timestamp": "2024-01-01T12:00:00.000Z"
  },
  {
    "market_growth": 200,
    "sentiment_score": 0.9,
    "timestamp": "2024-01-01T12:00:00.000Z"
  }
]
```

**Response:**
```json
{
  "anomalies": [
    {
      "type": "statistical_outlier",
      "column": "market_growth",
      "value": 200,
      "expected_range": [10, 50],
      "z_score": 4.5,
      "timestamp": "2024-01-01T12:00:00.000Z",
      "severity": "high"
    }
  ],
  "anomaly_count": 1,
  "data_points": 2,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

#### Get Learning Summary
```http
GET /api/v1/learning/summary
```

Get learning system summary.

**Response:**
```json
{
  "total_learning_sessions": 5,
  "learning_types": {
    "rule_optimization": 2,
    "sentiment_improvement": 1,
    "trend_prediction": 2
  },
  "average_performance_by_type": {
    "rule_optimization": 0.85,
    "sentiment_improvement": 0.78,
    "trend_prediction": 0.82
  },
  "best_performing_type": {
    "type": "rule_optimization",
    "performance": 0.85
  },
  "total_improvements": 3,
  "models_trained": ["rule_optimization", "sentiment_improvement", "trend_prediction"],
  "last_learning": "2024-01-01T11:30:00.000Z"
}
```

## Error Codes

| Error Code | Description |
|------------|-------------|
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 422 | Validation Error - Input validation failed |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |
| 503 | Service Unavailable - Service down |

## Rate Limiting

API endpoints may have rate limiting to prevent abuse:

- Standard endpoints: 100 requests per minute
- Analysis endpoints: 10 requests per minute
- Learning endpoints: 5 requests per minute

Rate limit headers are included in responses:
- `X-RateLimit-Limit`: Request limit per window
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Time until reset (Unix timestamp)

## Interactive Documentation

The API provides interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to explore and test API endpoints directly from your browser.

## SDK Examples

### Python
```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api/v1"

# Analyze sentiment
response = requests.post(
    f"{BASE_URL}/analysis/sentiment",
    json={"text": "Market is showing strong growth"}
)
result = response.json()
print(f"Sentiment: {result['sentiment']['compound']}")

# Get market data
response = requests.get(f"{BASE_URL}/market/?limit=10")
market_data = response.json()
print(f"Retrieved {len(market_data)} market data items")
```

### JavaScript
```javascript
// Analyze sentiment
const response = await fetch('http://localhost:8000/api/v1/analysis/sentiment', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'Market is showing strong growth'
  })
});

const result = await response.json();
console.log('Sentiment:', result.sentiment.compound);
```

### cURL
```bash
# Analyze sentiment
curl -X POST "http://localhost:8000/api/v1/analysis/sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text": "Market is showing strong growth"}'

# Get market data
curl -X GET "http://localhost:8000/api/v1/market/?limit=10"
```

## Webhooks

The system can send webhook notifications for events:

### Configure Webhook
```http
POST /api/v1/webhooks/configure
```

**Request Body:**
```json
{
  "url": "https://your-webhook-url.com/endpoint",
  "events": ["decision_created", "rule_triggered", "anomaly_detected"],
  "secret": "your-webhook-secret"
}
```

### Webhook Payload
```json
{
  "event": "decision_created",
  "data": {
    "decision_id": "decision_20240101_120000_high_growth",
    "title": "Investment Opportunity Detected",
    "priority": "high"
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

This API documentation provides comprehensive information for integrating with the Adaptive Neuro-Symbolic Market Intelligence System.

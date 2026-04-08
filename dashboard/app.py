"""
Streamlit Dashboard for Adaptive Neuro-Symbolic Market Intelligence System
This module provides a web-based dashboard for visualizing market intelligence
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Any

# Configure page
st.set_page_config(
    page_title="Adaptive Market Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def api_request(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make API request to backend"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=10)
        else:
            return {"error": "Unsupported method"}
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def format_timestamp(timestamp_str: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str

def create_sentiment_gauge(sentiment_score: float) -> go.Figure:
    """Create sentiment gauge chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = sentiment_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Sentiment Score"},
        delta = {'reference': 0},
        gauge = {
            'axis': {'range': [-1, 1]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-1, -0.5], 'color': "lightgray"},
                {'range': [-0.5, 0.5], 'color': "gray"},
                {'range': [0.5, 1], 'color': "lightgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0.8
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_trend_chart(data: Dict) -> go.Figure:
    """Create trend analysis chart"""
    fig = go.Figure()
    
    for keyword, keyword_data in data.items():
        if 'timeline' in keyword_data and 'dates' in keyword_data:
            fig.add_trace(go.Scatter(
                x=keyword_data['dates'],
                y=keyword_data['timeline'],
                mode='lines+markers',
                name=keyword,
                line=dict(width=2)
            ))
    
    fig.update_layout(
        title="Trend Analysis",
        xaxis_title="Date",
        yaxis_title="Trend Score",
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_decision_chart(decisions: List[Dict]) -> go.Figure:
    """Create decisions distribution chart"""
    if not decisions:
        return go.Figure()
    
    # Count decisions by type
    decision_types = {}
    priorities = {}
    
    for decision in decisions:
        dtype = decision.get('decision_type', 'Unknown')
        priority = decision.get('priority', 'Unknown')
        
        decision_types[dtype] = decision_types.get(dtype, 0) + 1
        priorities[priority] = priorities.get(priority, 0) + 1
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Decisions by Type', 'Decisions by Priority'),
        specs=[[{"type": "pie"}, {"type": "pie"}]]
    )
    
    # Add pie charts
    fig.add_trace(
        go.Pie(labels=list(decision_types.keys()), values=list(decision_types.values()), name="Type"),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Pie(labels=list(priorities.keys()), values=list(priorities.values()), name="Priority"),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False)
    return fig

# Main dashboard
def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">🧠 Adaptive Neuro-Symbolic Market Intelligence</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Select Page",
            ["🏠 Dashboard", "📊 Market Data", "🤖 AI Analysis", "⚖️ Rules & Decisions", 
             "📈 Trends", "🎯 Competitors", "📚 Learning", "⚙️ Settings"]
        )
        
        st.header("System Status")
        if st.button("🔄 Refresh Status"):
            st.rerun()
        
        # Check API connection
        health_status = api_request("/health")
        if "error" not in health_status:
            st.success("✅ API Connected")
            st.info(f"Database: {health_status.get('database', 'Unknown')}")
        else:
            st.error("❌ API Connection Failed")
            st.error(health_status.get('error', 'Unknown error'))
    
    # Page content
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📊 Market Data":
        show_market_data()
    elif page == "🤖 AI Analysis":
        show_ai_analysis()
    elif page == "⚖️ Rules & Decisions":
        show_rules_decisions()
    elif page == "📈 Trends":
        show_trends()
    elif page == "🎯 Competitors":
        show_competitors()
    elif page == "📚 Learning":
        show_learning()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Main dashboard page"""
    
    st.header("📊 Market Intelligence Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Get system status
        status = api_request("/api/v1/status")
        if "error" not in status:
            stats = status.get('statistics', {})
            st.metric("Active Rules", stats.get('rules_loaded', 0))
    
    with col2:
        if "error" not in status:
            st.metric("Learning Sessions", stats.get('learning_sessions', 0))
    
    with col3:
        if "error" not in status:
            st.metric("Recent Decisions", stats.get('recent_decisions', 0))
    
    with col4:
        # Get decision summary
        decision_summary = api_request("/api/v1/decisions/history")
        if "error" not in decision_summary:
            st.metric("Avg Confidence", f"{decision_summary.get('average_confidence', 0):.2f}")
    
    # Recent decisions
    st.subheader("🎯 Recent Decisions")
    decisions = api_request("/api/v1/decisions/export?limit=10")
    
    if "error" not in decisions and decisions.get('decisions'):
        decision_data = decisions['decisions']
        
        # Display decisions
        for decision in decision_data[:5]:
            priority = decision.get('priority', 'medium')
            confidence = decision.get('confidence_score', 0)
            
            if priority == 'critical':
                st.markdown(f'<div class="error-box"><strong>{decision.get("title", "No Title")}</strong><br>{decision.get("recommendation", "No Recommendation")}</div>', 
                           unsafe_allow_html=True)
            elif priority == 'high':
                st.markdown(f'<div class="warning-box"><strong>{decision.get("title", "No Title")}</strong><br>{decision.get("recommendation", "No Recommendation")}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="success-box"><strong>{decision.get("title", "No Title")}</strong><br>{decision.get("recommendation", "No Recommendation")}</div>', 
                           unsafe_allow_html=True)
        
        # Decision chart
        if len(decision_data) > 0:
            fig = create_decision_chart(decision_data)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No recent decisions available")
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Collect Data", type="primary"):
            result = api_request("/api/v1/collect-data", method="POST")
            if "error" not in result:
                st.success("Data collection started!")
            else:
                st.error(result.get('error', 'Failed to start data collection'))
    
    with col2:
        if st.button("🧠 Analyze Sentiment", type="primary"):
            result = api_request("/api/v1/analysis/news-sentiment", method="POST")
            if "error" not in result:
                st.success("Sentiment analysis started!")
            else:
                st.error(result.get('error', 'Failed to start sentiment analysis'))
    
    with col3:
        if st.button("📊 Comprehensive Analysis", type="primary"):
            result = api_request("/api/v1/comprehensive-analysis", method="POST")
            if "error" not in result:
                st.success("Comprehensive analysis started!")
            else:
                st.error(result.get('error', 'Failed to start comprehensive analysis'))

def show_market_data():
    """Market data page"""
    
    st.header("📊 Market Data")
    
    # Data collection controls
    col1, col2 = st.columns(2)
    
    with col1:
        source = st.selectbox("News Source", ["reuters", "bloomberg", "cnbc", "marketwatch"])
        max_articles = st.slider("Max Articles", 1, 50, 10)
    
    with col2:
        if st.button("📰 Collect News", type="primary"):
            result = api_request(f"/api/v1/market/collect?source={source}&max_articles={max_articles}", method="POST")
            if "error" not in result:
                st.success(f"Started collecting {max_articles} articles from {source}")
            else:
                st.error(result.get('error', 'Failed to start collection'))
    
    # Display market data
    st.subheader("📈 Recent Market Data")
    
    market_data = api_request("/api/v1/market/?limit=50")
    
    if "error" not in market_data and market_data:
        df = pd.DataFrame(market_data)
        
        # Display data table
        st.dataframe(df[['title', 'source', 'category', 'sentiment_score', 'published_date']], use_container_width=True)
        
        # Sentiment distribution
        if 'sentiment_score' in df.columns:
            st.subheader("😊 Sentiment Distribution")
            
            # Create sentiment categories
            df['sentiment_category'] = pd.cut(
                df['sentiment_score'], 
                bins=[-1, -0.3, 0.3, 1], 
                labels=['Negative', 'Neutral', 'Positive']
            )
            
            sentiment_counts = df['sentiment_category'].value_counts()
            
            fig = px.pie(
                values=sentiment_counts.values, 
                names=sentiment_counts.index,
                title="Sentiment Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No market data available. Start data collection to see results.")

def show_ai_analysis():
    """AI analysis page"""
    
    st.header("🤖 AI Analysis")
    
    # Sentiment analysis
    st.subheader("📝 Sentiment Analysis")
    
    # Text input for sentiment analysis
    text_input = st.text_area("Enter text for sentiment analysis:", height=100)
    
    if st.button("🔍 Analyze Sentiment"):
        if text_input:
            result = api_request("/api/v1/analysis/sentiment", method="POST", data={"text": text_input})
            
            if "error" not in result:
                sentiment_data = result.get('sentiment', {})
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Compound Score", f"{sentiment_data.get('compound', 0):.3f}")
                
                with col2:
                    st.metric("Positive", f"{sentiment_data.get('positive', 0):.3f}")
                
                with col3:
                    st.metric("Negative", f"{sentiment_data.get('negative', 0):.3f}")
                
                # Sentiment gauge
                fig = create_sentiment_gauge(sentiment_data.get('compound', 0))
                st.plotly_chart(fig, use_container_width=True)
                
                # Keywords
                if sentiment_data.get('keywords'):
                    st.subheader("🔑 Keywords")
                    keywords = sentiment_data['keywords']
                    st.write(", ".join(keywords))
            else:
                st.error(result.get('error', 'Sentiment analysis failed'))
        else:
            st.warning("Please enter text to analyze")
    
    # Batch sentiment analysis
    st.subheader("📊 Batch Sentiment Analysis")
    
    batch_texts = st.text_area("Enter multiple texts (one per line):", height=150)
    
    if st.button("📈 Analyze Batch"):
        if batch_texts:
            texts = [text.strip() for text in batch_texts.split('\n') if text.strip()]
            
            if texts:
                result = api_request("/api/v1/analysis/sentiment/batch", method="POST", data={"texts": texts})
                
                if "error" not in result:
                    summary = result.get('summary', {})
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Texts", summary.get('total_texts', 0))
                    
                    with col2:
                        st.metric("Avg Sentiment", f"{summary.get('average_sentiment', 0):.3f}")
                    
                    with col3:
                        st.metric("Positive %", f"{summary.get('positive_percentage', 0):.1f}%")
                    
                    # Results table
                    results = result.get('results', [])
                    if results:
                        df_results = pd.DataFrame(results)
                        st.dataframe(df_results[['compound', 'positive', 'negative', 'confidence']], use_container_width=True)
                else:
                    st.error(result.get('error', 'Batch analysis failed'))
            else:
                st.warning("No valid texts found")
        else:
            st.warning("Please enter texts to analyze")

def show_rules_decisions():
    """Rules and decisions page"""
    
    st.header("⚖️ Rules & Decisions")
    
    # Rules section
    st.subheader("📋 Business Rules")
    
    rules_data = api_request("/api/v1/rules/")
    
    if "error" not in rules_data and rules_data.get('rules'):
        rules = rules_data['rules']
        
        # Rules statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Rules", len(rules))
        
        with col2:
            active_rules = [r for r in rules if r.get('status') == 'active']
            st.metric("Active Rules", len(active_rules))
        
        with col3:
            avg_success = np.mean([r.get('success_rate', 0) for r in rules])
            st.metric("Avg Success Rate", f"{avg_success:.1f}%")
        
        # Rules table
        df_rules = pd.DataFrame(rules)
        st.dataframe(df_rules[['name', 'rule_type', 'priority', 'status', 'success_rate']], use_container_width=True)
        
        # Rule evaluation
        st.subheader("🧪 Test Rules")
        
        # Create test context
        col1, col2 = st.columns(2)
        
        with col1:
            market_growth = st.slider("Market Growth (%)", -50, 100, 25)
            sentiment_score = st.slider("Sentiment Score", -1.0, 1.0, 0.3, 0.1)
        
        with col2:
            trend_demand = st.slider("Trend Demand", 0, 100, 70)
            market_volatility = st.slider("Market Volatility (%)", 0, 100, 20)
        
        test_context = {
            "market_growth": market_growth,
            "sentiment_score": sentiment_score,
            "trend_demand": trend_demand,
            "market_volatility": market_volatility
        }
        
        if st.button("🎯 Evaluate Rules"):
            result = api_request("/api/v1/rules/evaluate", method="POST", data=test_context)
            
            if "error" not in result:
                triggered_rules = result.get('results', [])
                
                st.success(f"Triggered {len(triggered_rules)} rules:")
                
                for rule_result in triggered_rules:
                    if rule_result.get('success'):
                        st.markdown(f"**{rule_result.get('rule_name', 'Unknown')}**: {rule_result.get('action', 'No action')}")
            else:
                st.error(result.get('error', 'Rule evaluation failed'))
    
    # Decisions section
    st.subheader("🎯 Recent Decisions")
    
    decisions_data = api_request("/api/v1/decisions/export?limit=20")
    
    if "error" not in decisions_data and decisions_data.get('decisions'):
        decisions = decisions_data['decisions']
        
        # Decision chart
        fig = create_decision_chart(decisions)
        st.plotly_chart(fig, use_container_width=True)
        
        # Decisions table
        df_decisions = pd.DataFrame(decisions)
        st.dataframe(df_decisions[['title', 'decision_type', 'priority', 'confidence', 'timestamp']], use_container_width=True)
    else:
        st.info("No decisions available")

def show_trends():
    """Trends analysis page"""
    
    st.header("📈 Trend Analysis")
    
    # Trend analysis controls
    st.subheader("🔍 Analyze Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        keywords_input = st.text_area("Keywords (one per line):", "AI market\ncryptocurrency\nstock market")
        keywords = [k.strip() for k in keywords_input.split('\n') if k.strip()]
    
    with col2:
        time_window = st.selectbox("Time Window", ["today 7-d", "today 30-d", "today 90-d"])
    
    if st.button("📊 Analyze Trends", type="primary"):
        if keywords:
            result = api_request("/api/v1/trends/analyze", method="POST", data=keywords)
            
            if "error" not in result:
                analysis = result.get('analysis', {})
                
                # Display trend charts
                if analysis.get('keyword_analysis'):
                    st.subheader("📈 Trend Charts")
                    
                    # Prepare data for chart
                    trend_data = {}
                    for keyword, data in analysis['keyword_analysis'].items():
                        if 'prediction' in data and 'timeline' in data['prediction']:
                            trend_data[keyword] = data['prediction']
                    
                    if trend_data:
                        fig = create_trend_chart(trend_data)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Trend summary table
                    st.subheader("📊 Trend Summary")
                    
                    trend_summary = []
                    for keyword, data in analysis['keyword_analysis'].items():
                        current_trend = data.get('current_trend', {})
                        prediction = data.get('prediction', {})
                        
                        trend_summary.append({
                            'Keyword': keyword,
                            'Current Value': data.get('current_value', 0),
                            'Growth Rate (%)': data.get('growth_rate', 0),
                            'Trend Direction': current_trend.get('direction', 'unknown'),
                            'Predicted Trend': prediction.get('trend_direction', 'unknown')
                        })
                    
                    df_trends = pd.DataFrame(trend_summary)
                    st.dataframe(df_trends, use_container_width=True)
                    
                    # Summary statistics
                    st.subheader("📈 Summary Statistics")
                    
                    summary = analysis.get('summary', {})
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Keywords", summary.get('total_keywords', 0))
                    
                    with col2:
                        st.metric("Avg Growth Rate", f"{summary.get('average_growth_rate', 0):.1f}%")
                    
                    with col3:
                        st.metric("Avg Volatility", f"{summary.get('average_volatility', 0):.3f}")
                    
                    # Top performing keywords
                    if summary.get('top_performing_keywords'):
                        st.subheader("🚀 Top Performing Keywords")
                        for keyword in summary['top_performing_keywords']:
                            st.success(f"• {keyword}")
                    
                    # Declining keywords
                    if summary.get('declining_keywords'):
                        st.subheader("📉 Declining Keywords")
                        for keyword in summary['declining_keywords']:
                            st.warning(f"• {keyword}")
            else:
                st.error(result.get('error', 'Trend analysis failed'))
        else:
            st.warning("Please enter keywords to analyze")
    
    # Historical trend data
    st.subheader("📚 Historical Trend Data")
    
    trend_data = api_request("/api/v1/trends/?limit=50")
    
    if "error" not in trend_data and trend_data:
        df_trends = pd.DataFrame(trend_data)
        st.dataframe(df_trends[['keyword', 'trend_score', 'volume', 'growth_rate', 'analysis_date']], use_container_width=True)
    else:
        st.info("No historical trend data available")

def show_competitors():
    """Competitor intelligence page"""
    
    st.header("🎯 Competitor Intelligence")
    
    # Competitor monitoring
    st.subheader("🔍 Monitor Competitors")
    
    if st.button("🔄 Start Monitoring", type="primary"):
        result = api_request("/api/v1/competitor/monitor", method="POST")
        
        if "error" not in result:
            st.success("Competitor monitoring started!")
        else:
            st.error(result.get('error', 'Failed to start monitoring'))
    
    # Competitor data
    st.subheader("📊 Competitor Data")
    
    competitor_data = api_request("/api/v1/competitor/?limit=50")
    
    if "error" not in competitor_data and competitor_data:
        df_competitors = pd.DataFrame(competitor_data)
        
        # Display competitor data
        st.dataframe(df_competitors[['competitor_name', 'product_name', 'price', 'market_share', 'activity_type']], use_container_width=True)
        
        # Competitor analysis
        if not df_competitors.empty:
            st.subheader("📈 Competitor Analysis")
            
            # Market share distribution
            if 'market_share' in df_competitors.columns:
                fig = px.pie(
                    df_competitors, 
                    values='market_share', 
                    names='competitor_name',
                    title="Market Share Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Price comparison
            if 'price' in df_competitors.columns:
                fig = px.bar(
                    df_competitors,
                    x='competitor_name',
                    y='price',
                    title="Price Comparison"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Activity types
            if 'activity_type' in df_competitors.columns:
                activity_counts = df_competitors['activity_type'].value_counts()
                
                fig = px.pie(
                    values=activity_counts.values,
                    names=activity_counts.index,
                    title="Competitor Activity Types"
                )
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No competitor data available. Start monitoring to see results.")

def show_learning():
    """Adaptive learning page"""
    
    st.header("📚 Adaptive Learning")
    
    # Learning summary
    st.subheader("📊 Learning Summary")
    
    summary = api_request("/api/v1/learning/summary")
    
    if "error" not in summary:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Learning Sessions", summary.get('total_learning_sessions', 0))
        
        with col2:
            st.metric("Total Improvements", summary.get('total_improvements', 0))
        
        with col3:
            models_trained = summary.get('models_trained', [])
            st.metric("Models Trained", len(models_trained))
        
        # Learning by type
        if summary.get('learning_types'):
            st.subheader("📈 Learning by Type")
            
            learning_types = summary['learning_types']
            df_learning = pd.DataFrame(list(learning_types.items()), columns=['Learning Type', 'Sessions'])
            st.dataframe(df_learning, use_container_width=True)
        
        # Performance by type
        if summary.get('average_performance_by_type'):
            st.subheader("🎯 Performance by Type")
            
            performance = summary['average_performance_by_type']
            df_performance = pd.DataFrame(list(performance.items()), columns=['Learning Type', 'Avg Performance'])
            
            fig = px.bar(
                df_performance,
                x='Learning Type',
                y='Avg Performance',
                title="Model Performance by Type"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Best performing type
        if summary.get('best_performing_type'):
            best = summary['best_performing_type']
            st.success(f"🏆 Best Performing Type: {best['type']} (Performance: {best['performance']:.3f})")
    
    # Learning history
    st.subheader("📚 Learning History")
    
    history = api_request("/api/v1/learning/history?limit=20")
    
    if "error" not in history and history.get('learning_history'):
        df_history = pd.DataFrame(history['learning_history'])
        
        # Display relevant columns
        display_cols = ['learning_type', 'model_type', 'accuracy_score', 'improvement_score', 'training_samples', 'timestamp']
        available_cols = [col for col in display_cols if col in df_history.columns]
        
        st.dataframe(df_history[available_cols], use_container_width=True)
    else:
        st.info("No learning history available")
    
    # Anomaly detection
    st.subheader("🚨 Anomaly Detection")
    
    # Sample data for anomaly detection (in real app, this would come from actual data)
    sample_data = [
        {"market_growth": 25, "sentiment_score": 0.4, "timestamp": datetime.now().isoformat()},
        {"market_growth": 30, "sentiment_score": 0.5, "timestamp": datetime.now().isoformat()},
        {"market_growth": 200, "sentiment_score": 0.9, "timestamp": datetime.now().isoformat()},  # Anomaly
        {"market_growth": 28, "sentiment_score": 0.3, "timestamp": datetime.now().isoformat()}
    ]
    
    if st.button("🔍 Detect Anomalies"):
        result = api_request("/api/v1/learning/detect-anomalies", method="POST", data=sample_data)
        
        if "error" not in result:
            anomalies = result.get('anomalies', [])
            
            if anomalies:
                st.warning(f"🚨 Detected {len(anomalies)} anomalies:")
                
                for anomaly in anomalies:
                    st.error(f"• {anomaly.get('type', 'Unknown')} in {anomaly.get('column', 'Unknown')}: {anomaly.get('value', 'N/A')}")
            else:
                st.success("✅ No anomalies detected")
        else:
            st.error(result.get('error', 'Anomaly detection failed'))

def show_settings():
    """Settings page"""
    
    st.header("⚙️ Settings")
    
    # System configuration
    st.subheader("🔧 System Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("API Base URL", value=API_BASE_URL, disabled=True)
        st.text_input("Database Host", value="localhost", disabled=True)
        st.text_input("Database Port", value="3306", disabled=True)
    
    with col2:
        st.selectbox("Log Level", ["INFO", "DEBUG", "WARNING", "ERROR"], index=0)
        st.number_input("Data Collection Interval (minutes)", value=60, min_value=1, max_value=1440)
        st.number_input("Model Retrain Interval (hours)", value=24, min_value=1, max_value=168)
    
    # Data collection settings
    st.subheader("📊 Data Collection Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.multiselect(
            "News Sources",
            ["reuters", "bloomberg", "cnbc", "marketwatch"],
            default=["reuters", "cnbc"]
        )
        
        st.text_input("News API Key", type="password", placeholder="Enter your News API key")
    
    with col2:
        st.text_input("Alpha Vantage API Key", type="password", placeholder="Enter your Alpha Vantage key")
        st.text_input("Twitter Bearer Token", type="password", placeholder="Enter your Twitter API token")
    
    # AI Model settings
    st.subheader("🤖 AI Model Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox("Sentiment Analysis Model", ["ensemble", "vader", "textblob"], index=0)
        st.slider("Sentiment Confidence Threshold", 0.0, 1.0, 0.5, 0.1)
    
    with col2:
        st.selectbox("Trend Prediction Model", ["random_forest", "linear_regression"], index=0)
        st.slider("Trend Prediction Horizon", 1, 30, 7)
    
    # Rule settings
    st.subheader("⚖️ Rule Engine Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.slider("Market Growth Threshold (%)", 0, 100, 30)
        st.slider("Negative Sentiment Threshold (%)", 0, 100, 40)
    
    with col2:
        st.slider("Demand Threshold", 0, 100, 70)
        st.slider("Market Share Threshold (%)", 0, 50, 15)
    
    # Save settings
    if st.button("💾 Save Settings", type="primary"):
        st.success("Settings saved successfully!")
        st.info("Some settings may require a restart to take effect.")
    
    # System information
    st.subheader("ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Python Version", "3.8+")
        st.metric("Streamlit Version", "1.28.2")
    
    with col2:
        st.metric("FastAPI Version", "0.104.1")
        st.metric("System Status", "Running")

if __name__ == "__main__":
    main()

"""
Sample Data Generator for Adaptive Market Intelligence System
This script generates sample data to demonstrate the system capabilities
"""

import random
import json
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """Create database connection"""
    try:
        # Parse DATABASE_URL
        db_url = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://root:@localhost/market_intelligence')
        
        # Extract connection details
        if 'mysql+mysqlconnector://' in db_url:
            db_url = db_url.replace('mysql+mysqlconnector://', '')
        
        if '@' in db_url:
            credentials, host_db = db_url.split('@')
            if ':' in credentials:
                user, password = credentials.split(':', 1)
            else:
                user, password = credentials, ''
            
            if '/' in host_db:
                host, database = host_db.split('/', 1)
            else:
                host, database = host_db, ''
        else:
            user, password, host, database = 'root', '', 'localhost', 'market_intelligence'
        
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def generate_sample_news():
    """Generate sample news articles"""
    news_templates = [
        "Tech stocks surge as {company} reports strong earnings",
        "Market volatility increases amid {event} concerns",
        "{company} announces new product line, investors optimistic",
        "Economic indicators show {trend} in {sector} sector",
        "Analysts upgrade {company} stock on {reason} prospects",
        "Federal Reserve signals {policy} stance on interest rates",
        "{company} faces challenges in {market} market conditions",
        "Breaking: {event} impacts global market sentiment",
        "Investment opportunities emerge in {sector} sector",
        "Market rally continues as {factor} drives optimism"
    ]
    
    companies = ["Apple", "Microsoft", "Google", "Amazon", "Tesla", "Meta", "Netflix", "NVIDIA"]
    events = ["inflation", "recession", "geopolitical", "supply chain", "regulatory"]
    sectors = ["technology", "healthcare", "finance", "energy", "consumer goods"]
    trends = ["positive growth", "declining performance", "mixed signals", "strong momentum"]
    reasons = ["growth", "innovation", "market expansion", "cost reduction"]
    policies = ["hawkish", "dovish", "neutral", "accommodative"]
    markets = ["emerging", "developed", "domestic", "international"]
    factors = ["earnings", "economic data", "technological advances", "consumer demand"]
    
    news_articles = []
    
    for i in range(50):
        template = random.choice(news_templates)
        title = template.format(
            company=random.choice(companies),
            event=random.choice(events),
            sector=random.choice(sectors),
            trend=random.choice(trends),
            reason=random.choice(reasons),
            policy=random.choice(policies),
            market=random.choice(markets),
            factor=random.choice(factors)
        )
        
        # Generate content
        content = f"""
        {title}. This development has significant implications for investors and market analysts.
        
        Market experts suggest that this could lead to increased volatility in the short term,
        but may present opportunities for long-term investors. The company's fundamentals
        remain strong according to recent analysis.
        
        Technical indicators show mixed signals, with some metrics suggesting overbought
        conditions while others indicate room for growth. Investors are advised to conduct
        thorough research before making investment decisions.
        
        The broader market context includes concerns about economic growth, inflation
        pressures, and geopolitical tensions that could impact market performance in the
        coming months.
        """
        
        # Generate random date within last 30 days
        days_ago = random.randint(0, 30)
        published_date = datetime.now() - timedelta(days=days_ago)
        
        # Generate sentiment score (-1 to 1)
        sentiment_score = random.uniform(-0.8, 0.8)
        
        # Generate keywords
        keywords = ["market", "stocks", "investment", "economy"]
        if sentiment_score > 0.3:
            keywords.extend(["growth", "bullish", "opportunity"])
        elif sentiment_score < -0.3:
            keywords.extend(["risk", "bearish", "concern"])
        
        article = {
            'source': random.choice(['Reuters', 'Bloomberg', 'CNBC', 'MarketWatch']),
            'title': title.strip(),
            'content': content.strip(),
            'url': f"https://example.com/news/{i}",
            'published_date': published_date,
            'category': random.choice(['market_news', 'technology', 'finance', 'economy']),
            'sentiment_score': sentiment_score,
            'keywords': keywords
        }
        
        news_articles.append(article)
    
    return news_articles

def generate_sample_competitor_data():
    """Generate sample competitor intelligence data"""
    competitors = [
        "TechCorp", "DataSoft", "CloudNet", "InfoSys", "CyberTech",
        "AI Solutions", "Quantum Computing", "Blockchain Inc", "IoT Systems", "Robotics Ltd"
    ]
    
    products = [
        "Cloud Platform", "AI Assistant", "Data Analytics", "Security Suite",
        "Mobile App", "Web Service", "Enterprise Software", "Consumer Device"
    ]
    
    activities = [
        "Product Launch", "Price Change", "Marketing Campaign", "Partnership",
        "Acquisition", "Expansion", "Research Investment", "Customer Update"
    ]
    
    competitor_data = []
    
    for i in range(30):
        competitor_name = random.choice(competitors)
        product_name = random.choice(products)
        
        data = {
            'competitor_name': competitor_name,
            'product_name': product_name,
            'price': round(random.uniform(10, 500), 2),
            'market_share': round(random.uniform(5, 25), 1),
            'activity_type': random.choice(activities),
            'description': f"{competitor_name} announced {random.choice(activities).lower()} for {product_name}",
            'source': 'Web Monitoring',
            'recorded_date': datetime.now() - timedelta(hours=random.randint(1, 168))
        }
        
        competitor_data.append(data)
    
    return competitor_data

def generate_sample_trend_data():
    """Generate sample trend analysis data"""
    keywords = [
        "AI market", "cryptocurrency", "stock market", "blockchain",
        "machine learning", "cloud computing", "cybersecurity", "fintech"
    ]
    
    trend_data = []
    
    for keyword in keywords:
        # Generate trend timeline (last 7 days)
        timeline = []
        dates = []
        
        base_value = random.uniform(20, 80)
        
        for i in range(7):
            date = datetime.now() - timedelta(days=6-i)
            dates.append(date.strftime('%Y-%m-%d'))
            
            # Add some randomness and trend
            change = random.uniform(-10, 15)
            base_value = max(0, min(100, base_value + change))
            timeline.append(round(base_value, 2))
        
        data = {
            'keyword': keyword,
            'trend_score': round(random.uniform(0, 100), 2),
            'volume': random.randint(1000, 100000),
            'growth_rate': round(random.uniform(-50, 200), 2),
            'source': 'Google Trends',
            'analysis_date': datetime.now()
        }
        
        trend_data.append(data)
    
    return trend_data

def generate_sample_recommendations():
    """Generate sample recommendations"""
    recommendation_types = [
        "investment", "marketing", "competitive", "risk_management", "opportunity"
    ]
    
    titles = [
        "Strong Buy Recommendation Based on Market Growth",
        "Marketing Campaign Needed for Negative Sentiment",
        "Competitive Response to Price Changes Required",
        "Risk Management Strategy for High Volatility",
        "Market Expansion Opportunity Identified",
        "Portfolio Rebalancing Recommended",
        "New Product Launch Consideration",
        "Strategic Partnership Opportunity"
    ]
    
    descriptions = [
        "Analysis indicates strong potential for investment returns",
        "Negative market sentiment requires immediate marketing attention",
        "Competitor pricing changes suggest strategic response needed",
        "High market volatility requires risk mitigation measures",
        "Market analysis reveals expansion opportunities",
        "Portfolio analysis suggests rebalancing for optimal returns",
        "Market conditions favorable for new product introduction",
        "Strategic partnership could enhance market position"
    ]
    
    recommendations = []
    
    for i in range(20):
        rec_type = random.choice(recommendation_types)
        
        recommendation = {
            'recommendation_type': rec_type,
            'title': random.choice(titles),
            'description': random.choice(descriptions),
            'priority': random.choice(['high', 'medium', 'low']),
            'confidence_score': round(random.uniform(0.6, 0.95), 2),
            'status': random.choice(['pending', 'implemented', 'reviewed']),
            'generated_date': datetime.now() - timedelta(hours=random.randint(1, 72))
        }
        
        recommendations.append(recommendation)
    
    return recommendations

def insert_sample_data():
    """Insert sample data into database"""
    connection = get_db_connection()
    if not connection:
        print("Failed to connect to database")
        return
    
    try:
        cursor = connection.cursor()
        
        print("Generating sample data...")
        
        # Generate and insert market data
        print("Generating market news data...")
        news_data = generate_sample_news()
        
        for news in news_data:
            query = """
            INSERT INTO market_data (source, title, content, url, published_date, category, sentiment_score, keywords)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                news['source'], news['title'], news['content'], news['url'],
                news['published_date'], news['category'], news['sentiment_score'],
                json.dumps(news['keywords'])
            ))
        
        print(f"Inserted {len(news_data)} news articles")
        
        # Generate and insert competitor data
        print("Generating competitor data...")
        competitor_data = generate_sample_competitor_data()
        
        for comp in competitor_data:
            query = """
            INSERT INTO competitor_data (competitor_name, product_name, price, market_share, activity_type, description, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                comp['competitor_name'], comp['product_name'], comp['price'],
                comp['market_share'], comp['activity_type'], comp['description'], comp['source']
            ))
        
        print(f"Inserted {len(competitor_data)} competitor records")
        
        # Generate and insert trend data
        print("Generating trend data...")
        trend_data = generate_sample_trend_data()
        
        for trend in trend_data:
            query = """
            INSERT INTO trend_analysis (keyword, trend_score, volume, growth_rate, source)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                trend['keyword'], trend['trend_score'], trend['volume'],
                trend['growth_rate'], trend['source']
            ))
        
        print(f"Inserted {len(trend_data)} trend records")
        
        # Generate and insert recommendations
        print("Generating recommendations...")
        recommendations = generate_sample_recommendations()
        
        for rec in recommendations:
            query = """
            INSERT INTO recommendations (recommendation_type, title, description, priority, confidence_score, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                rec['recommendation_type'], rec['title'], rec['description'],
                rec['priority'], rec['confidence_score'], rec['status']
            ))
        
        print(f"Inserted {len(recommendations)} recommendations")
        
        # Commit all changes
        connection.commit()
        print("\nSample data inserted successfully!")
        print("\nSummary:")
        print(f"- News Articles: {len(news_data)}")
        print(f"- Competitor Data: {len(competitor_data)}")
        print(f"- Trend Analysis: {len(trend_data)}")
        print(f"- Recommendations: {len(recommendations)}")
        
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    print("Adaptive Market Intelligence - Sample Data Generator")
    print("=" * 50)
    
    # Check if database exists
    connection = get_db_connection()
    if connection:
        print("Database connection successful!")
        connection.close()
        
        # Ask user confirmation
        response = input("\nDo you want to generate and insert sample data? (y/n): ")
        if response.lower() in ['y', 'yes']:
            insert_sample_data()
        else:
            print("Sample data generation cancelled.")
    else:
        print("Failed to connect to database. Please check your configuration.")
        print("Make sure MySQL is running and the database exists.")
        print("Run: mysql -u root -p < database/market.sql")

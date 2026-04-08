"""
API Data Fetcher Module
This module handles fetching data from various APIs including news, market data, and trends
"""

import requests
import json
import time
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsAPIFetcher:
    """
    Fetcher for news data using NewsAPI or similar services
    """
    
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY', 'your_news_api_key_here')
        self.base_url = 'https://newsapi.org/v2'
        self.session = requests.Session()
        
        # Categories for market intelligence
        self.categories = ['business', 'technology', 'finance']
        self.keywords = ['market', 'stock', 'economy', 'investment', 'trading']
    
    def fetch_market_news(self, query: str = 'market OR stock OR economy', days: int = 7) -> List[Dict]:
        """
        Fetch market news from NewsAPI
        
        Args:
            query: Search query for news
            days: Number of days to look back
        
        Returns:
            List of news articles
        """
        try:
            # Calculate date range
            from_date = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
            to_date = datetime.utcnow().strftime('%Y-%m-%d')
            
            params = {
                'q': query,
                'from': from_date,
                'to': to_date,
                'language': 'en',
                'sortBy': 'relevancy',
                'pageSize': 50,
                'apiKey': self.api_key
            }
            
            logger.info(f"Fetching market news for query: {query}")
            response = self.session.get(f"{self.base_url}/everything", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'ok':
                logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                return []
            
            articles = []
            for article in data.get('articles', []):
                processed_article = {
                    'source': article['source']['name'],
                    'title': article['title'],
                    'content': article.get('content', article.get('description', '')),
                    'url': article['url'],
                    'published_date': self._parse_newsapi_date(article['publishedAt']),
                    'category': 'market_news',
                    'author': article.get('author'),
                    'image_url': article.get('urlToImage')
                }
                articles.append(processed_article)
            
            logger.info(f"Successfully fetched {len(articles)} news articles")
            return articles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch news from NewsAPI: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching news: {e}")
            return []
    
    def _parse_newsapi_date(self, date_str: str) -> datetime:
        """Parse date from NewsAPI format"""
        try:
            # NewsAPI returns ISO 8601 format
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return datetime.utcnow()
    
    def fetch_category_news(self, category: str = 'business') -> List[Dict]:
        """Fetch news by category"""
        try:
            params = {
                'category': category,
                'language': 'en',
                'country': 'us',
                'pageSize': 20,
                'apiKey': self.api_key
            }
            
            response = self.session.get(f"{self.base_url}/top-headlines", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'ok':
                logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                return []
            
            articles = []
            for article in data.get('articles', []):
                processed_article = {
                    'source': article['source']['name'],
                    'title': article['title'],
                    'content': article.get('content', article.get('description', '')),
                    'url': article['url'],
                    'published_date': self._parse_newsapi_date(article['publishedAt']),
                    'category': category,
                    'author': article.get('author')
                }
                articles.append(processed_article)
            
            return articles
            
        except Exception as e:
            logger.error(f"Failed to fetch {category} news: {e}")
            return []

class GoogleTrendsAPI:
    """
    Fetcher for Google Trends data
    Note: This uses pytrends library for Google Trends API
    """
    
    def __init__(self):
        try:
            from pytrends.request import TrendReq
            self.pytrends = TrendReq(hl='en-US', tz=360)
        except ImportError:
            logger.warning("pytrends not installed. Google Trends data will be simulated.")
            self.pytrends = None
    
    def fetch_trend_data(self, keywords: List[str], timeframe: str = 'today 7-d') -> Dict[str, Any]:
        """
        Fetch trend data for specified keywords
        
        Args:
            keywords: List of keywords to analyze
            timeframe: Timeframe for trend analysis
        
        Returns:
            Dictionary with trend data
        """
        if not self.pytrends:
            # Simulate trend data if pytrends is not available
            return self._simulate_trend_data(keywords)
        
        try:
            logger.info(f"Fetching Google Trends data for: {keywords}")
            
            # Build payload
            self.pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')
            
            # Get interest over time
            interest_over_time = self.pytrends.interest_over_time()
            
            # Get related queries
            related_queries = self.pytrends.related_queries()
            
            # Get regional interest
            interest_by_region = self.pytrends.interest_by_region()
            
            # Process data
            trend_data = {}
            
            for keyword in keywords:
                if keyword in interest_over_time.columns:
                    trend_data[keyword] = {
                        'keyword': keyword,
                        'timeline': interest_over_time[keyword].tolist(),
                        'dates': interest_over_time.index.strftime('%Y-%m-%d').tolist(),
                        'average_interest': interest_over_time[keyword].mean(),
                        'peak_interest': interest_over_time[keyword].max(),
                        'current_interest': interest_over_time[keyword].iloc[-1] if len(interest_over_time) > 0 else 0,
                        'growth_rate': self._calculate_growth_rate(interest_over_time[keyword]),
                        'related_queries': self._process_related_queries(related_queries, keyword),
                        'regional_interest': self._process_regional_interest(interest_by_region, keyword),
                        'fetched_date': datetime.utcnow()
                    }
            
            logger.info(f"Successfully fetched trend data for {len(trend_data)} keywords")
            return trend_data
            
        except Exception as e:
            logger.error(f"Failed to fetch Google Trends data: {e}")
            return self._simulate_trend_data(keywords)
    
    def _simulate_trend_data(self, keywords: List[str]) -> Dict[str, Any]:
        """Simulate trend data when API is not available"""
        import random
        
        trend_data = {}
        for keyword in keywords:
            trend_data[keyword] = {
                'keyword': keyword,
                'timeline': [random.randint(10, 100) for _ in range(7)],
                'dates': [(datetime.utcnow() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)],
                'average_interest': random.uniform(20, 80),
                'peak_interest': random.uniform(60, 100),
                'current_interest': random.uniform(10, 90),
                'growth_rate': random.uniform(-20, 50),
                'related_queries': [f"{keyword} analysis", f"{keyword} market", f"{keyword} trends"],
                'regional_interest': {'United States': random.randint(20, 100)},
                'fetched_date': datetime.utcnow(),
                'simulated': True
            }
        
        return trend_data
    
    def _calculate_growth_rate(self, series) -> float:
        """Calculate growth rate from time series data"""
        if len(series) < 2:
            return 0.0
        
        try:
            start_value = series.iloc[0]
            end_value = series.iloc[-1]
            
            if start_value == 0:
                return 0.0
            
            growth_rate = ((end_value - start_value) / start_value) * 100
            return round(growth_rate, 2)
        except:
            return 0.0
    
    def _process_related_queries(self, related_queries: Dict, keyword: str) -> List[str]:
        """Process related queries data"""
        try:
            if keyword in related_queries and related_queries[keyword] is not None:
                top_queries = related_queries[keyword].get('top', [])
                return [query['query'] for query in top_queries[:5]]
        except:
            pass
        return []
    
    def _process_regional_interest(self, interest_by_region: Dict, keyword: str) -> Dict[str, int]:
        """Process regional interest data"""
        try:
            if keyword in interest_by_region.columns:
                return interest_by_region[keyword].head(10).to_dict()
        except:
            pass
        return {}

class MarketDataAPI:
    """
    Fetcher for market data (stock prices, indices, etc.)
    """
    
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY', 'your_alpha_vantage_key_here')
        self.base_url = 'https://www.alphavantage.co/query'
        self.session = requests.Session()
    
    def fetch_stock_data(self, symbol: str, function: str = 'TIME_SERIES_DAILY') -> Dict:
        """
        Fetch stock market data using Alpha Vantage API
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'GOOGL')
            function: API function to call
        
        Returns:
            Dictionary with stock data
        """
        try:
            params = {
                'function': function,
                'symbol': symbol,
                'outputsize': 'compact',
                'apikey': self.alpha_vantage_key
            }
            
            logger.info(f"Fetching stock data for {symbol}")
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API error messages
            if 'Error Message' in data:
                logger.error(f"Alpha Vantage API error: {data['Error Message']}")
                return {}
            
            if 'Note' in data:
                logger.warning(f"Alpha Vantage API rate limit: {data['Note']}")
                return {}
            
            # Process the time series data
            time_series_key = None
            for key in data.keys():
                if 'Time Series' in key:
                    time_series_key = key
                    break
            
            if not time_series_key:
                logger.error("No time series data found in API response")
                return {}
            
            time_series = data[time_series_key]
            processed_data = {
                'symbol': symbol,
                'metadata': data.get('Meta Data', {}),
                'prices': [],
                'latest_price': None,
                'price_change': None,
                'volume': 0,
                'fetched_date': datetime.utcnow()
            }
            
            # Process the last 30 days of data
            dates = sorted(time_series.keys(), reverse=True)[:30]
            
            for i, date in enumerate(dates):
                price_data = time_series[date]
                price_info = {
                    'date': date,
                    'open': float(price_data['1. open']),
                    'high': float(price_data['2. high']),
                    'low': float(price_data['3. low']),
                    'close': float(price_data['4. close']),
                    'volume': int(price_data['5. volume'])
                }
                processed_data['prices'].append(price_info)
                
                if i == 0:
                    processed_data['latest_price'] = price_info['close']
                elif i == 1:
                    # Calculate price change
                    previous_close = price_info['close']
                    if processed_data['latest_price'] and previous_close:
                        change = processed_data['latest_price'] - previous_close
                        change_percent = (change / previous_close) * 100
                        processed_data['price_change'] = {
                            'absolute': round(change, 2),
                            'percentage': round(change_percent, 2)
                        }
            
            # Calculate average volume
            if processed_data['prices']:
                processed_data['volume'] = sum(p['volume'] for p in processed_data['prices']) // len(processed_data['prices'])
            
            logger.info(f"Successfully fetched stock data for {symbol}")
            return processed_data
            
        except Exception as e:
            logger.error(f"Failed to fetch stock data for {symbol}: {e}")
            return {}
    
    def fetch_market_indices(self) -> Dict[str, Dict]:
        """Fetch major market indices"""
        indices = {
            'S&P 500': '^GSPC',
            'Dow Jones': '^DJI',
            'NASDAQ': '^IXIC',
            'FTSE': '^FTSE',
            'DAX': '^DAX'
        }
        
        indices_data = {}
        for name, symbol in indices.items():
            try:
                data = self.fetch_stock_data(symbol)
                if data:
                    indices_data[name] = data
                time.sleep(1)  # Rate limiting
            except Exception as e:
                logger.error(f"Failed to fetch data for {name}: {e}")
        
        return indices_data

class SocialMediaAPI:
    """
    Fetcher for social media data and sentiment
    Note: This is a placeholder implementation
    """
    
    def __init__(self):
        self.twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN', 'your_twitter_token_here')
    
    def fetch_twitter_sentiment(self, query: str, max_tweets: int = 100) -> List[Dict]:
        """
        Fetch Twitter data for sentiment analysis
        Note: This requires Twitter API v2 access
        
        Args:
            query: Search query
            max_tweets: Maximum number of tweets to fetch
        
        Returns:
            List of tweet data
        """
        # This is a placeholder implementation
        # In production, you would use the official Twitter API
        
        logger.warning("Twitter API integration is a placeholder. Use official Twitter API for production.")
        
        # Simulate tweet data
        import random
        
        sentiments = ['positive', 'negative', 'neutral']
        tweets = []
        
        for i in range(min(max_tweets, 20)):  # Limit to 20 for simulation
            tweet = {
                'id': f"tweet_{i}_{random.randint(1000, 9999)}",
                'text': f"This is a sample tweet about {query}. {'Great' if random.random() > 0.5 else 'Concerning'} market conditions.",
                'author': f"user_{random.randint(100, 999)}",
                'created_at': (datetime.utcnow() - timedelta(hours=random.randint(0, 24))).isoformat(),
                'retweet_count': random.randint(0, 100),
                'like_count': random.randint(0, 500),
                'sentiment': random.choice(sentiments),
                'confidence': random.uniform(0.6, 1.0)
            }
            tweets.append(tweet)
        
        logger.info(f"Simulated {len(tweets)} tweets for query: {query}")
        return tweets

# Data collection manager
class DataCollectionManager:
    """
    Main manager for coordinating all data collection activities
    """
    
    def __init__(self):
        self.news_fetcher = NewsAPIFetcher()
        self.trends_fetcher = GoogleTrendsAPI()
        self.market_fetcher = MarketDataAPI()
        self.social_fetcher = SocialMediaAPI()
    
    def collect_all_data(self, keywords: List[str] = None) -> Dict[str, Any]:
        """
        Collect all types of market intelligence data
        
        Args:
            keywords: Keywords for trend analysis
        
        Returns:
            Dictionary containing all collected data
        """
        if keywords is None:
            keywords = ['market', 'stock', 'economy', 'investment']
        
        logger.info("Starting comprehensive data collection")
        
        collected_data = {
            'collection_timestamp': datetime.utcnow(),
            'news_data': [],
            'trend_data': {},
            'market_data': {},
            'social_data': []
        }
        
        try:
            # Collect news data
            logger.info("Collecting news data...")
            collected_data['news_data'] = self.news_fetcher.fetch_market_news()
            
            # Collect trend data
            logger.info("Collecting trend data...")
            collected_data['trend_data'] = self.trends_fetcher.fetch_trend_data(keywords)
            
            # Collect market data
            logger.info("Collecting market indices data...")
            collected_data['market_data'] = self.market_fetcher.fetch_market_indices()
            
            # Collect social media data
            logger.info("Collecting social media data...")
            for keyword in keywords[:3]:  # Limit to first 3 keywords
                tweets = self.social_fetcher.fetch_twitter_sentiment(keyword)
                collected_data['social_data'].extend(tweets)
            
            logger.info("Data collection completed successfully")
            return collected_data
            
        except Exception as e:
            logger.error(f"Error during data collection: {e}")
            return collected_data
    
    def collect_news_only(self) -> List[Dict]:
        """Collect only news data"""
        return self.news_fetcher.fetch_market_news()
    
    def collect_trends_only(self, keywords: List[str]) -> Dict[str, Any]:
        """Collect only trend data"""
        return self.trends_fetcher.fetch_trend_data(keywords)

# Example usage
if __name__ == "__main__":
    # Initialize data collection manager
    manager = DataCollectionManager()
    
    # Test news collection
    print("Testing news collection...")
    news = manager.collect_news_only()
    print(f"Fetched {len(news)} news articles")
    
    # Test trend collection
    print("\nTesting trend collection...")
    keywords = ['AI market', 'cryptocurrency']
    trends = manager.collect_trends_only(keywords)
    print(f"Fetched trends for {len(trends)} keywords")
    
    # Test comprehensive collection
    print("\nTesting comprehensive data collection...")
    all_data = manager.collect_all_data(['market', 'technology'])
    print(f"Collected data: {len(all_data['news_data'])} news, {len(all_data['trend_data'])} trends, {len(all_data['market_data'])} market indices")

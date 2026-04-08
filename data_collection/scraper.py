"""
Web Scraper Module for Market Data Collection
This module handles web scraping from various news sources and competitor websites
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from typing import List, Dict, Optional
from datetime import datetime
import re
from urllib.parse import urljoin, urlparse
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketScraper:
    """
    Web scraper for collecting market intelligence data
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # List of news sources to scrape
        self.news_sources = {
            'reuters': 'https://www.reuters.com/markets',
            'bloomberg': 'https://www.bloomberg.com/markets',
            'cnbc': 'https://www.cnbc.com/markets/',
            'marketwatch': 'https://www.marketwatch.com/'
        }
        
        # Rate limiting configuration
        self.min_delay = 1  # seconds
        self.max_delay = 3  # seconds
    
    def _delay_between_requests(self):
        """Add random delay between requests to avoid being blocked"""
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\-\!\?\:\;]', '', text)
        return text.strip()
    
    def _extract_article_content(self, url: str) -> Optional[Dict]:
        """Extract full article content from URL"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('h1') or soup.find('title')
            title = self._clean_text(title_tag.get_text() if title_tag else "")
            
            # Extract content (try different selectors)
            content_selectors = [
                'article p',
                '.article-body p',
                '.story-content p',
                '.post-content p',
                '.entry-content p',
                'main p'
            ]
            
            content_parts = []
            for selector in content_selectors:
                paragraphs = soup.select(selector)
                if paragraphs:
                    content_parts = [self._clean_text(p.get_text()) for p in paragraphs if p.get_text().strip()]
                    break
            
            content = ' '.join(content_parts[:10])  # Limit to first 10 paragraphs
            
            # Extract publication date
            date_selectors = [
                'time[datetime]',
                '.date',
                '.published',
                '.timestamp',
                '[data-date]'
            ]
            
            published_date = None
            for selector in date_selectors:
                date_element = soup.select_one(selector)
                if date_element:
                    date_str = date_element.get('datetime') or date_element.get('data-date') or date_element.get_text()
                    published_date = self._parse_date(date_str)
                    break
            
            return {
                'title': title,
                'content': content,
                'url': url,
                'published_date': published_date
            }
            
        except Exception as e:
            logger.error(f"Failed to extract content from {url}: {e}")
            return None
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string into datetime object"""
        try:
            # Try different date formats
            date_formats = [
                '%Y-%m-%dT%H:%M:%S.%fZ',
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%B %d, %Y',
                '%b %d, %Y'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str.strip(), fmt)
                except ValueError:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def scrape_news_headlines(self, source: str = 'reuters', max_articles: int = 10) -> List[Dict]:
        """
        Scrape news headlines from specified source
        
        Args:
            source: News source name ('reuters', 'bloomberg', 'cnbc', 'marketwatch')
            max_articles: Maximum number of articles to scrape
        
        Returns:
            List of dictionaries containing article data
        """
        if source not in self.news_sources:
            logger.error(f"Unknown news source: {source}")
            return []
        
        base_url = self.news_sources[source]
        articles = []
        
        try:
            logger.info(f"Scraping news from {source}")
            response = self.session.get(base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Different selectors for different news sources
            if source == 'reuters':
                article_links = soup.select('a[data-testid="Heading"]')
            elif source == 'bloomberg':
                article_links = soup.select('a[data-component="headline"]')
            elif source == 'cnbc':
                article_links = soup.select('.Card-titleContainer a')
            elif source == 'marketwatch':
                article_links = soup.select('.article__headline a')
            else:
                article_links = soup.select('a[href*="/article/"]')
            
            for i, link in enumerate(article_links[:max_articles]):
                if i >= max_articles:
                    break
                
                href = link.get('href')
                if not href:
                    continue
                
                # Build full URL
                article_url = urljoin(base_url, href)
                
                # Extract article content
                article_data = self._extract_article_content(article_url)
                if article_data:
                    article_data['source'] = source
                    article_data['category'] = 'market_news'
                    articles.append(article_data)
                    logger.info(f"Scraped article: {article_data['title'][:50]}...")
                
                self._delay_between_requests()
            
            logger.info(f"Successfully scraped {len(articles)} articles from {source}")
            return articles
            
        except Exception as e:
            logger.error(f"Failed to scrape {source}: {e}")
            return []
    
    def scrape_competitor_data(self, competitor_url: str, competitor_name: str) -> Dict:
        """
        Scrape competitor data from their website
        
        Args:
            competitor_url: URL of competitor's website
            competitor_name: Name of the competitor
        
        Returns:
            Dictionary containing competitor intelligence
        """
        try:
            logger.info(f"Scraping competitor data for {competitor_name}")
            response = self.session.get(competitor_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract pricing information
            price_patterns = [
                r'\$\d+(?:\.\d{2})?',
                r'(\d+(?:\.\d{2})?)\s*(?:USD|dollars?)',
                r'Price[:\s]*\$?\d+(?:\.\d{2})?'
            ]
            
            prices = []
            for pattern in price_patterns:
                matches = re.findall(pattern, soup.get_text(), re.IGNORECASE)
                prices.extend(matches)
            
            # Extract product information
            product_keywords = ['product', 'service', 'solution', 'offering']
            product_info = []
            
            for keyword in product_keywords:
                elements = soup.find_all(text=re.compile(keyword, re.IGNORECASE))
                for element in elements[:5]:  # Limit to first 5 matches
                    product_info.append(self._clean_text(str(element)))
            
            # Extract recent news or announcements
            news_selectors = [
                '.news',
                '.announcement',
                '.press-release',
                '.blog',
                '.updates'
            ]
            
            news_items = []
            for selector in news_selectors:
                elements = soup.select(selector)
                if elements:
                    for element in elements[:3]:
                        text = self._clean_text(element.get_text())
                        if text:
                            news_items.append(text)
                    break
            
            return {
                'competitor_name': competitor_name,
                'url': competitor_url,
                'prices': prices[:5],  # Limit to first 5 prices
                'product_info': product_info,
                'news_items': news_items,
                'scraped_date': datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Failed to scrape competitor data for {competitor_name}: {e}")
            return {
                'competitor_name': competitor_name,
                'url': competitor_url,
                'error': str(e),
                'scraped_date': datetime.utcnow()
            }
    
    def scrape_social_media_sentiment(self, keyword: str, platform: str = 'twitter') -> List[Dict]:
        """
        Scrape social media data for sentiment analysis
        Note: This is a placeholder implementation. In production, you would use official APIs
        
        Args:
            keyword: Keyword to search for
            platform: Social media platform
        
        Returns:
            List of social media posts
        """
        # This is a placeholder - in production, use official APIs
        logger.warning("Social media scraping is a placeholder. Use official APIs for production.")
        
        # Simulate social media data
        sample_posts = [
            {
                'platform': platform,
                'content': f"Great news about {keyword}! The market looks promising.",
                'author': 'market_analyst1',
                'timestamp': datetime.utcnow(),
                'engagement': random.randint(10, 1000)
            },
            {
                'platform': platform,
                'content': f"Concerned about {keyword} market volatility. Need to watch carefully.",
                'author': 'investor_pro',
                'timestamp': datetime.utcnow(),
                'engagement': random.randint(5, 500)
            }
        ]
        
        return sample_posts
    
    def scrape_market_trends(self, keywords: List[str]) -> Dict[str, Dict]:
        """
        Scrape market trends for specified keywords
        
        Args:
            keywords: List of keywords to search for
        
        Returns:
            Dictionary with trend data for each keyword
        """
        trends_data = {}
        
        for keyword in keywords:
            try:
                # This is a placeholder - in production, use Google Trends API or similar
                logger.info(f"Scraping trends for keyword: {keyword}")
                
                # Simulate trend data
                trends_data[keyword] = {
                    'keyword': keyword,
                    'trend_score': random.uniform(0, 100),
                    'volume': random.randint(1000, 100000),
                    'growth_rate': random.uniform(-50, 200),
                    'related_keywords': [f"{keyword} analysis", f"{keyword} market", f"{keyword} trends"],
                    'scraped_date': datetime.utcnow()
                }
                
                self._delay_between_requests()
                
            except Exception as e:
                logger.error(f"Failed to scrape trends for {keyword}: {e}")
                trends_data[keyword] = {'error': str(e)}
        
        return trends_data

class CompetitorMonitor:
    """
    Specialized class for monitoring competitor activities
    """
    
    def __init__(self):
        self.scraper = MarketScraper()
        
        # List of competitors to monitor
        self.competitors = {
            'competitor1': 'https://example-competitor1.com',
            'competitor2': 'https://example-competitor2.com',
            # Add actual competitor URLs
        }
    
    def monitor_all_competitors(self) -> List[Dict]:
        """Monitor all configured competitors"""
        competitor_data = []
        
        for name, url in self.competitors.items():
            try:
                data = self.scraper.scrape_competitor_data(url, name)
                competitor_data.append(data)
                logger.info(f"Monitored competitor: {name}")
            except Exception as e:
                logger.error(f"Failed to monitor {name}: {e}")
        
        return competitor_data
    
    def add_competitor(self, name: str, url: str):
        """Add a new competitor to monitor"""
        self.competitors[name] = url
        logger.info(f"Added competitor: {name} -> {url}")
    
    def remove_competitor(self, name: str):
        """Remove a competitor from monitoring"""
        if name in self.competitors:
            del self.competitors[name]
            logger.info(f"Removed competitor: {name}")

# Example usage and testing
if __name__ == "__main__":
    # Initialize scraper
    scraper = MarketScraper()
    
    # Test news scraping
    print("Testing news scraping...")
    articles = scraper.scrape_news_headlines('reuters', max_articles=3)
    for article in articles:
        print(f"Title: {article['title'][:50]}...")
    
    # Test trend scraping
    print("\nTesting trend scraping...")
    keywords = ['AI market', 'cryptocurrency', 'stock market']
    trends = scraper.scrape_market_trends(keywords)
    for keyword, data in trends.items():
        print(f"{keyword}: {data.get('trend_score', 'N/A')}")
    
    # Test competitor monitoring
    print("\nTesting competitor monitoring...")
    monitor = CompetitorMonitor()
    competitor_data = monitor.monitor_all_competitors()
    print(f"Monitored {len(competitor_data)} competitors")

"""
Sentiment Analysis Module
This module handles sentiment analysis of market news, social media, and text data
"""

import re
import logging
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import numpy as np
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('corpora/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Advanced sentiment analyzer combining multiple approaches
    """
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Market-specific sentiment keywords
        self.positive_market_words = {
            'bullish', 'rally', 'surge', 'growth', 'profit', 'gain', 'increase', 
            'boom', 'expansion', 'recovery', 'strong', 'robust', 'outperform',
            'breakthrough', 'innovation', 'opportunity', 'momentum', 'upward'
        }
        
        self.negative_market_words = {
            'bearish', 'crash', 'decline', 'loss', 'fall', 'decrease', 'recession',
            'downturn', 'slump', 'weak', 'poor', 'underperform', 'volatility',
            'risk', 'concern', 'worry', 'fear', 'panic', 'sell-off', 'correction'
        }
        
        self.financial_keywords = {
            'revenue', 'earnings', 'profit', 'margin', 'dividend', 'stock', 'share',
            'market', 'economy', 'inflation', 'interest', 'investment', 'portfolio',
            'trading', 'commodity', 'currency', 'cryptocurrency', 'blockchain'
        }
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for sentiment analysis
        
        Args:
            text: Input text to preprocess
        
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove numbers and special characters, but keep important punctuation
        text = re.sub(r'[^a-zA-Z\s\.\!\?\,\;\:]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract relevant keywords from text
        
        Args:
            text: Input text
        
        Returns:
            List of keywords
        """
        if not text:
            return []
        
        # Tokenize and lemmatize
        tokens = word_tokenize(text.lower())
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words and len(token) > 2]
        
        # Filter for market-relevant keywords
        keywords = []
        for token in tokens:
            if token in self.positive_market_words or token in self.negative_market_words or token in self.financial_keywords:
                keywords.append(token)
        
        return list(set(keywords))
    
    def analyze_sentiment_vader(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using VADER
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with sentiment scores
        """
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            return {
                'compound': scores['compound'],
                'positive': scores['pos'],
                'negative': scores['neg'],
                'neutral': scores['neu']
            }
        except Exception as e:
            logger.error(f"VADER sentiment analysis failed: {e}")
            return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
    
    def analyze_sentiment_textblob(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using TextBlob
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with sentiment scores
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Convert polarity to positive/negative/neutral scores
            if polarity > 0:
                positive = polarity
                negative = 0.0
            elif polarity < 0:
                positive = 0.0
                negative = abs(polarity)
            else:
                positive = 0.0
                negative = 0.0
            
            return {
                'compound': polarity,
                'positive': positive,
                'negative': negative,
                'neutral': 1 - positive - negative,
                'subjectivity': subjectivity
            }
        except Exception as e:
            logger.error(f"TextBlob sentiment analysis failed: {e}")
            return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': 1.0, 'subjectivity': 0.0}
    
    def analyze_market_sentiment(self, text: str) -> Dict[str, float]:
        """
        Custom market sentiment analysis using domain-specific keywords
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with sentiment scores
        """
        try:
            preprocessed_text = self.preprocess_text(text)
            tokens = word_tokenize(preprocessed_text)
            
            positive_count = sum(1 for token in tokens if token in self.positive_market_words)
            negative_count = sum(1 for token in tokens if token in self.negative_market_words)
            total_tokens = len(tokens)
            
            if total_tokens == 0:
                return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
            
            positive_score = positive_count / total_tokens
            negative_score = negative_count / total_tokens
            neutral_score = 1 - positive_score - negative_score
            
            # Calculate compound score
            compound_score = (positive_score - negative_score) * 10  # Scale to -10 to 10
            compound_score = max(-1, min(1, compound_score / 10))  # Normalize to -1 to 1
            
            return {
                'compound': compound_score,
                'positive': positive_score,
                'negative': negative_score,
                'neutral': neutral_score
            }
        except Exception as e:
            logger.error(f"Market sentiment analysis failed: {e}")
            return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
    
    def analyze_sentiment_ensemble(self, text: str) -> Dict[str, float]:
        """
        Ensemble sentiment analysis combining multiple methods
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with ensemble sentiment scores
        """
        try:
            # Get sentiment from all methods
            vader_scores = self.analyze_sentiment_vader(text)
            textblob_scores = self.analyze_sentiment_textblob(text)
            market_scores = self.analyze_market_sentiment(text)
            
            # Weight the different methods
            # VADER is good for social media and short text
            # TextBlob is good for general text
            # Market-specific analysis is good for financial content
            weights = {
                'vader': 0.4,
                'textblob': 0.3,
                'market': 0.3
            }
            
            # Calculate weighted average
            ensemble_scores = {}
            for metric in ['compound', 'positive', 'negative', 'neutral']:
                ensemble_scores[metric] = (
                    vader_scores[metric] * weights['vader'] +
                    textblob_scores[metric] * weights['textblob'] +
                    market_scores[metric] * weights['market']
                )
            
            # Add additional metadata
            ensemble_scores['confidence'] = self._calculate_confidence(vader_scores, textblob_scores, market_scores)
            ensemble_scores['keywords'] = self.extract_keywords(text)
            ensemble_scores['analysis_method'] = 'ensemble'
            
            return ensemble_scores
            
        except Exception as e:
            logger.error(f"Ensemble sentiment analysis failed: {e}")
            return {'compound': 0.0, 'positive': 0.0, 'negative': 0.0, 'neutral': 1.0, 'confidence': 0.0}
    
    def _calculate_confidence(self, vader_scores: Dict, textblob_scores: Dict, market_scores: Dict) -> float:
        """Calculate confidence score based on agreement between methods"""
        try:
            # Calculate agreement between compound scores
            vader_compound = vader_scores['compound']
            textblob_compound = textblob_scores['compound']
            market_compound = market_scores['compound']
            
            # Calculate standard deviation
            compounds = [vader_compound, textblob_compound, market_compound]
            std_dev = np.std(compounds)
            
            # Convert to confidence (lower std_dev = higher confidence)
            confidence = max(0.0, 1.0 - std_dev)
            
            return round(confidence, 3)
        except:
            return 0.5  # Default confidence
    
    def batch_analyze_sentiment(self, texts: List[str]) -> List[Dict]:
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts: List of texts to analyze
        
        Returns:
            List of sentiment analysis results
        """
        results = []
        
        for i, text in enumerate(texts):
            try:
                logger.info(f"Analyzing sentiment for text {i+1}/{len(texts)}")
                sentiment_result = self.analyze_sentiment_ensemble(text)
                sentiment_result['text_length'] = len(text)
                sentiment_result['analyzed_at'] = datetime.utcnow()
                results.append(sentiment_result)
            except Exception as e:
                logger.error(f"Failed to analyze text {i+1}: {e}")
                results.append({
                    'compound': 0.0,
                    'positive': 0.0,
                    'negative': 0.0,
                    'neutral': 1.0,
                    'confidence': 0.0,
                    'error': str(e)
                })
        
        return results
    
    def get_sentiment_summary(self, sentiment_results: List[Dict]) -> Dict:
        """
        Get summary statistics for sentiment analysis results
        
        Args:
            sentiment_results: List of sentiment analysis results
        
        Returns:
            Dictionary with summary statistics
        """
        if not sentiment_results:
            return {}
        
        try:
            # Extract compound scores
            compound_scores = [result.get('compound', 0) for result in sentiment_results]
            
            # Calculate statistics
            summary = {
                'total_texts': len(sentiment_results),
                'average_sentiment': np.mean(compound_scores),
                'median_sentiment': np.median(compound_scores),
                'sentiment_std': np.std(compound_scores),
                'min_sentiment': np.min(compound_scores),
                'max_sentiment': np.max(compound_scores),
                'positive_count': sum(1 for score in compound_scores if score > 0.1),
                'negative_count': sum(1 for score in compound_scores if score < -0.1),
                'neutral_count': sum(1 for score in compound_scores if -0.1 <= score <= 0.1),
                'average_confidence': np.mean([result.get('confidence', 0) for result in sentiment_results])
            }
            
            # Calculate percentages
            total = len(sentiment_results)
            summary['positive_percentage'] = (summary['positive_count'] / total) * 100
            summary['negative_percentage'] = (summary['negative_count'] / total) * 100
            summary['neutral_percentage'] = (summary['neutral_count'] / total) * 100
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to calculate sentiment summary: {e}")
            return {}

class MarketSentimentAnalyzer:
    """
    Specialized analyzer for market sentiment across different data sources
    """
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
    
    def analyze_news_sentiment(self, news_articles: List[Dict]) -> List[Dict]:
        """
        Analyze sentiment for news articles
        
        Args:
            news_articles: List of news article dictionaries
        
        Returns:
            List of articles with sentiment analysis
        """
        analyzed_articles = []
        
        for article in news_articles:
            try:
                # Combine title and content for analysis
                text_to_analyze = f"{article.get('title', '')} {article.get('content', '')}"
                
                # Perform sentiment analysis
                sentiment_result = self.sentiment_analyzer.analyze_sentiment_ensemble(text_to_analyze)
                
                # Add sentiment data to article
                article_with_sentiment = article.copy()
                article_with_sentiment['sentiment'] = sentiment_result
                article_with_sentiment['sentiment_analyzed_at'] = datetime.utcnow()
                
                analyzed_articles.append(article_with_sentiment)
                
            except Exception as e:
                logger.error(f"Failed to analyze article sentiment: {e}")
                article['sentiment'] = {'error': str(e)}
                analyzed_articles.append(article)
        
        return analyzed_articles
    
    def analyze_social_sentiment(self, social_posts: List[Dict]) -> List[Dict]:
        """
        Analyze sentiment for social media posts
        
        Args:
            social_posts: List of social media post dictionaries
        
        Returns:
            List of posts with sentiment analysis
        """
        analyzed_posts = []
        
        for post in social_posts:
            try:
                text_to_analyze = post.get('content', post.get('text', ''))
                
                # Perform sentiment analysis
                sentiment_result = self.sentiment_analyzer.analyze_sentiment_ensemble(text_to_analyze)
                
                # Add sentiment data to post
                post_with_sentiment = post.copy()
                post_with_sentiment['sentiment'] = sentiment_result
                post_with_sentiment['sentiment_analyzed_at'] = datetime.utcnow()
                
                analyzed_posts.append(post_with_sentiment)
                
            except Exception as e:
                logger.error(f"Failed to analyze post sentiment: {e}")
                post['sentiment'] = {'error': str(e)}
                analyzed_posts.append(post)
        
        return analyzed_posts
    
    def get_market_sentiment_trend(self, sentiment_data: List[Dict], time_window: str = 'daily') -> Dict:
        """
        Analyze sentiment trends over time
        
        Args:
            sentiment_data: List of sentiment analysis results with timestamps
            time_window: Time window for aggregation ('hourly', 'daily', 'weekly')
        
        Returns:
            Dictionary with sentiment trend data
        """
        try:
            if not sentiment_data:
                return {}
            
            # Convert to DataFrame for easier analysis
            df = pd.DataFrame(sentiment_data)
            
            # Ensure timestamp column exists
            timestamp_col = 'sentiment_analyzed_at'
            if timestamp_col not in df.columns:
                timestamp_col = 'created_at'
            
            if timestamp_col not in df.columns:
                return {}
            
            # Convert timestamps
            df[timestamp_col] = pd.to_datetime(df[timestamp_col])
            
            # Extract compound scores
            df['compound'] = df['sentiment'].apply(lambda x: x.get('compound', 0) if isinstance(x, dict) else 0)
            
            # Group by time window
            if time_window == 'hourly':
                df['time_group'] = df[timestamp_col].dt.floor('H')
            elif time_window == 'weekly':
                df['time_group'] = df[timestamp_col].dt.floor('W')
            else:  # daily
                df['time_group'] = df[timestamp_col].dt.floor('D')
            
            # Calculate aggregate sentiment per time period
            trend_data = df.groupby('time_group').agg({
                'compound': ['mean', 'std', 'count'],
                'sentiment': lambda x: np.mean([s.get('confidence', 0) for s in x if isinstance(s, dict)])
            }).round(3)
            
            # Flatten column names
            trend_data.columns = ['avg_sentiment', 'sentiment_std', 'post_count', 'avg_confidence']
            
            # Convert to dictionary format
            trend_dict = {
                'time_window': time_window,
                'data_points': len(trend_data),
                'trend': trend_data.to_dict('index'),
                'overall_trend': self._calculate_overall_trend(trend_data['avg_sentiment'].tolist()),
                'volatility': trend_data['sentiment_std'].mean(),
                'generated_at': datetime.utcnow()
            }
            
            return trend_dict
            
        except Exception as e:
            logger.error(f"Failed to analyze sentiment trend: {e}")
            return {}
    
    def _calculate_overall_trend(self, sentiment_values: List[float]) -> str:
        """Calculate overall trend direction"""
        try:
            if len(sentiment_values) < 2:
                return 'insufficient_data'
            
            # Calculate linear trend
            x = list(range(len(sentiment_values)))
            slope = np.polyfit(x, sentiment_values, 1)[0]
            
            if slope > 0.01:
                return 'improving'
            elif slope < -0.01:
                return 'declining'
            else:
                return 'stable'
        except:
            return 'unknown'

# Example usage
if __name__ == "__main__":
    # Initialize sentiment analyzer
    analyzer = SentimentAnalyzer()
    
    # Test sentiment analysis
    test_texts = [
        "The stock market is showing strong growth with bullish sentiment among investors.",
        "Concerns about recession are growing as economic indicators show decline.",
        "The company reported mixed earnings with revenue growth but profit margin pressure.",
        "Cryptocurrency markets remain volatile with Bitcoin experiencing significant fluctuations."
    ]
    
    print("Testing sentiment analysis...")
    for i, text in enumerate(test_texts):
        result = analyzer.analyze_sentiment_ensemble(text)
        print(f"\nText {i+1}: {text[:50]}...")
        print(f"Sentiment: {result['compound']:.3f} (Positive: {result['positive']:.3f}, Negative: {result['negative']:.3f})")
        print(f"Confidence: {result['confidence']:.3f}")
        print(f"Keywords: {result['keywords']}")
    
    # Test batch analysis
    print("\n\nTesting batch sentiment analysis...")
    batch_results = analyzer.batch_analyze_sentiment(test_texts)
    summary = analyzer.get_sentiment_summary(batch_results)
    print(f"Average sentiment: {summary['average_sentiment']:.3f}")
    print(f"Positive: {summary['positive_percentage']:.1f}%, Negative: {summary['negative_percentage']:.1f}%")

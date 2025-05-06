import os
import json
import time
from datetime import datetime, timedelta
import requests
import feedparser
import yfinance as yf
from bs4 import BeautifulSoup
from sec_api import QueryApi
from dotenv import load_dotenv

load_dotenv()

class DataIngestion:
    def __init__(self):
        self.fmp_api_key = os.getenv('FMP_API_KEY')
        self.sec_api_key = os.getenv('SEC_API_KEY')
        self.base_url = "https://financialmodelingprep.com/api/v3"
        
    def fetch_sec_filings(self, ticker):
        """Fetch recent SEC filings for a given ticker."""
        query = {
            "query": {
                "query_string": {
                    "query": f"ticker:{ticker} AND formType:(10-K OR 10-Q OR 8-K)"
                }
            },
            "from": "0",
            "size": "10",
            "sort": [{"filedAt": {"order": "desc"}}]
        }
        
        sec_api = QueryApi(api_key=self.sec_api_key)
        try:
            response = sec_api.get_filings(query)
            return response['filings']
        except Exception as e:
            print(f"Error fetching SEC filings for {ticker}: {e}")
            return []

    def fetch_news_feeds(self, ticker):
        """Fetch news from various RSS feeds for a given ticker."""
        feeds = [
            f"https://seekingalpha.com/feed.xml?symbol={ticker}",
            f"https://www.marketwatch.com/rss/stock/{ticker}",
            f"https://www.benzinga.com/feed/{ticker}"
        ]
        
        news_items = []
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    news_items.append({
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.published,
                        'source': feed_url
                    })
            except Exception as e:
                print(f"Error fetching news from {feed_url}: {e}")
        
        return news_items

    def fetch_forum_sentiment(self, ticker):
        """Fetch sentiment data from stock market forums."""
        # Example implementation using Reddit API
        headers = {'User-Agent': 'Mozilla/5.0'}
        subreddits = ['stocks', 'investing', 'wallstreetbets']
        sentiment_data = []
        
        for subreddit in subreddits:
            url = f"https://www.reddit.com/r/{subreddit}/search.json?q={ticker}&restrict_sr=1&sort=relevance&t=week"
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    for post in data['data']['children']:
                        sentiment_data.append({
                            'title': post['data']['title'],
                            'score': post['data']['score'],
                            'num_comments': post['data']['num_comments'],
                            'created_utc': post['data']['created_utc'],
                            'subreddit': subreddit
                        })
            except Exception as e:
                print(f"Error fetching forum data from {subreddit}: {e}")
        
        return sentiment_data

    def fetch_market_data(self, ticker):
        """Fetch comprehensive market data for a ticker."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get historical data
            hist = stock.history(period="1mo")
            
            # Calculate additional metrics
            market_data = {
                'current_price': info.get('currentPrice'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'forward_pe': info.get('forwardPE'),
                'dividend_yield': info.get('dividendYield'),
                'beta': info.get('beta'),
                'volume': info.get('volume'),
                'avg_volume': info.get('averageVolume'),
                'price_change_1d': hist['Close'].pct_change().iloc[-1] if not hist.empty else None,
                'price_change_1w': hist['Close'].pct_change(5).iloc[-1] if len(hist) >= 5 else None,
                'price_change_1m': hist['Close'].pct_change(20).iloc[-1] if len(hist) >= 20 else None
            }
            
            return market_data
        except Exception as e:
            print(f"Error fetching market data for {ticker}: {e}")
            return {}

    def fetch_ai_metrics(self, ticker):
        """Fetch AI-specific metrics for a company."""
        url = f"{self.base_url}/key-metrics/{ticker}?limit=1&apikey={self.fmp_api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()[0]
                return {
                    'rd_expense': data.get('researchAndDevelopmentExpenses'),
                    'rd_to_revenue': data.get('researchAndDevelopmentExpenses') / data.get('revenue') if data.get('revenue') else None,
                    'patent_count': self._fetch_patent_count(ticker),
                    'ai_mentions': self._count_ai_mentions(ticker)
                }
        except Exception as e:
            print(f"Error fetching AI metrics for {ticker}: {e}")
        return {}

    def _fetch_patent_count(self, ticker):
        """Helper method to fetch patent count (placeholder implementation)."""
        # This would typically involve querying a patent database
        return None

    def _count_ai_mentions(self, ticker):
        """Helper method to count AI-related mentions in recent filings."""
        filings = self.fetch_sec_filings(ticker)
        ai_keywords = ['artificial intelligence', 'machine learning', 'deep learning', 'neural network']
        mention_count = 0
        
        for filing in filings:
            try:
                # This is a placeholder - actual implementation would need to fetch and parse filing text
                mention_count += 1
            except Exception as e:
                print(f"Error processing filing for {ticker}: {e}")
        
        return mention_count

    def collect_all_data(self, ticker):
        """Collect all available data for a given ticker."""
        return {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'market_data': self.fetch_market_data(ticker),
            'sec_filings': self.fetch_sec_filings(ticker),
            'news': self.fetch_news_feeds(ticker),
            'forum_sentiment': self.fetch_forum_sentiment(ticker),
            'ai_metrics': self.fetch_ai_metrics(ticker)
        } 
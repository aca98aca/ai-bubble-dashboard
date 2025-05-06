import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_CONFIG = {
    'fmp_api_key': os.getenv('FMP_API_KEY'),
    'sec_api_key': os.getenv('SEC_API_KEY'),
    'reddit_client_id': os.getenv('REDDIT_CLIENT_ID'),
    'reddit_client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
    'reddit_user_agent': os.getenv('REDDIT_USER_AGENT')
}

# Data Collection Configuration
DATA_COLLECTION_CONFIG = {
    'update_interval': 5 * 60,  # 5 minutes in seconds
    'max_retries': 3,
    'timeout': 30,
    'cache_duration': 3600  # 1 hour in seconds
}

# News Feed Configuration
NEWS_FEEDS = [
    'https://seekingalpha.com/feed.xml',
    'https://www.marketwatch.com/rss',
    'https://www.benzinga.com/feed'
]

# Forum Configuration
FORUM_CONFIG = {
    'subreddits': ['stocks', 'investing', 'wallstreetbets'],
    'max_posts': 100,
    'time_filter': 'week'
}

# AI Keywords for Classification
AI_KEYWORDS = [
    'artificial intelligence',
    'machine learning',
    'deep learning',
    'neural network',
    'natural language processing',
    'computer vision',
    'robotics',
    'automation',
    'predictive analytics',
    'data science'
]

# Risk Scoring Configuration
RISK_SCORING_CONFIG = {
    'weights': {
        'valuation_metrics': 0.3,
        'sentiment_metrics': 0.2,
        'growth_metrics': 0.2,
        'ai_exposure': 0.15,
        'market_metrics': 0.15
    },
    'thresholds': {
        'extreme_risk': 0.8,
        'high_risk': 0.6,
        'moderate_risk': 0.4,
        'low_risk': 0.2
    }
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    'title': 'AI Bubble Dashboard',
    'description': 'Track potential speculative bubbles in the AI sector',
    'theme': 'bootstrap',
    'refresh_interval': 5 * 60 * 1000  # 5 minutes in milliseconds
}

# File Paths
PATHS = {
    'data_dir': 'data',
    'config_dir': 'config',
    'log_file': 'data/app.log',
    'tickers_file': 'config/tickers.json'
}

# Create necessary directories
for directory in [PATHS['data_dir'], PATHS['config_dir']]:
    if not os.path.exists(directory):
        os.makedirs(directory) 
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta

class BubbleScorer:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.weights = {
            'valuation_metrics': 0.3,
            'sentiment_metrics': 0.2,
            'growth_metrics': 0.2,
            'ai_exposure': 0.15,
            'market_metrics': 0.15
        }

    def calculate_valuation_score(self, market_data):
        """Calculate valuation-based risk score."""
        scores = []
        
        # P/E Ratio Score
        if market_data.get('pe_ratio'):
            pe_score = min(market_data['pe_ratio'] / 50, 1)  # Normalize to 0-1, cap at 50
            scores.append(pe_score)
        
        # Forward P/E Score
        if market_data.get('forward_pe'):
            forward_pe_score = min(market_data['forward_pe'] / 40, 1)
            scores.append(forward_pe_score)
        
        # Price to Sales Score (if available)
        if market_data.get('price_to_sales'):
            ps_score = min(market_data['price_to_sales'] / 20, 1)
            scores.append(ps_score)
        
        return np.mean(scores) if scores else 0.5

    def calculate_sentiment_score(self, news_data, forum_data):
        """Calculate sentiment-based risk score."""
        scores = []
        
        # News Volume Score
        news_volume = len(news_data)
        if news_volume > 0:
            news_volume_score = min(news_volume / 50, 1)  # Normalize to 0-1, cap at 50 articles
            scores.append(news_volume_score)
        
        # Forum Activity Score
        if forum_data:
            total_comments = sum(post['num_comments'] for post in forum_data)
            comment_score = min(total_comments / 1000, 1)  # Normalize to 0-1, cap at 1000 comments
            scores.append(comment_score)
            
            # Post Score
            avg_score = np.mean([post['score'] for post in forum_data])
            post_score = min(avg_score / 1000, 1)  # Normalize to 0-1, cap at 1000 score
            scores.append(post_score)
        
        return np.mean(scores) if scores else 0.5

    def calculate_growth_score(self, market_data, ai_metrics):
        """Calculate growth-based risk score."""
        scores = []
        
        # Price Change Score
        if market_data.get('price_change_1m'):
            price_change = abs(market_data['price_change_1m'])
            price_score = min(price_change / 0.5, 1)  # Normalize to 0-1, cap at 50% change
            scores.append(price_score)
        
        # R&D to Revenue Score
        if ai_metrics.get('rd_to_revenue'):
            rd_score = min(ai_metrics['rd_to_revenue'] / 0.3, 1)  # Normalize to 0-1, cap at 30%
            scores.append(rd_score)
        
        return np.mean(scores) if scores else 0.5

    def calculate_ai_exposure_score(self, ai_metrics):
        """Calculate AI exposure risk score."""
        scores = []
        
        # R&D Expense Score
        if ai_metrics.get('rd_expense'):
            rd_score = min(ai_metrics['rd_expense'] / 1e9, 1)  # Normalize to 0-1, cap at $1B
            scores.append(rd_score)
        
        # AI Mentions Score
        if ai_metrics.get('ai_mentions'):
            mention_score = min(ai_metrics['ai_mentions'] / 20, 1)  # Normalize to 0-1, cap at 20 mentions
            scores.append(mention_score)
        
        # Patent Count Score
        if ai_metrics.get('patent_count'):
            patent_score = min(ai_metrics['patent_count'] / 100, 1)  # Normalize to 0-1, cap at 100 patents
            scores.append(patent_score)
        
        return np.mean(scores) if scores else 0.5

    def calculate_market_score(self, market_data):
        """Calculate market-based risk score."""
        scores = []
        
        # Volume Score
        if market_data.get('volume') and market_data.get('avg_volume'):
            volume_ratio = market_data['volume'] / market_data['avg_volume']
            volume_score = min(volume_ratio / 3, 1)  # Normalize to 0-1, cap at 3x average
            scores.append(volume_score)
        
        # Beta Score
        if market_data.get('beta'):
            beta_score = min(market_data['beta'] / 2, 1)  # Normalize to 0-1, cap at beta of 2
            scores.append(beta_score)
        
        return np.mean(scores) if scores else 0.5

    def calculate_bubble_risk(self, data):
        """Calculate overall bubble risk score."""
        market_data = data.get('market_data', {})
        ai_metrics = data.get('ai_metrics', {})
        news_data = data.get('news', [])
        forum_data = data.get('forum_sentiment', [])
        
        # Calculate individual component scores
        valuation_score = self.calculate_valuation_score(market_data)
        sentiment_score = self.calculate_sentiment_score(news_data, forum_data)
        growth_score = self.calculate_growth_score(market_data, ai_metrics)
        ai_exposure_score = self.calculate_ai_exposure_score(ai_metrics)
        market_score = self.calculate_market_score(market_data)
        
        # Calculate weighted average
        bubble_risk = (
            self.weights['valuation_metrics'] * valuation_score +
            self.weights['sentiment_metrics'] * sentiment_score +
            self.weights['growth_metrics'] * growth_score +
            self.weights['ai_exposure'] * ai_exposure_score +
            self.weights['market_metrics'] * market_score
        )
        
        return {
            'bubble_risk': bubble_risk,
            'component_scores': {
                'valuation_score': valuation_score,
                'sentiment_score': sentiment_score,
                'growth_score': growth_score,
                'ai_exposure_score': ai_exposure_score,
                'market_score': market_score
            }
        }

    def get_risk_level(self, bubble_risk):
        """Convert bubble risk score to risk level."""
        if bubble_risk >= 0.8:
            return "Extreme Risk"
        elif bubble_risk >= 0.6:
            return "High Risk"
        elif bubble_risk >= 0.4:
            return "Moderate Risk"
        elif bubble_risk >= 0.2:
            return "Low Risk"
        else:
            return "Minimal Risk" 
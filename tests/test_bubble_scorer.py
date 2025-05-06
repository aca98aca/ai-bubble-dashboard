import unittest
from datetime import datetime
from src.analysis.bubble_scorer import BubbleScorer

class TestBubbleScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = BubbleScorer()
        self.sample_data = {
            'market_data': {
                'pe_ratio': 30,
                'forward_pe': 25,
                'price_to_sales': 10,
                'current_price': 100,
                'volume': 1000000,
                'avg_volume': 500000,
                'beta': 1.5,
                'price_change_1m': 0.2
            },
            'ai_metrics': {
                'rd_expense': 500000000,
                'rd_to_revenue': 0.15,
                'patent_count': 50,
                'ai_mentions': 10
            },
            'news': [
                {'title': 'Test News 1', 'link': 'http://test1.com'},
                {'title': 'Test News 2', 'link': 'http://test2.com'}
            ],
            'forum_sentiment': [
                {
                    'title': 'Test Post 1',
                    'score': 100,
                    'num_comments': 50,
                    'created_utc': datetime.now().timestamp(),
                    'subreddit': 'stocks'
                }
            ]
        }

    def test_calculate_valuation_score(self):
        score = self.scorer.calculate_valuation_score(self.sample_data['market_data'])
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)

    def test_calculate_sentiment_score(self):
        score = self.scorer.calculate_sentiment_score(
            self.sample_data['news'],
            self.sample_data['forum_sentiment']
        )
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)

    def test_calculate_growth_score(self):
        score = self.scorer.calculate_growth_score(
            self.sample_data['market_data'],
            self.sample_data['ai_metrics']
        )
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)

    def test_calculate_ai_exposure_score(self):
        score = self.scorer.calculate_ai_exposure_score(self.sample_data['ai_metrics'])
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)

    def test_calculate_market_score(self):
        score = self.scorer.calculate_market_score(self.sample_data['market_data'])
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)

    def test_calculate_bubble_risk(self):
        result = self.scorer.calculate_bubble_risk(self.sample_data)
        self.assertIn('bubble_risk', result)
        self.assertIn('component_scores', result)
        self.assertGreaterEqual(result['bubble_risk'], 0)
        self.assertLessEqual(result['bubble_risk'], 1)

    def test_get_risk_level(self):
        risk_levels = [
            (0.9, "Extreme Risk"),
            (0.7, "High Risk"),
            (0.5, "Moderate Risk"),
            (0.3, "Low Risk"),
            (0.1, "Minimal Risk")
        ]
        
        for risk, expected_level in risk_levels:
            level = self.scorer.get_risk_level(risk)
            self.assertEqual(level, expected_level)

if __name__ == '__main__':
    unittest.main() 
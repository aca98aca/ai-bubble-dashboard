# AI Bubble Dashboard

A comprehensive financial analytics tool designed to track and analyze potential speculative bubbles in the AI sector. The dashboard integrates various data sources and provides real-time monitoring of AI-related stocks, market sentiment, and bubble risk indicators.

## Features

- Real-time data collection from multiple sources
- Bubble risk scoring system
- Interactive dashboard with visualizations
- Sentiment analysis from news and social media
- Historical pattern analysis
- Sector comparison tools

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aca98aca/ai-bubble-dashboard.git
cd ai-bubble-dashboard
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
FMP_API_KEY=your_fmp_api_key_here
SEC_API_KEY=your_sec_api_key_here
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=your_reddit_user_agent_here
```

## Usage

Run the application:
```bash
python src/main.py
```

Available command-line options:
- `--mode`: Choose between 'dashboard', 'service', or 'both' (default: 'both')
- `--port`: Specify the dashboard port (default: 8050)
- `--debug`: Enable debug mode

Example:
```bash
python src/main.py --mode dashboard --port 8050 --debug
```

## Project Structure

```
ai_bubble_dashboard/
├── data/                  # Data storage
├── src/
│   ├── data_collection/  # Data ingestion modules
│   ├── analysis/         # Analysis and scoring modules
│   ├── visualization/    # Dashboard and visualization
│   └── utils/           # Utility functions
├── tests/               # Test suite
├── config/             # Configuration files
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

## API Keys Required

- Financial Modeling Prep (FMP) API: https://financialmodelingprep.com/developer
- SEC API: https://sec-api.io/
- Reddit API (optional): https://www.reddit.com/dev/api/

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Financial Modeling Prep for financial data
- SEC API for regulatory filings
- Reddit API for sentiment analysis
- Dash and Plotly for visualization 
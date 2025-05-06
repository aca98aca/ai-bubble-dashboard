# AI Bubble Dashboard

A real-time dashboard for monitoring and analyzing potential speculative bubbles in the AI sector. The dashboard provides comprehensive metrics, visualizations, and risk indicators to help investors make informed decisions.

## Features

- Real-time P/S ratio trend analysis
- Correlation matrix visualization
- Market indicators monitoring (VIX, Fed Rate, M2)
- Bubble risk level assessment
- Auto-refreshing data every 5 minutes
- Modern, responsive UI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-bubble-dashboard.git
cd ai-bubble-dashboard
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

## Usage

1. Set up your environment variables in a `.env` file:
```
FMP_API_KEY=your_fmp_api_key
SEC_API_KEY=your_sec_api_key
```

2. Run the dashboard:
```bash
python src/main.py --mode dashboard
```

The dashboard will be available at `http://localhost:8050`

## Project Structure

```
ai-bubble-dashboard/
├── src/
│   ├── analysis/
│   │   └── bubble_analysis.py
│   ├── visualization/
│   │   ├── dashboard.py
│   │   └── bubble_dashboard.py
│   └── utils/
│       ├── config.py
│       └── helpers.py
├── tests/
│   └── test_bubble_analyzer.py
├── setup.py
├── requirements.txt
└── README.md
```

## Required API Keys

- FMP API Key: For financial market data
- SEC API Key: For SEC filings data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Financial Modeling Prep API
- SEC EDGAR API
- Dash and Plotly for visualization 
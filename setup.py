from setuptools import setup, find_packages

setup(
    name="ai_bubble_dashboard",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "yfinance>=0.2.36",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "python-dotenv>=1.0.0",
        "feedparser>=6.0.10",
        "sec-api>=1.0.0",
        "nltk>=3.8.1",
        "plotly>=5.18.0",
        "dash>=2.14.0",
        "dash-bootstrap-components>=1.0.0",
    ],
    python_requires=">=3.8",
) 
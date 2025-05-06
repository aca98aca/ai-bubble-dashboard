import os
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from data_collection.data_ingestion import DataIngestion
from analysis.bubble_scorer import BubbleScorer

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
data_ingestion = DataIngestion()
bubble_scorer = BubbleScorer()

# Load initial tickers
with open('config/tickers.json', 'r') as f:
    tickers = json.load(f)['tickers']

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("AI Bubble Dashboard", className="text-center my-4"),
            html.P("Track potential speculative bubbles in the AI sector", className="text-center")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Add New Ticker", className="card-title"),
                    dbc.Input(id="new-ticker-input", placeholder="Enter ticker symbol", type="text"),
                    dbc.Button("Add Ticker", id="add-ticker-button", color="primary", className="mt-2")
                ])
            ], className="mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Sector Comparison", className="card-title"),
                    dcc.Dropdown(
                        id="sector-dropdown",
                        options=[
                            {"label": "AI", "value": "ai"},
                            {"label": "Biotech", "value": "biotech"},
                            {"label": "Tech", "value": "tech"}
                        ],
                        value="ai"
                    )
                ])
            ], className="mb-4")
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Bubble Risk Overview", className="card-title"),
                    dcc.Graph(id="bubble-risk-gauge")
                ])
            ], className="mb-4")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Component Scores", className="card-title"),
                    dcc.Graph(id="component-scores-radar")
                ])
            ], className="mb-4")
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Price Trends", className="card-title"),
                    dcc.Graph(id="price-trend-chart")
                ])
            ], className="mb-4")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("News Sentiment", className="card-title"),
                    dcc.Graph(id="news-sentiment-chart")
                ])
            ], className="mb-4")
        ])
    ]),
    
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # Update every 5 minutes
        n_intervals=0
    )
], fluid=True)

# Callbacks
@app.callback(
    [Output("bubble-risk-gauge", "figure"),
     Output("component-scores-radar", "figure"),
     Output("price-trend-chart", "figure"),
     Output("news-sentiment-chart", "figure")],
    [Input("interval-component", "n_intervals"),
     Input("sector-dropdown", "value")]
)
def update_charts(n_intervals, sector):
    # Collect data for all tickers
    all_data = []
    for ticker in tickers:
        data = data_ingestion.collect_all_data(ticker)
        risk_scores = bubble_scorer.calculate_bubble_risk(data)
        data.update(risk_scores)
        all_data.append(data)
    
    # Create bubble risk gauge
    avg_risk = sum(d['bubble_risk'] for d in all_data) / len(all_data)
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_risk * 100,
        title={'text': "Average Bubble Risk"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 20], 'color': "lightgray"},
                {'range': [20, 40], 'color': "lightgreen"},
                {'range': [40, 60], 'color': "yellow"},
                {'range': [60, 80], 'color': "orange"},
                {'range': [80, 100], 'color': "red"}
            ]
        }
    ))
    
    # Create component scores radar chart
    component_scores = {
        'Valuation': sum(d['component_scores']['valuation_score'] for d in all_data) / len(all_data),
        'Sentiment': sum(d['component_scores']['sentiment_score'] for d in all_data) / len(all_data),
        'Growth': sum(d['component_scores']['growth_score'] for d in all_data) / len(all_data),
        'AI Exposure': sum(d['component_scores']['ai_exposure_score'] for d in all_data) / len(all_data),
        'Market': sum(d['component_scores']['market_score'] for d in all_data) / len(all_data)
    }
    
    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=list(component_scores.values()),
        theta=list(component_scores.keys()),
        fill='toself',
        name='Sector Average'
    ))
    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        )
    )
    
    # Create price trend chart
    price_data = []
    for data in all_data:
        if 'market_data' in data and 'current_price' in data['market_data']:
            price_data.append({
                'ticker': data['ticker'],
                'price': data['market_data']['current_price'],
                'timestamp': data['timestamp']
            })
    
    price_df = pd.DataFrame(price_data)
    price_fig = px.line(price_df, x='timestamp', y='price', color='ticker',
                       title='Price Trends')
    
    # Create news sentiment chart
    sentiment_data = []
    for data in all_data:
        if 'news' in data:
            sentiment_data.append({
                'ticker': data['ticker'],
                'news_count': len(data['news']),
                'timestamp': data['timestamp']
            })
    
    sentiment_df = pd.DataFrame(sentiment_data)
    sentiment_fig = px.bar(sentiment_df, x='ticker', y='news_count',
                          title='News Coverage Volume')
    
    return gauge_fig, radar_fig, price_fig, sentiment_fig

@app.callback(
    Output("new-ticker-input", "value"),
    [Input("add-ticker-button", "n_clicks")],
    [State("new-ticker-input", "value")]
)
def add_ticker(n_clicks, value):
    if n_clicks is None:
        raise PreventUpdate
    
    if value and value.upper() not in tickers:
        tickers.append(value.upper())
        with open('config/tickers.json', 'w') as f:
            json.dump({'tickers': tickers}, f)
    
    return ""

if __name__ == '__main__':
    app.run_server(debug=True) 
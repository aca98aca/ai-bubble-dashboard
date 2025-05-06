"""
Dashboard component for bubble analysis visualization.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from src.analysis.bubble_analysis import BubbleAnalyzer
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def create_bubble_dashboard():
    """Create the bubble analysis dashboard component."""
    
    try:
        # Initialize the analyzer
        analyzer = BubbleAnalyzer()
        data = analyzer.collect_data()
        risk_metrics = analyzer.analyze_bubble_risk()
        
        # Create the layout
        layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H2("AI Sector Bubble Analysis", className="text-center mb-4"),
                    html.Div([
                        dbc.Alert(
                            f"Current Bubble Risk Level: {risk_metrics['bubble_risk_level']}",
                            color="danger" if risk_metrics['bubble_risk_level'] == 'HIGH' else 
                                  "warning" if risk_metrics['bubble_risk_level'] == 'MODERATE' else "success",
                            className="mb-4"
                        )
                    ])
                ])
            ]),
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='ps-ratio-trend',
                        figure=px.line(
                            data,
                            y=['ps_ratio', 'ps_ratio_ma12'],
                            title='P/S Ratio Trend Analysis'
                        ).update_layout(
                            xaxis_title="Date",
                            yaxis_title="P/S Ratio",
                            template="plotly_white"
                        )
                    )
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='correlation-heatmap',
                        figure=px.imshow(
                            data.corr(),
                            title='Correlation Matrix',
                            color_continuous_scale='RdBu'
                        ).update_layout(
                            template="plotly_white"
                        )
                    )
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Risk Metrics", className="mb-3"),
                        html.P(f"Current Deviation: {risk_metrics['current_deviation']:.2f}%"),
                        html.P(f"Volatility: {risk_metrics['volatility']:.2f}%")
                    ], className="p-3 bg-light rounded")
                ], width=6),
                
                dbc.Col([
                    html.Div([
                        html.H4("Market Indicators", className="mb-3"),
                        html.P(f"VIX: {data['vix'].iloc[-1]:.2f}"),
                        html.P(f"Fed Rate: {data['fed_rate'].iloc[-1]:.2f}%"),
                        html.P(f"M2 YoY: {data['m2_yoy'].iloc[-1]:.2f}%")
                    ], className="p-3 bg-light rounded")
                ], width=6)
            ])
        ], fluid=True)
        
        return layout
    except Exception as e:
        logger.error(f"Error creating bubble dashboard: {e}")
        return dbc.Alert(
            "Error loading dashboard data. Please try again later.",
            color="danger",
            className="m-4"
        )

def register_callbacks(app):
    """Register callbacks for the bubble dashboard."""
    
    @app.callback(
        Output('ps-ratio-trend', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_ps_ratio_trend(n):
        try:
            analyzer = BubbleAnalyzer()
            data = analyzer.collect_data()
            return px.line(
                data,
                y=['ps_ratio', 'ps_ratio_ma12'],
                title='P/S Ratio Trend Analysis'
            ).update_layout(
                xaxis_title="Date",
                yaxis_title="P/S Ratio",
                template="plotly_white"
            )
        except Exception as e:
            logger.error(f"Error updating P/S ratio trend: {e}")
            return go.Figure()
    
    @app.callback(
        Output('correlation-heatmap', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_correlation_heatmap(n):
        try:
            analyzer = BubbleAnalyzer()
            data = analyzer.collect_data()
            return px.imshow(
                data.corr(),
                title='Correlation Matrix',
                color_continuous_scale='RdBu'
            ).update_layout(
                template="plotly_white"
            )
        except Exception as e:
            logger.error(f"Error updating correlation heatmap: {e}")
            return go.Figure() 
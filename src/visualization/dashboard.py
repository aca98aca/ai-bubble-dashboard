"""
Main dashboard application for the AI Bubble Dashboard.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.visualization.bubble_dashboard import create_bubble_dashboard, register_callbacks

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create the layout
app.layout = dbc.Container([
    # Interval component for auto-refresh
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # 5 minutes
        n_intervals=0
    ),
    
    # Navigation
    dbc.NavbarSimple(
        brand="AI Bubble Dashboard",
        brand_href="#",
        color="primary",
        dark=True,
    ),
    
    # Main content
    dbc.Row([
        dbc.Col([
            create_bubble_dashboard()
        ], width=12)
    ])
], fluid=True)

# Register callbacks
register_callbacks(app)

def run_dashboard(debug: bool = False, port: int = 8050):
    """Run the dashboard application."""
    app.run_server(debug=debug, port=port)

if __name__ == '__main__':
    run_dashboard(debug=True) 
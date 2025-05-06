"""
Main entry point for the AI Bubble Dashboard.
"""

import argparse
import logging
from src.visualization.dashboard import run_dashboard
from src.utils.config import PATHS
from src.utils.helpers import ensure_directory, logger

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(PATHS['logs'] / 'app.log')
        ]
    )

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description='AI Bubble Dashboard')
    parser.add_argument('--mode', choices=['dashboard'], default='dashboard',
                      help='Application mode (default: dashboard)')
    parser.add_argument('--debug', action='store_true',
                      help='Run in debug mode')
    parser.add_argument('--port', type=int, default=8050,
                      help='Port to run the dashboard on (default: 8050)')
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging()
    logger.info("Starting AI Bubble Dashboard")
    
    # Ensure required directories exist
    for path in PATHS.values():
        ensure_directory(path)
    
    if args.mode == 'dashboard':
        logger.info(f"Starting dashboard on port {args.port}")
        run_dashboard(debug=args.debug, port=args.port)

if __name__ == '__main__':
    main() 
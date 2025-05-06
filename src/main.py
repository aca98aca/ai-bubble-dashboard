import os
import sys
import argparse
from src.data_collection.service import start_service, stop_service
from src.visualization.dashboard import app
from src.utils.config import PATHS
from src.utils.helpers import ensure_directory, logger

def setup_environment():
    """Set up the application environment."""
    # Create necessary directories
    for directory in [PATHS['data_dir'], PATHS['config_dir']]:
        ensure_directory(directory)
    
    # Check for required environment variables
    required_vars = ['FMP_API_KEY', 'SEC_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='AI Bubble Dashboard')
    parser.add_argument('--mode', choices=['dashboard', 'service', 'both'],
                      default='both', help='Run mode: dashboard, service, or both')
    parser.add_argument('--port', type=int, default=8050,
                      help='Port for the dashboard (default: 8050)')
    parser.add_argument('--debug', action='store_true',
                      help='Enable debug mode')
    return parser.parse_args()

def main():
    """Main entry point for the application."""
    args = parse_arguments()
    setup_environment()
    
    try:
        if args.mode in ['service', 'both']:
            logger.info("Starting data collection service...")
            start_service()
        
        if args.mode in ['dashboard', 'both']:
            logger.info(f"Starting dashboard on port {args.port}...")
            app.run_server(debug=args.debug, port=args.port)
        
        if args.mode == 'both':
            # Keep the main thread alive
            while True:
                try:
                    input()
                except KeyboardInterrupt:
                    break
    
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        if args.mode in ['service', 'both']:
            stop_service()
        logger.info("Application stopped")

if __name__ == '__main__':
    main() 
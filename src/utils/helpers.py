import os
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def load_config(config_file):
    """Load configuration from a JSON file."""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading config file {config_file}: {e}")
        return {}

def save_config(config_file, data):
    """Save configuration to a JSON file."""
    try:
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving config file {config_file}: {e}")

def format_currency(value):
    """Format number as currency."""
    if value is None:
        return "N/A"
    if abs(value) >= 1e9:
        return f"${value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"

def format_percentage(value):
    """Format number as percentage."""
    if value is None:
        return "N/A"
    return f"{value*100:.2f}%"

def get_timestamp():
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()

def ensure_directory(directory):
    """Ensure directory exists, create if it doesn't."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")

def save_data(data, filename):
    """Save data to a JSON file."""
    ensure_directory('data')
    filepath = os.path.join('data', filename)
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Saved data to {filepath}")
    except Exception as e:
        logger.error(f"Error saving data to {filepath}: {e}")

def load_data(filename):
    """Load data from a JSON file."""
    filepath = os.path.join('data', filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading data from {filepath}: {e}")
        return {} 
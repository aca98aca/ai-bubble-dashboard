import time
import threading
from datetime import datetime
import logging
from src.utils.config import DATA_COLLECTION_CONFIG, PATHS
from src.utils.helpers import save_data, load_config, logger
from src.data_collection.data_ingestion import DataIngestion

class DataCollectionService:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.running = False
        self.thread = None
        self.last_update = None

    def start(self):
        """Start the data collection service."""
        if self.running:
            logger.warning("Data collection service is already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        logger.info("Data collection service started")

    def stop(self):
        """Stop the data collection service."""
        if not self.running:
            logger.warning("Data collection service is not running")
            return

        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("Data collection service stopped")

    def _run(self):
        """Main service loop."""
        while self.running:
            try:
                self._collect_data()
                time.sleep(DATA_COLLECTION_CONFIG['update_interval'])
            except Exception as e:
                logger.error(f"Error in data collection service: {e}")
                time.sleep(60)  # Wait a minute before retrying

    def _collect_data(self):
        """Collect data for all tickers."""
        tickers = load_config(PATHS['tickers_file']).get('tickers', [])
        if not tickers:
            logger.warning("No tickers configured")
            return

        timestamp = datetime.now().isoformat()
        data = {
            'timestamp': timestamp,
            'tickers': {}
        }

        for ticker in tickers:
            try:
                ticker_data = self.data_ingestion.collect_all_data(ticker)
                data['tickers'][ticker] = ticker_data
                logger.info(f"Collected data for {ticker}")
            except Exception as e:
                logger.error(f"Error collecting data for {ticker}: {e}")

        # Save the collected data
        filename = f"market_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_data(data, filename)
        self.last_update = timestamp

    def get_last_update(self):
        """Get the timestamp of the last data update."""
        return self.last_update

    def is_running(self):
        """Check if the service is running."""
        return self.running

# Create a singleton instance
data_service = DataCollectionService()

def start_service():
    """Start the data collection service."""
    data_service.start()

def stop_service():
    """Stop the data collection service."""
    data_service.stop()

if __name__ == '__main__':
    start_service()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_service() 
import logging
import sys

class logs:

    def __init__(self, filename: str = " "):
        self.filename = filename
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s -  %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)  # Вывод в stdout
            ]
        )
        self.logger = logging.getLogger(__name__)

    def log_info(self, message: str):
        self.logger.info(self.filename + " - " + message)
        
    def log_error(self, message: str):
        self.logger.error(self.fimessage + " - " + message)


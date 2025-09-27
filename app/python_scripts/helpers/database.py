import psycopg2 # type: ignore
import os
from logger import logs
class database:
    
    DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'port': os.getenv('DB_PORT')
    }

    def __init__(self):
        self._connection = None

    def connect(self):
        logger = logs(filename="database.py")
        logger.log_info(f"Connecting to database")
        if self._connection is None:
            self._connection = psycopg2.connect(**self.DB_CONFIG)
        if self._connection is None:
            logger.log_error("Failed to connect to the database")
        else:
            logger.log_info("database connection established")
        return self._connection
    
    def close(self):
        logger = logs(filename="database.py")
        if self._connection:
            self._connection.close()
            self._connection = None
        logger.log_info("database connection closed")

    def get_connection(self):
        return self._connection


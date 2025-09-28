import psycopg2 # type: ignore
import os
class database:
    
    DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'port': os.getenv('DB_PORT_FROM_CONTAINER')
    }

    def __init__(self, logger):
        self.logger = logger
        self._connection = None

    def connect(self):
        self.logger.log_info(f"Connecting to database")
        if self._connection is None:
            self._connection = psycopg2.connect(**self.DB_CONFIG)
        if self._connection is None:
            self.logger.log_error("Failed to connect to the database")
        else:
            self.logger.log_info("database connection established")
        return self._connection
    
    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
        self.logger.log_info("database connection closed")

    def get_connection(self):
        return self._connection
    
    def commit(self):
        if self._connection:
            self._connection.commit()


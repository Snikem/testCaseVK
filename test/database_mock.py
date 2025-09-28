import psycopg2 # type: ignore
import os
from dotenv import load_dotenv

load_dotenv()
class test_database:
    
    DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'port': os.getenv('DB_PORT_FROM_CONTAINER')
    }

    def __init__(self):
        self._connection = None

    def connect(self):
        if self._connection is None:
            self._connection = psycopg2.connect(**self.DB_CONFIG)
        
        return self._connection
    
    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def get_connection(self):
        return self._connection
    
    def commit(self):
        if self._connection:
            self._connection.commit()


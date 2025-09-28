import os
import sys
# Получаем путь к корню проекта
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
# Добавляем helpers в путь
helpers_path = os.path.join(project_root, 'helpers')
sys.path.append(helpers_path)
import requests # type: ignore
from logger import logs # type: ignore
from database import database# type: ignore
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type # type: ignore

maximum_attempts = 3
wait_to_try_again = 2  # seconds
logger = logs(filename="extract.py")
@retry(
    stop=stop_after_attempt(maximum_attempts),   
    wait=wait_fixed(wait_to_try_again),              
    retry=retry_if_exception_type((requests.exceptions.RequestException))
)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def extract_data(db):
    logger.log_info("script extract.py start")
    API_URL = os.getenv('API_URL')
    cursor = db.connect().cursor()
    try:
        data = fetch_data(API_URL)
    except requests.exceptions.RequestException as e:
        logger.log_error(f"Error fetching data from API: {e}")

    for item in data:
        try:
            cursor.execute(
                """
                INSERT INTO USERS_BY_POSTS (user_id, id, title, body)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (item['userId'], item['id'], item['title'], item['body'])
            )
        except Exception as e:
            logger.log_error(f"Error inserting item {item['id']}: {e}")

    db.commit()
    cursor.close()
    db.close()

    logger.log_info("script extract.py end")

if __name__ == "__main__":
    db = database(logger)
    extract_data(db)
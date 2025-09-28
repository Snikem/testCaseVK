import sys
import os
# Получаем путь к корню проекта
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..') 
# Добавляем helpers в путь
helpers_path = os.path.join(project_root, 'helpers')
sys.path.append(helpers_path)

from database import database # type: ignore
from logger import logs # type: ignore
logger = logs(filename="transform.py")
def transform_data(db):


    logger.log_info("script transform.py start")
    cursor = db.connect().cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS top_users_by_posts (
            user_id INT,
            posts_cnt INT,
            calculated_at TIMESTAMP
        )
        """)
    db.commit()
    cursor.execute("TRUNCATE TABLE top_users_by_posts")
    db.commit()
    cursor.execute("""
        INSERT INTO top_users_by_posts (user_id, posts_cnt, calculated_at)
        SELECT
            user_id,
            COUNT(*) AS posts_cnt,
            NOW() AS calculated_at
        FROM users_by_posts
        GROUP BY user_id
        ORDER BY posts_cnt DESC
        """)
    db.commit()
    cursor.close()
    db.close()
    logger.log_info("script transform.py end")

if __name__ == "__main__":
    db = database(logger)
    transform_data(db)
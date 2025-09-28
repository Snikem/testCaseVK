import sys
import os
# Получаем путь к корню проекта
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..')  
# Добавляем helpers в путь
helpers_path = os.path.join(project_root, 'app', 'helpers')
sys.path.append(helpers_path)
from database import database # type: ignore
from logger import logs # type: ignore

logger = logs(filename="migration.py")
db = database(logger)

logger.log_info("script migration.py start")
cursor = db.connect().cursor()
cursor.execute("DROP TABLE IF EXISTS USERS_BY_POSTS;")

cursor.execute("""
    CREATE TABLE USERS_BY_POSTS (
        user_id INTEGER,
        id INTEGER PRIMARY KEY,
        title TEXT,
        body TEXT
    );
""")
cursor.execute("DROP TABLE IF EXISTS top_users_by_posts;")
cursor.execute("""
        CREATE TABLE top_users_by_posts (
            user_id INT,
            posts_cnt INT,
            calculated_at TIMESTAMP
        )
        """)

db.commit()
db.close()
logger.log_info("script migration.py end")
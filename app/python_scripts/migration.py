import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
helpers_path = os.path.join(current_dir, 'helpers')
sys.path.append(helpers_path)
from database import database # type: ignore
from logger import logs # type: ignore
db = database()
logger = logs(filename="migration.py")

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

db.get_connection().commit()
db.close()
logger.log_info("script migration.py end")
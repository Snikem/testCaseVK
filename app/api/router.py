import os
import sys

# Получаем путь к корню проекта
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..') 
# Добавляем helpers в путь
helpers_path = os.path.join(project_root, 'helpers')
sys.path.append(helpers_path)
from flask import Flask # type: ignore
from database import database # type: ignore
from logger import logs # type: ignore


app = Flask(__name__)
logger = logs(filename="router.py")
@app.route("/top", methods=['GET'])
def get_top_users():
    logger.log_info("Received request for /top")
    db = database(logger)
    cursor = db.connect().cursor()
    cursor.execute("""
        SELECT * FROM top_users_by_posts
    """)
    data = cursor.fetchall()

    html = """
    <h1>Top Records</h1>
    <table border="1">
      <tr>
        <th>user_id</th>
        <th>posts_cnt</th>
        <th>calculated_at</th>
      </tr>
    """
    for row in data:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    html += "</table>"

    db.get_connection().commit()
    cursor.close()
    db.close()


    return html
if __name__ == "__main__":
    logger.log_info("Starting Flask app...")
    app.run(host=os.getenv('API_HOST'), port=int(os.getenv('API_PORT_IN_CONTAINER')))
from Database import Database
import requests


API_URL = "https://jsonplaceholder.typicode.com/posts"

db = Database()
cursor = db.connect().cursor()
response = requests.get(API_URL)
data = response.json()

for item in data:
    cursor.execute(
        """
        INSERT INTO USERS_BY_POSTS (user_id, id, title, body)
        VALUES (%s, %s, %s, %s)
        """,
        (item['userId'], item['id'], item['title'], item['body'])
    )
db.get_connection().commit()
db.close()
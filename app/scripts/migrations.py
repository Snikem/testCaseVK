from Database import Database

db = Database()
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
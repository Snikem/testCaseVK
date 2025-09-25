from Database import Database

db = Database()
cursor = db.connect().cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS top_users_by_posts (
        user_id INT,
        posts_cnt INT,
        calculated_at TIMESTAMP
    )
    """)
db.get_connection().commit()
cursor.execute("TRUNCATE TABLE top_users_by_posts")
db.get_connection().commit()
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
db.get_connection().commit()
cursor.close()
db.close()
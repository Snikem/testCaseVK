import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
# Добавляем helpers в путь
helpers_path = os.path.join(project_root, 'app','workers')
sys.path.append(helpers_path)

import pytest  # type: ignore
from unittest.mock import patch

# Замените на реальные имена файлов
from extract import extract_data  # type: ignore
from transform import transform_data  # type: ignore
from database_mock import test_database


@pytest.fixture
def mock_api_data():
    return [
        {"userId": 1, "id": 1, "title": "Test Title 1", "body": "Test Body 1"},
        {"userId": 2, "id": 2, "title": "Test Title 2", "body": "Test Body 2"},
        {"userId": 1, "id": 3, "title": "Test Title 3", "body": "Test Body 3"},
    ]

def clearDB(db):
    with open('db_migrations/schema.sql', 'r') as file:
        sql_script = file.read()

    # Разделяем команды по ';'
    commands = sql_script.split(';')

    cursor = db.connect().cursor()
    for command in commands:
        command = command.strip()
        if command:  # пропускаем пустые команды
            cursor.execute(command)

    db.commit()
    cursor.close()
    db.close()


def test_extract_data_success(mock_api_data):
    postgresql = test_database()
    clearDB(postgresql)

    # Мокаем fetch_data
    with patch('extract.fetch_data', return_value=mock_api_data):
        extract_data(postgresql)
    cursor = postgresql.connect().cursor()
    # Проверяем, что данные записались
    cursor.execute("SELECT COUNT(*) FROM USERS_BY_POSTS")
    count = cursor.fetchone()[0]
    assert count == 3

    cursor.execute("SELECT user_id, id, title FROM USERS_BY_POSTS WHERE id = 1")
    row = cursor.fetchone()
    assert row == (1, 1, "Test Title 1")

    cursor.close()
    postgresql.close()


def test_transform_data_success():
    postgresql = test_database()
    clearDB(postgresql)
    cursor = postgresql.connect().cursor()

    # Создаем таблицу и вставляем данные
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_by_posts (
            user_id INT,
            id INT PRIMARY KEY,
            title TEXT,
            body TEXT
        )
    """)

    cursor.execute("INSERT INTO users_by_posts (user_id, id, title, body) VALUES (1, 1, 'A', 'B'), (1, 2, 'C', 'D'), (2, 3, 'E', 'F'),(3, 4, 'A', 'B'),(3, 5, 'A', 'B'),(3, 6, 'A', 'B')")
    postgresql.commit()

    cursor.close()
    postgresql.close()

    transform_data(postgresql)
    cursor = postgresql.connect().cursor()
    # Проверяем, что агрегированные данные записались
    cursor.execute("SELECT user_id, posts_cnt FROM top_users_by_posts")
    rows = cursor.fetchall()

    assert len(rows) == 3
    assert rows[0] == (3, 3)  # пользователь 3 — 3 поста
    assert rows[1] == (1, 2)  # пользователь 1 — 2 поста
    assert rows[2] == (2, 1)  # пользователь 2 — 1 пост

    cursor.close()
    postgresql.close()
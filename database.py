import sqlite3
import os
DB_NAME = os.getenv("DB_NAME", "parliament_bot.db")

def get_db():
    return sqlite3.connect(DB_NAME)
def init_db():
    """Инициализация базы данных и создание необходимых таблиц."""
    db = get_db()
    cur = db.cursor()

    # Таблица пользователей
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT
        )
    """)

    # Таблица сообщений
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            group_message_id INTEGER
        )
    """)

    # Таблица обращений
    cur.execute("""
        CREATE TABLE IF NOT EXISTS appeals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER,
            text TEXT,
            type TEXT
        )
    """)

    # Таблица заявок
    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER,
            text TEXT
        )
    """)



    db.commit()
    print("DB CREATED")
    db.close()

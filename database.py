import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "database.db")  # путь к файлу базы (можешь указать свой)

def get_db():
    """
    Возвращает соединение с базой данных SQLite.
    Не забудь закрывать его после работы: db.close()
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # чтобы можно было обращаться к колонкам по имени
    return conn

def init_db():
    """
    Инициализация базы данных: создаёт таблицы, если их нет
    """
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

    # Таблица сообщений (для связи сообщений бота и пользователя)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            user_id INTEGER,
            group_message_id INTEGER
        )
    """)

    # Таблица заявок на участие в Парламент
    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            tg_id INTEGER,
            text TEXT
        )
    """)

    # Таблица идей / feedback
    cur.execute("""
        CREATE TABLE IF NOT EXISTS appeals (
            tg_id INTEGER,
            text TEXT,
            type TEXT
        )
    """)

    db.commit()
    db.close()

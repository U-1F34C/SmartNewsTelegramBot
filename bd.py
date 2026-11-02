import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'Subscribers.db'

# Устанавливаем соединение с базой данных
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()


def create_subscribers_table():
    # Создаем таблицу Subscribers, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Subscribers (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        chatid TEXT NOT NULL
    )
    ''')
    connection.commit()


create_subscribers_table()

def add_subscriber(username, chatid):
    # Добавляем нового подписчика в таблицу Subscribers
    cursor.execute('''
    INSERT INTO Subscribers (username, chatid)
    VALUES (?, ?)
    ''', (username, chatid))
    connection.commit()

def remove_subscriber(chatid):
    # Удаляем подписчика из таблицы Subscribers по chatid
    cursor.execute('''
    DELETE FROM Subscribers WHERE chatid = ?
    ''', (chatid,))
    connection.commit()

def get_subscriber(chatid):
    # Получаем подписчика из таблицы Subscribers по chatid
    cursor.execute('''
    SELECT * FROM Subscribers WHERE chatid = ?
    ''', (chatid,))
    if cursor.fetchone() is None:
        return False
    return True

def get_all_subscribers():
    # Получаем всех подписчиков из таблицы Subscribers
    cursor.execute('SELECT * FROM Subscribers')
    return [row[2] for row in cursor.fetchall()]  # Возвращаем только chatid всех подписчиков


if __name__ == "__main__":
    create_subscribers_table()
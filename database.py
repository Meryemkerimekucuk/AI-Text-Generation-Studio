import sqlite3
from datetime import datetime


DATABASE_NAME = "chats.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (chat_id)
            REFERENCES chats(id)
            ON DELETE CASCADE
        )
        """
    )

    connection.commit()

    connection.close()


def create_chat(name):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO chats (name, created_at)
        VALUES (?, ?)
        """,
        (
            name,
            datetime.now().isoformat()
        )
    )

    chat_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return chat_id


def get_all_chats():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, created_at
        FROM chats
        ORDER BY id ASC
        """
    )

    chats = cursor.fetchall()

    connection.close()

    return chats


def get_messages(chat_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, content, created_at
        FROM messages
        WHERE chat_id = ?
        ORDER BY id ASC
        """,
        (chat_id,)
    )

    messages = cursor.fetchall()

    connection.close()

    return messages


def add_message(
    chat_id,
    role,
    content
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO messages (
            chat_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            chat_id,
            role,
            content,
            datetime.now().isoformat()
        )
    )

    connection.commit()

    connection.close()


def rename_chat(
    chat_id,
    new_name
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE chats
        SET name = ?
        WHERE id = ?
        """,
        (
            new_name,
            chat_id
        )
    )

    connection.commit()

    connection.close()


def delete_chat(chat_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM messages
        WHERE chat_id = ?
        """,
        (chat_id,)
    )

    cursor.execute(
        """
        DELETE FROM chats
        WHERE id = ?
        """,
        (chat_id,)
    )

    connection.commit()

    connection.close()
import sqlite3
import hashlib

conn = sqlite3.connect("users.db")
c = conn.cursor()


class dm:
    def initialize_database():
        c.execute(
            """CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    highscore INTEGER DEFAULT 0,
                    remember INTEGER DEFAULT 0);"""
        )

    def get_user(username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hashed_password),
        )
        return c.fetchone()

    def set_user(username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )
        conn.commit()

    def update_remember(username, remember):
        if remember == "Once":
            c.execute("UPDATE users SET remember=0 WHERE username=?", (username,))
        elif remember == "Always":
            c.execute("UPDATE users SET remember=1 WHERE username=?", (username,))
            conn.commit()

    def get_selected_data(username):
        c.execute("SELECT password, remember FROM users WHERE username=?", (username,))
        return c.fetchone()

    def update_password(username, password):
        c.execute("UPDATE users SET password=? WHERE username=?", (password, username))
        conn.commit()

    def get_remembered_users():
        c.execute("SELECT username FROM users WHERE remember=1")
        return c.fetchall()

    def get_user_highscore(username):
        c.execute("SELECT highscore FROM users WHERE username=?", (username,))
        return c.fetchone()[0]

    def update_user_highscore(username, highscore):
        c.execute(
            "UPDATE users SET highscore=? WHERE username=?", (highscore, username)
        )
        conn.commit()

    def close_database():
        c.close()
        conn.close()

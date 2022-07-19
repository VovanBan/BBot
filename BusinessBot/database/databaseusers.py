import sqlite3


class DatabaseUsers:
    def __init__(self):
        with sqlite3.connect('usersdb.db') as db:
            cur = db.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS users (
                             UserID INTEGER PRIMARY KEY NOT NULL,
                             UserTelegramID INTEGER,
                             UserCount INTEGER)''')

    @staticmethod
    def get_db():
        """Gets all values from DB"""
        with sqlite3.connect('usersdb.db') as db:
            cur = db.cursor()
            result = cur.execute('''SELECT * FROM users''')
        return result.fetchall()

    @staticmethod
    def get_user(telegram_id):
        """Gets all information about users from the DB"""
        with sqlite3.connect('usersdb.db') as db:
            cur = db.cursor()
            result = cur.execute('''SELECT * FROM users WHERE UserTelegramID == ?''', (telegram_id,))
        return result.fetchall()

    @staticmethod
    def get_user_count(telegram_id):
        """Gets the id of the photo where the user stopped"""
        with sqlite3.connect('usersdb.db') as db:
            cur = db.cursor()
            result = cur.execute('''SELECT UserCount FROM users WHERE UserTelegramID == ?''', (telegram_id,))
        return result.fetchall()

    @staticmethod
    def add_user(telegram_id, min_count):
        """Adds a user to the DB"""
        with sqlite3.connect('usersdb.db') as db:
            cur = db.cursor()
            cur.execute('''INSERT INTO users (UserTelegramID, UserCount) VALUES (?, ?)''', (telegram_id, min_count))

    @staticmethod
    def update_user_count(telegram_id):
        """Adds one to the UserCount"""
        with sqlite3.connect('usersdb.db') as db:
            cur = db.cursor()
            cur.execute('''UPDATE users SET UserCount = UserCount + 1 WHERE UserTelegramID == ?''', (telegram_id,))

    @staticmethod
    def delete_user(user_id):
        """Delete a user from the DB"""
        with sqlite3.connect('usersdb.db') as db:
            cur = db.cursor()
            cur.execute('''DELETE FROM users WHERE UserID == ?''', (user_id,))

    @staticmethod
    def add_admin():
        """Add the Admin in the DB"""
        with sqlite3.connect('usersdb.db') as db:
            cur = db.cursor()
            cur.execute('''INSERT INTO users (UserTelegramID) VALUES (1)''')

import sqlite3


class DatabaseImages:
    def __init__(self):
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS mems (
                             PhotoID INTEGER PRIMARY KEY NOT NULL,
                             PhotoURL TEXT,
                             PhotoCount INTEGER DEFAULT 1,
                             PhotoLikes INTEGER DEFAULT 0,
                             PhotoDislikes INTEGER DEFAULT 0)''')

    @staticmethod
    def get_db():
        """Gets all values from DB"""
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            result = cur.execute('''SELECT * FROM mems''')
        return result.fetchall()

    @staticmethod
    def get_min_count():
        """Gets the id of the very first available photo from DB"""
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            result = cur.execute('''SELECT MIN(PhotoID) FROM mems''')
        return result.fetchall()

    @staticmethod
    def get_path(image_id):
        """Gets the path to the photo from DB"""
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            result = cur.execute('''SELECT PhotoURL FROM mems WHERE PhotoID == ?''', (image_id,))
        return result.fetchall()

    @staticmethod
    def get_likes(image_id):
        """Gets the number of likes for a photo from DB"""
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            result = cur.execute('''SELECT PhotoLikes FROM mems WHERE PhotoID == ?''', (image_id,))
        return result.fetchall()

    @staticmethod
    def get_dislikes(image_id):
        """Gets the number of dislikes for a photo from DB"""
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            result = cur.execute('''SELECT PhotoDislikes FROM mems WHERE PhotoID == ?''', (image_id,))
        return result.fetchall()

    @staticmethod
    def get_path_old_images():
        """Gets the path to photos whose PhotoCount is greater than or equal to 7"""
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            result = cur.execute('''SELECT PhotoURL FROM mems WHERE PhotoCount >= 7''')
        return result.fetchall()

    @staticmethod
    def add_photo(photo_url):
        """Adds a path before the photo to the DB"""
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            cur.execute('''INSERT INTO mems (PhotoURL) VALUES (?)''', (photo_url,))

    @staticmethod
    def delete_photo(photo_id):
        """Delete a path before the photo from the DB"""
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            cur.execute('''DELETE FROM mems WHERE PhotoID == ?''', (photo_id,))

    @staticmethod
    def update_likes(image_id):
        """Adds one to the PhotoLikes"""
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            cur.execute('''UPDATE mems SET PhotoLikes = PhotoLikes + 1 WHERE PhotoID == ?''', (image_id,))

    @staticmethod
    def update_dislikes(image_id):
        """Adds one to the PhotoDislikes"""
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            cur.execute('''UPDATE mems SET PhotoDislikes = PhotoDislikes + 1 WHERE PhotoID == ?''', (image_id,))

    @staticmethod
    def update_photo_count():
        """Adds one to the PhotoCount"""
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            cur.execute('''UPDATE mems SET PhotoCount = PhotoCount + 1''')

    @staticmethod
    def delete_old_images():
        """Removes photos whose PhotoCount is greater than or equal to 7"""
        with sqlite3.connect('photodb.db') as db:
            cur = db.cursor()
            cur.execute('''DELETE FROM mems WHERE PhotoCount >= 7''')

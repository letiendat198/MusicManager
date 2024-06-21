import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

class DatabaseHelper:
    def __init__(self):
        self.con = sqlite3.connect(os.path.join(os.getcwd(), "database.db"))
        self.cur = self.con.cursor()

    def init_database(self):
        self.cur.execute("PRAGMA foreign_keys = ON;")
        # self.cur.execute("DROP TABLE IF EXISTS playlists")
        # self.cur.execute("DROP TABLE IF EXISTS albums")
        # self.cur.execute("DROP TABLE IF EXISTS songs")
        # self.cur.execute("DROP TABLE IF EXISTS ids")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS songs(
            local_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name, 
            artist, 
            album, 
            track_order, 
            playlist, 
            FOREIGN KEY (album) REFERENCES albums(name),
            FOREIGN KEY (playlist) REFERENCES playlists(name)
            )""")
        self.cur.execute("CREATE TABLE IF NOT EXISTS albums(name PRIMARY KEY, artist, year, genre, image_url)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS playlists(name PRIMARY KEY)")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ids(
            local_id,
            platform,
            platform_id,
            FOREIGN KEY (local_id) REFERENCES songs(local_id)
        )""")

    def add_song(self, name, artist, album, playlist, track_order=None):
        # ID to NULL to use SQLite ROWID
        data = (None, name, artist, album, track_order, playlist)
        self.cur.execute("INSERT INTO songs VALUES (?,?,?,?,?,?) RETURNING local_id", data)
        return self.cur.fetchone()[0]

    def add_playlist(self, name):
        self.cur.execute("INSERT INTO playlists VALUES (?)", (name,))

    def add_album(self, name, artist, year=None, genre=None, img_url=None):
        data = (name, artist, year, genre, img_url)
        self.cur.execute("INSERT INTO albums VALUES (?,?,?,?,?)", data)

    def add_id(self, local_id, platform, platform_id):
        self.cur.execute("INSERT INTO ids VALUES(?,?,?)", (local_id, platform, platform_id))

    # Update a single field or multiple fields if passed a hashmap (Will ignore column and new_value)
    def update_row(self, table, by, filter, column=None, new_value=None, hashmap=None):
        if hashmap is None:
            self.cur.execute("UPDATE ? SET ? = ? WHERE ? = ?", (table, column, new_value, by, filter))
            return
        for field in hashmap:
            self.cur.execute("UPDATE ? SET ? = ? WHERE ? = ?", (table, field, hashmap[field], by, filter))

    def delete_row(self, table, by, filter):
        self.cur.execute("DELETE FROM ? WHERE ? = ?", (table, by, filter))

    def filter_row(self, table, column, condition):
        self.cur.execute("SELECT * FROM {} WHERE {}='{}'".format(table, column, condition))
        return self

    def filter_row_unsafe(self, table, query): # WARNING: SQL INJECTION
        logger.warning("filter_row_unsafe is UNSAFE (duh!). Be careful with user input")
        self.cur.execute("SELECT * FROM " + table + " WHERE " + query)
        return self

    def get_output(self):
        return self.cur.fetchall()

    def commit(self):
        self.con.commit()
    def close(self):
        self.con.close()

# try:
#     db = DatabaseHelper()
#     db.init_database()
#     db.add_album("1989", "Taylor Swift")
#     db.add_playlist("Liked")
#     db.add_song(0, "Blank Space", "Taylor Swift", "1989", "Liked", "Spotify")
# except Exception as e:
#     print(e)
#
# db.commit()
# db.close()